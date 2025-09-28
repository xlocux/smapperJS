# smapperJS

A powerful tool for extracting and analyzing JavaScript Source Maps. It uses [gau](https://github.com/lc/gau) to discover JavaScript files, then unpacks Source Maps into a filesystem structure using [unmap](https://github.com/chbrown/unmap). Perfect for security researchers to find API keys, credentials, and other sensitive information.

## Features

- **Multi-threaded processing** for faster analysis
- **Automatic dependency installation**
- **Support for single URLs, URL lists, and domain lists**
- **Duplicate file detection and removal**
- **Color-coded output for better readability**

## Prerequisites

Ensure the following tools are installed on your system:

- [gau](https://github.com/lc/gau) - Get all URLs
- [anti-burl](https://github.com/tomnomnom/hacks/tree/master/anti-burl) - Filter out broken URLs
- [unmap](https://github.com/chbrown/unmap) - Unpack Source Maps
- [fdupes](https://github.com/adrianlopezroche/fdupes) - Remove duplicate files

## Installation

```bash
git clone https://github.com/your-repo/smapperJS.git
cd smapperJS
```

## Usage

```bash
python3 smapperJS.py -o output_directory [options]
```

### Options

- `-d, --domains FILE`    File containing list of domains to analyze
- `-u, --url URL`         Single URL to analyze
- `-l, --list FILE`       File containing list of URLs to analyze
- `-o, --output DIR`      Output directory (required)
- `-t, --threads NUM`     Number of threads (default: 10)

### Examples

1. Analyze a single URL:
   ```bash
   python3 smapperJS.py -u https://example.com/main.js -o results
   ```

2. Analyze a list of URLs:
   ```bash
   python3 smapperJS.py -l urls.txt -o results
   ```

3. Analyze domains from a list:
   ```bash
   python3 smapperJS.py -d domains.txt -o results
   ```

4. Use custom number of threads:
   ```bash
   python3 smapperJS.py -d domains.txt -o results -t 20
   ```

## Output

The tool creates the following structure in the output directory:
```
output/
├── domain1/
│   ├── domain1.map
│   └── smapped/
│       └── (unpacked files)
├── domain2/
│   ├── domain2.map
│   └── smapped/
│       └── (unpacked files)
└── ...
```

## Searching for Sensitive Information

After running smapperJS, you can search for sensitive information using tools like `grep`:

```bash
grep -r "api_key" results/
grep -r "password" results/
grep -r "secret" results/
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License.

