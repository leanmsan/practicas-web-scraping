import requests
from bs4 import BeautifulSoup
import pandas as pd

payload = { 'api_key': '9a4e9d1aadb6222410695fedc563afd7', 'url': 'https://inmuebles.mercadolibre.com.ar/departamentos/venta/_NoIndex_True' }
response = requests.get('https://api.scraperapi.com/', params=payload)

print(response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # La clase que contiene es div class="poly-card__content"
    propiedades_html = soup.find_all('div', class_='poly-card__content')

    propiedades = []

    for propiedad in propiedades_html:
        titulo = propiedad.find('h2', class_='poly-box poly-component__title').text.strip()
        precio = propiedad.find('span', class_='andes-money-amount__fraction').text.strip()
        atributos = [attr.text.strip() for attr in propiedad.find_all('li', class_='poly-attributes-list__item')]
        locacion = propiedad.find('span', class_='poly-component__location').text.strip()

        propiedades.append({
            'titulo': titulo,
            'precio': precio,
            'atributos': atributos,
            'locacion': locacion
        })

    # Crear un DataFrame de pandas
    df = pd.DataFrame(propiedades)

    # Guardar el DataFrame en un archivo Excel
    df.to_excel('propiedades.xlsx', index=False)

print(propiedades)