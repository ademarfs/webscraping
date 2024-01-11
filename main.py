import requests  # Importa a biblioteca 'requests' para realizar solicitações HTTP
from bs4 import BeautifulSoup  # Importa 'BeautifulSoup' da biblioteca 'bs4' para análise HTML
import re  # Importa o módulo 're' para trabalhar com expressões regulares
import pandas as pd  # Importa a biblioteca 'pandas' para manipulação de dados em DataFrame

url = 'https://www.empregos.com.br/vagas'  # Atribui a URL do site de destino à variável 'url'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}  # Define cabeçalhos para simular um navegador da web

# Faz uma solicitação HTTP GET para a URL especificada com cabeçalhos personalizados
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')  # Analisa o conteúdo HTML da resposta usando BeautifulSoup
qnt_vagas = soup.find('h2', )  # Busca por um elemento 'h2' (quantidade de vagas - não utilizado)

# Dicionário para armazenar informações sobre as vagas
dic_vagas = {
    'titulo': [],
    'descricao': [],
    'empresa_localizacao': [],
    'publicacao': []
}

# Loop para percorrer páginas de 1 a 4
for i in range(1, 5):
    url_pag = f'https://www.empregos.com.br/vagas/p{i}'  # Constrói a URL da página específica
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')  # Analisa o conteúdo HTML da resposta usando BeautifulSoup
    vagas = soup.find_all('div', class_=re.compile('descricao'))  # Encontra todos os elementos 'div' com a classe que contém 'descricao'
    
    # Loop para extrair informações de cada vaga
    for vaga in vagas:
        titulo = vaga.find('h2').get_text().strip()  # Extrai e limpa o texto do elemento 'h2'
        descricao = vaga.find('p', class_=re.compile('resumo-vaga')).get_text().strip()  # Extrai e limpa o texto do elemento 'p' com a classe que contém 'resumo-vaga'
        empresa_localizacao = vaga.find('span', class_=re.compile('nome-empresa')).get_text().strip()  # Extrai e limpa o texto do elemento 'span' com a classe que contém 'nome-empresa'
        publicacao = vaga.find('span', class_=re.compile('publicado')).get_text().strip()  # Extrai e limpa o texto do elemento 'span' com a classe que contém 'publicado'
        
        # Adiciona as informações ao dicionário
        dic_vagas['titulo'].append(titulo)
        dic_vagas['descricao'].append(descricao)
        dic_vagas['empresa_localizacao'].append(empresa_localizacao)
        dic_vagas['publicacao'].append(publicacao)
    print(url_pag)  # Imprime a URL da página atual durante o loop

# Cria um DataFrame do pandas a partir do dicionário
df = pd.DataFrame(dic_vagas)

# Exporta os dados para um arquivo CSV
df.to_csv('C:/Users/adema/OneDrive/Área de Trabalho/webscraping.csv', encoding='utf-8', sep=';')
