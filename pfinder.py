#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Titulo: URL Path Finder (pfinder)
Versao: 1.1 
Data: 09/09/2020 
Homepage: https://www.desecsecurity.com
Tested on: macOS/Linux/Windows 10
'''

from colorama import Fore, Style
import argparse
import pathlib
import concurrent.futures
import time
import requests
import re
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()

# -----------------------------------------------------

print(Fore.RED + '''
 ██▓███   ▄▄▄     ▄▄▄█████▓ ██░ ██      █████▒██▓ ███▄    █ ▓█████▄ ▓█████  ██▀███  
▓██░  ██▒▒████▄   ▓  ██▒ ▓▒▓██░ ██▒   ▓██   ▒▓██▒ ██ ▀█   █ ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░   ▒████ ░▒██▒▓██  ▀█ ██▒░██   █▌▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██    ░▓█▒  ░░██░▓██▒  ▐▌██▒░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░ ▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓   ░▒█░   ░██░▒██░   ▓██░░▒████▓ ░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░ ▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒    ▒ ░   ░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░     
░▒ ░       ▒   ▒▒ ░   ░     ▒ ░▒░ ░    ░      ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░   
░░         ░   ▒    ░       ░  ░░ ░    ░ ░    ▒ ░   ░   ░ ░  ░ ░  ░    ░     ░░   ░        by ''' + Fore.GREEN + 'DESEC' + '''
               ░  ░         ░  ░  ░           ░           ░    ░       ░  ░   ░     
                                                             ░                     
\n''')

print(Fore.YELLOW + "        #################### - URL PATH FINDER - #####################")
print(Fore.YELLOW + "        #                    -  Desec Academy  -                     #")
print(Fore.YELLOW + "        #    Type for help: python3 pfinder.py --help                #")
print(Fore.YELLOW + "        #    Example: python3 pfinder.py -u example.com --robots     #")
print(Fore.YELLOW + "        ##############################################################\n\n")

# -----------------------------------------------------

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def read_wordlist():
    wordlist = args.f
    if isinstance(wordlist, list):
        wordlist = args.f[0]
    try:
        with open(wordlist) as f:
            lines = f.readlines()
            return lines
    except IOError:
        print(Fore.RED + 'Error reading wordlist file!')

def all_wordlist():
    wordlist = read_wordlist()
    return list(chunks(wordlist, 10))

def unique_wordlist():
    wordlist = read_wordlist()
    lines = [re.sub(r'\/.{1,}|\.[a-z]*|\/$', r'', l.strip().lower()) for l in wordlist]
    unique_lines = sorted(set(lines))
    return list(chunks(unique_lines, 10))

def scan_robots():
    print(Fore.YELLOW + '[!] ' + Style.RESET_ALL + 'Scanning paths in robots.txt ...')
    try:
        response = requests.get(domain + 'robots.txt', timeout=3, verify=False)
        data = response.text
        response.close()
        if(data):
            for line in data.split('\n'):
                if line.startswith("Disallow:"):
                    path = re.search(r'\s\/.*$', line)
                    if(path is not None):
                        full_url = domain + path.group(0).strip().replace('/', '')
                        try:
                            r = requests.get(full_url, timeout=4, verify=False)
                            if(r.status_code == 200):
                                print(Fore.GREEN + '[+] ' + Style.RESET_ALL + full_url)
                            r.close()
                        except requests.exceptions.ConnectionError:
                            continue
        print(Fore.GREEN + '[!] ' + Style.RESET_ALL + 'Robots search completed!')
    except requests.exceptions.ConnectionError:
        print(Fore.RED + '[!] ' + Style.RESET_ALL + "Error opening robots.txt or maybe it doesn't exist in server.")

def request_subdomains(subdomains):
    parse = urlparse(domain)
    for subdomain in subdomains:
        try:
            if parse.hostname.startswith('www.'):
                hostname = parse.hostname.replace('www.', '')
            else:
                hostname = parse.hostname 
            full_url =  parse.scheme + '://' + subdomain + '.' + hostname
            r = requests.get(full_url, timeout=5)
            if(r.status_code == 200):
                print(Fore.GREEN + '[+] ' + Style.RESET_ALL + full_url)
            r.close()
        except requests.exceptions.ConnectionError:
            continue

def scan_subdomains():
    print(Fore.YELLOW + '[!] ' + Style.RESET_ALL + 'Scanning subdomains...')
    with concurrent.futures.ProcessPoolExecutor() as exec_subdomains:
        results_subdomain = [exec_subdomains.submit(request_subdomains, subdomains) for subdomains in unique_wordlist()]
        for f in concurrent.futures.as_completed(results_subdomain):
            if(f.result() != None):
                print(f.result())
        print(Fore.GREEN + '[!] ' + Style.RESET_ALL + 'Subdomains search completed!')  

def request_paths(paths):
    for path in paths:
        try:
            full_url = domain + path.strip()
            r = requests.get(full_url, timeout=5)
            if(r.status_code == 200):
                print(Fore.GREEN + '[+] ' + Style.RESET_ALL + full_url)
            r.close()
        except requests.exceptions.ConnectionError:
            continue

def scan_paths():
    print(Fore.YELLOW + '[!] ' + Style.RESET_ALL + 'Scanning paths...')
    with concurrent.futures.ProcessPoolExecutor() as exec_contexts:
        results_paths = [exec_contexts.submit(request_paths, paths) for paths in all_wordlist()]
        for f in concurrent.futures.as_completed(results_paths):
            if(f.result() != None):
                print(f.result())
        print(Fore.GREEN + '[!] ' + Style.RESET_ALL + 'Paths search completed!')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '-url', nargs=1, help='URL Base <mandatory>', required=True, default=None, type=str)
    parser.add_argument('-f', '-file', nargs=1, help='Scan paths in wordlist.txt file', type=str, default='wordlist.txt')
    parser.add_argument('--robots', action='store_true', help='Scan paths in robots.txt', default=False)
    parser.add_argument('--sub', action='store_true', help='Scan subdomains in wordlist.txt file', default=False)
    args = parser.parse_args()

    if not args.u:
        print(Fore.RED + '********************************************')
        print(Fore.RED + '*     URL is required to run script!       *')
        print(Fore.RED + '********************************************')
        print(Fore.YELLOW + 'Usage: python3 pfinder.py -u <url> --robots --sub\n')
    if not pathlib.Path('wordlist.txt').exists() and not pathlib.Path(args.f[0]).exists():
        print(Fore.RED + '*************************************************************************')
        print(Fore.RED + '*          File wordlist.txt not found in this directory.               *')
        print(Fore.RED + '*  Use the -f argument to enter the correct path of your wordlist file. *')
        print(Fore.RED + '*************************************************************************')
    else:
        start = time.perf_counter()
        domain = ''
        schemes = ['www.', 'http://', 'https://']
        for s in schemes:
            try:
                r = requests.get(s + args.u[0], timeout=8, verify=False)
                if r.status_code == 200:
                    domain = r.url    
                    break
            except:
                continue
        if(domain):
            print(Fore.GREEN + '[!] ' + Style.RESET_ALL + 'Valid URL: %s ' % domain)
            scan_paths()
            if(args.sub):
                scan_subdomains()
            if(args.robots):
                scan_robots()
        else:
            print(Fore.RED + '[!] ' + Style.RESET_ALL + 'Unable to scan host >>> ' + args.u[0])
        finish = time.perf_counter()
        print(Fore.BLUE + '[!] ' + Style.RESET_ALL + 'Finished in %s second(s)!' % str(round(finish-start, 2)))