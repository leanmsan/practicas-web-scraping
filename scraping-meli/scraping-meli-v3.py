import requests 
from bs4 import BeautifulSoup as bs 
import random 
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Configuración del navegador
browser = uc.Chrome()

# URL base
url_base = 'https://inmuebles.mercadolibre.com.ar/departamentos/venta/_Desde_{}_NoIndex_True'

# Inicializamos la lista de propiedades
propiedades = []

# Datos del sitio
num_paginas = 42
resultados_por_pagina = 48

for i in range(num_paginas):
    desde = i * resultados_por_pagina + 1
    url = url_base.format(desde)

    print(f'\n🌐 Página {i+1} / {num_paginas} | URL: {url}')
    intentos = 0
    max_reintentos = 3
    propiedades_html = []

    while intentos < max_reintentos:
        browser.get(url)
        time.sleep(random.uniform(5, 8))  # Espera mayor para cargar

        soup = bs(browser.page_source, 'html.parser')
        propiedades_html = soup.find_all('div', class_='poly-card__content')

        if propiedades_html:
            break
        else:
            print(f'❗ Intento {intentos+1}: No se encontraron propiedades. Reintentando...')
            intentos += 1
            time.sleep(3)

    print(f'✅ Se encontraron {len(propiedades_html)} propiedades en la página {i+1}')

    for propiedad in propiedades_html:
        try:
            titulo = propiedad.find('h2', class_='poly-box poly-component__title') or \
                     propiedad.find('h3', class_='poly-component__title-wrapper')
            precio = propiedad.find('span', class_='andes-money-amount__fraction')
            atributos = propiedad.find('div', class_='poly-component__attributes-list')
            locacion = propiedad.find('span', class_='poly-component__location')

            propiedades.append({
                'titulo': titulo.text.strip() if titulo else '',
                'precio': precio.text.strip() if precio else '',
                'atributos': [li.text.strip() for li in atributos.find_all('li')] if atributos else [],
                'locacion': locacion.text.strip() if locacion else ''
            })

        except Exception as e:
            print(f'❌ Error al procesar una propiedad: {e}')
            continue

    # Espera antes de pasar a la próxima página
    time.sleep(random.uniform(3, 7))

# Guardar resultados
df = pd.DataFrame(propiedades)
df.to_excel('propiedades_mercadolibre.xlsx', index=False)

# Cierre del navegador
try:
    browser.quit()
except OSError as e:
    print(f'Error al cerrar el navegador: {e}')
finally:
    print(f'\n📦 Total de propiedades extraídas: {len(propiedades)}')
