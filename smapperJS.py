#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# smapperJS 
# By Locu
# Refactored with multithreading and auto-installation

import os
import sys
import argparse
import time
import requests
import threading
import subprocess
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Auto-install missing packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ['requests']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        install_package(package)

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m' 
    DARKCYAN = '\033[36m'
    BLUE =  '\033[94m' 
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Thread-safe print
print_lock = threading.Lock()
def ts_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def check_tools():
    """Check if required external tools are installed"""
    tools = ['gau', 'anti-burl', 'unmap', 'fdupes']
    missing_tools = []
    for tool in tools:
        if subprocess.run(['which' if os.name != 'nt' else 'where', tool], 
                         capture_output=True).returncode != 0:
            missing_tools.append(tool)
    if missing_tools:
        ts_print(f"{color.RED}Missing tools: {', '.join(missing_tools)}{color.END}")
        ts_print("Please install them before running this script")
        sys.exit(1)

def check_input(url):
    if url.startswith(('http://', 'https://')):
        return url
    else:
        ts_print(f'{color.RED}Error: protocol is missing (http,https) for URL: {url}{color.END}')
        return None

def send_request(url):
    try:
        a = urlparse(url)
        fname = os.path.basename(a.path) or 'index'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        r = requests.get(url, timeout=10, verify=False)
        src = r.text
        
        if ".js.map" in src:
            map_url = url + '.map'
            r1 = requests.get(map_url, timeout=10, verify=False)
            if r1.status_code == 200:
                ts_print(f"{color.GREEN}{color.BOLD}MAP FOUND: {color.END}{map_url}")
                
                # Create directory
                dir_path = os.path.join(args.output, fname)
                os.makedirs(dir_path, exist_ok=True)
                
                # Save map file
                fpath = os.path.join(dir_path, fname + '.map')
                with open(fpath, 'wb') as f:
                    f.write(r1.content)
                
                # Run unmap
                output_dir = os.path.join(dir_path, 'smapped')
                cmd = f'unmap "{fpath}" --output "{output_dir}"'
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                ts_print(f"{color.YELLOW}Map not accessible: {map_url}{color.END}")
        else:
            ts_print(f"{color.RED}No map reference found: {url}{color.END}")
    except Exception as e:
        ts_print(f"{color.RED}Error processing {url}: {str(e)}{color.END}")

def process_urls(urls):
    """Process URLs using multithreading"""
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_single_url, urls)

def process_single_url(url):
    uri = check_input(url)
    if uri:
        send_request(uri)

def analyze(file_path):
    ts_print(f'{color.CYAN}-----------------------------------------ANALYZE{color.END}')
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    process_urls(urls)

def main():
    global args
    parser = argparse.ArgumentParser(description='smapperJS - JavaScript Source Map Extractor')
    parser.add_argument('-d', '--domains', help='File containing list of domains', action='store')
    parser.add_argument('-u', '--url', help='Single URL to analyze', action='store')
    parser.add_argument('-l', '--list', help='File containing list of URLs', action='store')
    parser.add_argument('-o', '--output', help='Output directory', required=True, action='store')
    parser.add_argument('-t', '--threads', help='Number of threads (default: 10)', type=int, default=10)
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Check for required tools
    check_tools()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Process based on arguments
    if args.domains:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fl = f"{args.output}-{timestr}"
        cmd = (f"cat {args.domains} | gau | grep '\\.js$' | anti-burl | "
               f"grep -Eo '(http|https)://[a-zA-Z0-9./?=_-]*' | sort -u | tee {args.output}/{fl}")
        ts_print(f"{color.PURPLE}{color.BOLD}Running: {cmd}{color.END}")
        subprocess.run(cmd, shell=True)
        
        file_path = os.path.join(os.getcwd(), args.output, fl)
        analyze(file_path)
        
        ts_print(f"{color.YELLOW}{color.BOLD}\nREMOVING DUPLICATES WITH fdupes...\n{color.END}")
        subprocess.run(f'fdupes -dN -R "{args.output}"', shell=True)
        ts_print(f"{color.BOLD}\nIt's time to start grepping!{color.END}")
    
    elif args.url:
        uri = check_input(args.url)
        if uri:
            send_request(uri)
    
    elif args.list:
        analyze(args.list)
        ts_print(f"{color.YELLOW}{color.BOLD}\nREMOVING DUPLICATES WITH fdupes...\n{color.END}")
        subprocess.run(f'fdupes -dN -R "{args.output}"', shell=True)
        ts_print(f"{color.BOLD}\nIt's time to start grepping!{color.END}")

if __name__ == "__main__":
    main()




	

