import requests
from bs4 import BeautifulSoup
import time
import sqlite3
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

def create_connection(db_name='iphone_prices.db'):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    """Cria a tabela de preços se ela não existir."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()

def save_to_database(conn, data):
    """Salva uma linha de dados no banco de dados SQLite usando pandas."""
    df = pd.DataFrame([data])  # Converte o dicionário em um DataFrame de uma linha
    df.to_sql('prices', conn, if_exists='append', index=False)  # Salva no banco de dados

def get_max_price(conn):
    """Consulta o maior preço registrado até o momento."""
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(new_price), timestamp FROM prices")
    result = cursor.fetchone()
    if result and result[0] is not None:
        return result[0], result[1]
    return None, None

# Função principal
if __name__ == '__main__':
    # Configuração do banco de dados
    conn = create_connection()
    setup_database(conn)

    while True:
        # Faz a requisição e parseia a página
        page_content = fetch_page()
        product_info = parse_page(page_content)
        current_price = product_info['new_price']
        
        # Obtém o maior preço já salvo
        max_price, max_price_timestamp = get_max_price(conn)
        
        # Comparação de preços
        if max_price is None or current_price > max_price:
            print(f"Preço maior detectado: {current_price}")
            max_price = current_price  # Atualiza o maior preço
            max_price_timestamp = product_info['timestamp']  # Atualiza o timestamp do maior preço
        else:
            print(f"O maior preço registrado é {max_price} em {max_price_timestamp}")

        # Salva os dados no banco de dados SQLite
        save_to_database(conn, product_info)
        print("Dados salvos no banco:", product_info)
        
        # Aguarda 10 segundos antes da próxima execução
        time.sleep(10)

    # Fecha a conexão com o banco de dados
    conn.close()
