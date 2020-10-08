#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# smapperJS 
# By Locu

# Import libraries
import os
import subprocess
import sys
import argparse
import time
import requests
import fileinput
from urllib.parse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning 

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


    
# Command line Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domains', help='Collects js links from domains list', action='store')
parser.add_argument('-u', '--url', help='Input  URL', action='store')
parser.add_argument('-l', '--list', help='Input URL list', action='store')
parser.add_argument('-o', '--output', help='Output directory', action='store')

if len(sys.argv)<2:
	print('eg: python %s -l url.list -d /url/' % sys.argv[0])
	args = parser.parse_args(['-h'])
else:
	args = parser.parse_args()


def parser_error(errmsg):

    print('Usage: python %s [Options] use -h for help' % sys.argv[0])
    print('Error: %s' % errmsg)
    sys.exit()

#check url protocols
def check_input(url):
	if url.startswith(('http://', 'https://')):
		return url
	else:
		print('Error: protocol is missing (http,https)')
		sys.exit(1)


def send_request(url):
	try:
		print('-----------------------------------------------SENDING REQUEST')
		a = urlparse(url)
		fname=(os.path.basename(a.path))
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		r = requests.get(url)
		src=r.text
		if (".js.map" in src):
			r1=requests.get(url+'.map')
			print()
			print( color.GREEN, color.BOLD + 'MAP FOUND:\n ', color.END, url +'.map')
			os.makedirs(args.output+'/'+fname)
			fpath=args.output+'/'+fname+'/'+fname+'.map'
			with open(fpath, 'wb') as f:
				f.write(r1.content)
				cmd= ('unmap ' + fpath +' --output ' + args.output+'/'+fname + '/smapped/')
				os.system(cmd)
		else:
			print(color.RED , url,color.END)
	except requests.exceptions.RequestException as e:
		pass
		
		
def analyze(f):
	print('-----------------------------------------ANALYZE')
	url_list = []
	url_list = filter(None, open(f, 'r').read().splitlines())
	for url in url_list:
		uri = check_input(url)
		try:
			send_request(uri)
		except:
			pass
				
if args.output:
  try:
    os.makedirs(args.output)
  except FileExistsError:
   pass
	
if args.domains:
	try:
		timestr = time.strftime("%Y%m%d-%H%M%S")
		fl=(args.output +'-'+ timestr)
		cmd= ( 'cat '+args.domains + ' | waybackurls | grep "\.js$" | anti-burl | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | sort -u | tee ' + args.output +'/'+ fl)
		print( color.PURPLE, color.BOLD, cmd, color.END)
		os.system(cmd)
		cwd = os.getcwd()
		print(cwd +'/'+args.output +'/'+ fl)
		analyze(cwd +'/'+args.output +'/'+ fl)
		print( color.YELLOW, color.BOLD + '\nREMOVING DUPLICATES WITH fdupes...\n', color.END)
		os.system('fdupes -dN -R ' + args.output)
		print( color.BOLD,  '\n It\'s time to start grepping!', color.END)
	except:
		print

if args.url:
	uri = check_input(args.url)
	try:
		send_request(uri)
	except:
		pass


if args.list:
	url_list = []
	url_list = filter(None, open(args.list, 'r').read().splitlines())
	for url in url_list:
		uri = check_input(url)
		try:
			send_request(uri)
		except:
			pass
	print( color.YELLOW, color.BOLD + '\nREMOVING DUPLICATES WITH fdupes...\n', color.END)
	os.system('fdupes -dN -R' +args.output+'/')
	print( color.BOLD,  '\n It\'s time to start grepping!', color.END)




	

