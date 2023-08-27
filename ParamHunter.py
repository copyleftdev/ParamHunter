import requests
from bs4 import BeautifulSoup
import argparse
import threading

session = requests.Session()  # Initialize a session to use for requests

# Global list to hold found parameters
found_params = []

# Thread lock to handle concurrent writes to the found_params list
param_lock = threading.Lock()


def check_param(target_url, param, method):
    if method.upper() == "GET":
        response = session.get(target_url, params={param: 'test'})
    else:  # POST
        response = session.post(target_url, data={param: 'test'})

    if 'test' in response.text:
        with param_lock:
            found_params.append(param)


def brute_force_params(target_url, wordlist, method):
    threads = []

    with open(wordlist, 'r') as wlist:
        for param in wlist:
            param = param.strip()
            t = threading.Thread(target=check_param, args=(target_url, param, method))
            threads.append(t)
            t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    return found_params



def find_old_parameters(target_url):
    base_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        'url': target_url,
        'output': 'text',
        'fl': 'original',
        'limit': '100'  # fetch last 100 URLs, you can adjust this as needed
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        urls = response.text.split("\n")
        for url in urls:
            # Extract the parameters
            if "?" in url:
                params_part = url.split('?')[1]
                params = params_part.split('&')
                for param in params:
                    param_name = param.split('=')[0]
                    print(f"Found old parameter: {param_name}")


def analyze_js(target_url):
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all linked JS files
    script_tags = soup.find_all('script', src=True)
    for tag in script_tags:
        js_link = tag['src']

        # Ensure the JS link is a full URL
        if not js_link.startswith(('http', 'https')):
            if js_link.startswith('/'):
                js_link = target_url.rstrip('/') + js_link
            else:
                js_link = target_url + '/' + js_link

        js_response = requests.get(js_link)
        js_content = js_response.text

        # A naive approach to extract possible parameters: look for variables or object keys
        # This can be expanded with a proper JS parser or AST analyzer for better results
        possible_params = set()  # using a set to avoid duplicates
        for line in js_content.split('\n'):
            if 'var ' in line:  # basic way to check for variable declaration
                possible_param = line.split('var ')[1].split('=')[0].strip()
                possible_params.add(possible_param)

        # Print found parameters
        for param in possible_params:
            print(f"Possible parameter found in JS: {param}")

def main():
    parser = argparse.ArgumentParser(description='ParamHunter: Discover hidden parameters in web applications')
    parser.add_argument('-u', '--url', help='Target URL', required=True)
    parser.add_argument('-w', '--wordlist', help='Path to wordlist', default='default_wordlist.txt')
    parser.add_argument('-t', '--type', help='Request type (GET or POST)', default='GET')
    parser.add_argument('-a', '--archives', help='Search archives for old parameters', action='store_true')
    parser.add_argument('-j', '--javascript', help='Analyze JS for parameters', action='store_true')
    args = parser.parse_args()

    if args.archives:
        find_old_parameters(args.url)

    if args.javascript:
        analyze_js(args.url)

    brute_force_params(args.url, args.wordlist, args.type)
    print(f"Found parameters: {', '.join(found_params)}")


if __name__ == "__main__":
    main()

