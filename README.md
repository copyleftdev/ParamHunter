# ParamHunter

Discover hidden parameters in web applications using brute force, archives from the Wayback Machine, and by analyzing JavaScript files.

## Features

- **Brute Force Parameters**: Uses a wordlist to brute force potential parameters on the target website.
- **Search Archives**: Check the Wayback Machine to find old parameters that might have been used on the website in previous versions.
- **Analyze JavaScript**: Scrutinizes JavaScript files linked in the webpage to find potential parameters.

## Prerequisites

Before you can run ParamHunter, you need the following installed:

- Python 3.x
- `requests` and `beautifulsoup4` Python packages. Install them using:

```
pip install requests beautifulsoup4
```

## Usage

```bash
python ParamHunter.py -u <TARGET_URL> [OPTIONS]
```

**Options**:

- `-u` or `--url`: The target URL to scan. **(Required)**
- `-w` or `--wordlist`: Path to the wordlist used for brute forcing. Default is `default_wordlist.txt`.
- `-t` or `--type`: Request type (either `GET` or `POST`). Default is `GET`.
- `-a` or `--archives`: Search the Wayback Machine for old parameters.
- `-j` or `--javascript`: Analyze linked JavaScript files for parameters.

## Caution

1. **Permissions**: Always ensure you have permission to test or scan any target. Unauthorized scanning and testing can be illegal.
2. **Rate Limiting**: Websites might have rate limits or might block IP addresses sending too many requests in a short amount of time.
3. **Concurrency**: The current implementation uses threading for brute forcing parameters. Consider monitoring your system's resources when using large wordlists.

## Example

To scan `https://example.com` using a wordlist named `params.txt`, searching archives and analyzing JavaScript, use:

```bash
python ParamHunter.py -u https://example.com -w params.txt -a -j
```

## Contributing

Feel free to fork this repository and submit pull requests for enhancements, bug fixes, or additional features. All contributions are welcome!
