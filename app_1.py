import requests

def fetch_page():
    url = 'https://www.mercadolivre.com.br/apple-iphone-16-pro-1-tb-titnio-preto-distribuidor-autorizado/p/MLB1040287851#polycard_client=search-nordic&wid=MLB5054621110&sid=search&searchVariation=MLB1040287851&position=6&search_layout=stack&type=product&tracking_id=92c2ddf6-f70e-475b-b41e-fe2742459774'
    response = requests.get(url)
    return response.text

# Teste da função
if __name__ == '__main__':
    page_content = fetch_page()
    print(page_content)  # Mostra os primeiros 500 caracteres do HTML
