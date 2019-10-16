# -*- coding: utf-8 -*-

'''
Titulo: URL Path Finder (pfinder)
Versao: 1.0 
Data: 16/10/2019 
Homepage: https://www.desecsecurity.com
Tested on: macOS/Linux/Windows 10
'''

import urllib.request
from urllib.error import URLError, HTTPError
import time
from datetime import datetime, timedelta
from colorama import Fore
import argparse
import sys


achados_global = []

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
print(Fore.YELLOW + "        #      Uso: python3 pfinder.py -u exemplo.com --robots       #")
print(Fore.YELLOW + "        ##############################################################\n\n")


# -----------------------------------------------------


def formatar_url(url):
    if not url.endswith('/'):
        url = url + '/'

    if url.startswith('www.'):
        url = url.replace('www.', 'http://')

    if not url.startswith('www') or not url.startswith('http'):
        url = 'http://' + url

    return url

# -----------------------------------------------------


def formatar_subdomain(url):
    if url.startswith('www.'):
        url = url.replace('www.', '')

    if url.startswith('http://'):
        url = url.replace('http://', '')

    if url.startswith('https://'):
        url = url.replace('https://', '')

    return url

# -----------------------------------------------------


def read_robots():
    robots_path = formatar_url(url) + 'robots.txt'

    print(Fore.YELLOW + '[' + Fore.BLUE + '+' + Fore.YELLOW + ']' + Fore.BLUE + ' Buscando paths no robots.txt...')

    try:
        data = urllib.request.urlopen(robots_path).read().decode("utf-8")
        for item in data.split("\n"):
            if item.startswith("Disallow:"):
                robots_found = item[11:]
                found.append(robots_found + Fore.YELLOW + ' (ROBOTS.TXT)')
                print(Fore.YELLOW + '[' + Fore.BLUE + '*' + Fore.YELLOW + ']' + Fore.BLUE + " Encontrado:" + Fore.YELLOW, robots_found)

    except HTTPError:
        print(Fore.YELLOW + '[' + Fore.RED + 'x' + Fore.YELLOW + ']' + Fore.BLUE + " Não foi possível parsear o robots.txt!")

# -----------------------------------------------------


def read_wordlist():
    global lines

    try:
        with open(wordlist) as path:
            lines = path.readlines()

    except:
        print(Fore.RED + 'Error ao ler wordlist.')

# -----------------------------------------------------


def progress(index):
    path_length = len(lines)
    porcentagem = round((index / path_length) * 100, 1)
    porcentagem = str(porcentagem) + '%  ' + '[' + str(index) + '/' + str(path_length) + ']'

    return porcentagem

# -----------------------------------------------------


def duracao(total_time):
    sec = timedelta(seconds=total_time)
    d = datetime(1, 1, 1) + sec

    total_time = Fore.BLUE + "\nDuracao: %dd:%dh:%dm:%ds" % (d.day-1, d.hour, d.minute, d.second)

    return total_time

# -----------------------------------------------------s


# def test():
#     a = urllib.request.urlopen('http://google.com')
#     print(a.getcode())

# -----------------------------------------------------


def find_paths():
    global total_time
    global found
    # test()
    read_wordlist()
    index = 0
    found_count = 0
    found = []

    if robots:
        read_robots()

    for path in lines:
        path = path.rstrip()
        index += 1

        try:
            code = urllib.request.urlopen(formatar_url(url) + path).getcode()
            print(Fore.YELLOW + '[' + Fore.GREEN + str(index) + Fore.YELLOW + ']', Fore.GREEN + 'Encontrado! Path:', \
                                        Fore.YELLOW + path + ' -> ' + progress(index) + ' [CODE : ' + str(code) + ']')
            found.append(path)

        except HTTPError:
            print(Fore.YELLOW + '[' + Fore.BLUE + str(index) + Fore.YELLOW + ']', Fore.RED + 'Falha:', \
                                        formatar_url(url) + Fore.BLUE + path + Fore.YELLOW + ' -> ' + progress(index))

        except URLError as e:
            print('Erro ao rodar o script. Provavelmente um erro na URL.')
            print(Fore.RED + 'ERRO:', e)
            break

    end = time.time()
    total_time = end - start

    if len(found) > 0:  
        print('\n' + Fore.GREEN + '########## [' + Fore.BLUE + str(len(found)) + Fore.GREEN + '] PATH(s) ENCONTRADO(s) ##########\n')
        for sub in achados_global:
            print(sub)

        for path in found:
            found_count += 1
            print(Fore.YELLOW + '[' + Fore.BLUE + str(found_count) + Fore.YELLOW + '] ' + Fore.BLUE + formatar_url(url) + Fore.GREEN + path)

    else:
        print(Fore.RED + '\nNada foi encontrado. Tente uma nova wordlist!')

    print(duracao(total_time) + '\n')


