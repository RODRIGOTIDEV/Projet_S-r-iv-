import requests
from bs4 import BeautifulSoup

def get_http(url, nome_livro):

	nome_livro = nome_livro.replace(' ', '%20')
	url = '{0}?q={1}'.format(url, nome_livro)

	try:
		return requests.get(url)
	except (requests.exceptions.HTTPError, requests.exceptions.RequestException,
				requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
		print(str(e))
	except Exception as e:
		raise

def get_produtos(content):

	soup = BeautifulSoup(content, 'lxml')
	produtos = soup.find_all('div', {'class':'cs-list-container'})

	lista_produtos = []
	for produto in produtos:
		info_produto = [produto.a.get('href'), produto.a.string]
		lista_produtos.append(info_produto)
	return lista_produtos

def get_http_page_produto(lista_produtos):

	for produto in lista_produtos:

		try:
			r = requests.get(produto[0])
		except (requests.exceptions.HTTPError, requests.exceptions.RequestException,
				requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
			print(str(e))
			r = None
		except Exception as e:
			raise

		parse_page_produto(r.text, produto[0], produto[1])
		break

def parse_page_produto(content, url_produto, titulo):

	soup = BeautifulSoup(content, 'lxml')
	with open('result.html', 'w') as f:
		f.write(content)


if __name__ == '__main__':

	url = 'http://busca.saraiva.com.br/'
	nome_livro = 'redes de computadores'

	r = get_http(url, nome_livro)

	if r:
		lista_produtos = get_produtos(r.text)
		get_http_page_produto(lista_produtos)