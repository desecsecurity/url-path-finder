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
$ python3 pfinder.py -u <url> -f <wordlist> --robots --sub
```

### Argumentos

Instruções de uso listadas abaixo.

| Args | Default | Required |
| ------ | ------ | ------  |
| -u, -url | None | Yes |
| -f, -file | wordlist.txt | No |
| --robots | False | No |
| --sub | False | No |


### Exemplo

Parseando Robots.txt:
```sh
$ python pfinder.py -u exemplo.com --robots
```

Buscando diretórios + subdomains usando uma wordlist própria:
```sh
$ python pfinder.py -u exemplo.com -f /home/user/wordlist.txt --robots --sub
```

Mostrar ajuda:
```sh
$ python pfinder.py -h
```

### Todos

- [x] Robots.txt parser
- [x] Buscar subdomain
- [x] Duração
- [ ] Mostrador de status code
- [ ] Progresso em porcentagem
- [ ] Graphic User Interface

### Screenshots

[![P|Finder](https://i.imgur.com/cnVylwV.png)](https://github.com/desecsecurity/url-path-finder/)