# -----------------------------------------------------


def subdomain():
    global found
    read_wordlist()
    index = 0
    found_count = 0
    found = []



    ### FORMATANDO WORDLIST PARA BUSCA DE SUBDOMÍNIOS ###
    if robots:
        read_robots()

    for sub in lines:
        sub = sub.rstrip()

        if sub.endswith('/'):
            sub = sub.replace('/', '.')

        if sub.endswith('.php') or sub.endswith('.txt')  or sub.endswith('.asp'):
            sub = sub[:-3]

        if sub.endswith('.html'):
            sub = sub[:-4]

        sub = 'http://' + sub

        index += 1

        try:
            code = urllib.request.urlopen(sub + formatar_subdomain(url)).getcode()
            print(Fore.YELLOW + '[' + Fore.GREEN + str(index) + Fore.YELLOW + ']', Fore.GREEN + 'Encontrado! Subdomínio:', \
                                                Fore.YELLOW + sub + formatar_subdomain(url) + ' -> ' + progress(index) + ' [CODE : ' + str(code) + ']')
            found.append(sub)
            achados_global.append(Fore.YELLOW + '[' + Fore.BLUE + 'X' + Fore.YELLOW + '] ' + sub + Fore.BLUE + formatar_subdomain(url) + Fore.YELLOW + ' (SUBDOMÍNIO)')

        except HTTPError:
            print(Fore.YELLOW + '[' + Fore.BLUE + str(index) + Fore.YELLOW + ']', Fore.RED + 'Falha:', \
                                                sub + formatar_subdomain(url) + Fore.YELLOW + ' -> ' + progress(index))

        except ValueError:
            print(Fore.YELLOW + '[' + Fore.BLUE + str(index) + Fore.YELLOW + ']', Fore.RED + 'Falha:', \
                                                sub + formatar_subdomain(url) + Fore.YELLOW + ' -> ' + progress(index))

        except URLError as e:
            print(Fore.YELLOW + '[' + Fore.BLUE + str(index) + Fore.YELLOW + ']', Fore.RED + 'Falha:', \
                                                sub + formatar_subdomain(url) + Fore.YELLOW + ' -> ' + progress(index))

    if len(found) > 0:
        print('\n' + Fore.GREEN + '########## [' + Fore.BLUE + str(len(found)) + Fore.GREEN + '] SUBDOMÍNIOS(s) ENCONTRADO(s) ##########\n')
        for sub in found:
            found_count += 1
            print(Fore.YELLOW + '[' + Fore.BLUE + str(found_count) + Fore.YELLOW + '] ' + Fore.BLUE + sub + formatar_subdomain(url) + '\n')

    else:
        print(Fore.RED + '\nNada foi encontrado. Tente uma nova wordlist!')


# -----------------------------------------------------


if __name__ == '__main__':
    global start
    global robots
    robots = False
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '-url', nargs=1, help='URL Base <obrigatório>', default=None, type=str)
    parser.add_argument('-l', '-list', nargs=1, help='Wordlist para busca', default="wordlist.txt", type=str)
    parser.add_argument('--robots', action='store_true', help='Parsear arquivo robots.txt e adicionar regra à wordlist', default=False)
    parser.add_argument('--sub', action='store_true', help='Busca de subdomínio na wordlist', default=False)
    args = parser.parse_args()

    if not args.u:
        print(Fore.RED + '********************************************')
        print(Fore.RED + '* A URL é necesseária para rodar o script! *')
        print(Fore.RED + '********************************************')
        print(Fore.YELLOW + 'Uso: python3 pfinder.py -u <url> --robots --sub\n')

    else:
        url = args.u[0]

    if args.l:
        wordlist = args.l

    if args.sub:
        subdomain()

    if args.robots:
        robots = True

    if len(sys.argv) > 1:
        start = time.time()
        find_paths()