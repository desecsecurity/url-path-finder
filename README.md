# url-path-finder

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

Script alternativo para a enumeração de diretórios e arquivos.
Sintam-se livre para contribuir tanto com o código, adicionando melhorias, quanto com a wordlist padrão, adicionando novos diretórios.

  - Robots.txt parser
  - Wordlist personalizada
  - Busca de subdomínios


### Instalação

Pfinder requer o [Python](https://www.python.org/) 3.x+ para rodar.

Instale as dependências antes de executar o script.

```sh
$ git clone https://github.com/desecsecurity/url-path-finder.git
$ pip3 install -r requirements.txt
$ python3 pfinder.py -u <url> -l <wordlist> --robots --sub
```

### Argumentos

Instruções de uso listadas abaixo.

| Args | Default | Required |
| ------ | ------ | ------  |
| -u, -url | None | Yes |
| -l, -list | wordlist.txt | No |
| --robots | False | No |
| --sub | False | No |


### Exemplo

Parseando Robots.txt:
```sh
$ python pfinder.py -u exemplo.com --robots
```

Buscando diretórios + subdomains usando uma wordlist própria:
```sh
$ python pfinder.py -u exemplo.com -l wordlist.txt --robots --sub
```

Mostrar ajuda:
```sh
$ python pfinder.py -h
```

### Todos

- [x] Robots.txt parser
- [x] Buscar subdomain
- [x] Progresso em porcentagem
- [x] Mostrador de status code
- [x] Duração
- [ ] Graphic User Interface

### Screenshots

[![P|Finder](https://i.imgur.com/uSEtOus.png)](https://github.com/desecsecurity/url-path-finder/)

[![P|Finder](https://i.imgur.com/LaLnOAg.png)](https://github.com/desecsecurity/url-path-finder/)

