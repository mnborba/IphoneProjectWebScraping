import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def fetch_page():
    url = 'https://www.mercadolivre.com.br/apple-iphone-16-pro-1-tb-titnio-preto-distribuidor-autorizado/p/MLB1040287851#polycard_client=search-nordic&wid=MLB5054621110&sid=search&searchVariation=MLB1040287851&position=6&search_layout=stack&type=product&tracking_id=92c2ddf6-f70e-475b-b41e-fe2742459774'
    response = requests.get(url)
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('h1', class_='ui-pdp-title').get_text(strip=True)
    prices = soup.find_all('span', class_='andes-money-amount__fraction')
    old_price = int(prices[0].get_text(strip=True).replace('.', ''))
    new_price = int(prices[1].get_text(strip=True).replace('.', ''))
    installment_price = int(prices[2].get_text(strip=True).replace('.', ''))

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_price': installment_price,
        'timestamp': timestamp
    }

def save_to_dataframe(product_info, df):
    new_row = pd.DataFrame([product_info])
    """Salva uma linha de dados no banco de dados SQLite usando pandas."""
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Teste das funções
if __name__ == '__main__':
    # DataFrame para acumular os resultados
    df = pd.DataFrame()

    while True:
        # Faz a requisição e parseia a página
        page_content = fetch_page()
        product_info = parse_page(page_content)
        # Converte o dicionário em DataFrame e adiciona ao acumulado usando pd.concat
        df = save_to_dataframe(product_info, df)
        # Exibe o DataFrame atualizado
        print(df)
        # Aguarda 10 segundos antes da próxima execução
        time.sleep(10)