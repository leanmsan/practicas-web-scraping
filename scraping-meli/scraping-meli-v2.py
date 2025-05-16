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

# Inicializamos una lista para guardar los datos
propiedades = []

# Número total de páginas a recorrer (42 según mencionaste)
num_paginas = 42
resultados_por_pagina = 48

# Bucle para recorrer cada página
for i in range(0, num_paginas):
    # Calcular el valor de _Desde_ (comienza en 1, 49, 97, ...)
    desde = i * resultados_por_pagina + 1
    url = url_base.format(desde)

    # Abrir la página con Selenium
    browser.get(url)
    
    # Esperar un poco para que cargue la página
    time.sleep(random.uniform(2, 5))
    
    # Crear objeto BeautifulSoup para analizar el HTML
    soup = bs(browser.page_source, 'html.parser')

    # Encontrar las tarjetas de propiedades
    propiedades_html = soup.find_all('div', class_='poly-card__content')

    # Extraer la información de cada propiedad
    for propiedad in propiedades_html:
        try:
            titulo = propiedad.find('h3', class_='poly-component__title').text.strip()
            precio = propiedad.find('span', class_='andes-money-amount andes-money-amount--cents-superscript').text.strip()
            atributos = [attr.text.strip() for attr in propiedad.find_all('li', class_='poly-attributes_list__item poly-attributes_list__separator')]
            locacion = propiedad.find('span', class_='poly-component__location').text.strip()
            
            # Guardar los datos en la lista
            propiedades.append({
                'titulo': titulo,
                'precio': precio,
                'atributos': atributos,
                'locacion': locacion
            })

        except AttributeError:
            # Si no encuentra alguno de los elementos, pasa al siguiente
            continue

    # Pausa entre cada página para evitar bloqueos
    time.sleep(random.uniform(3, 7))

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(propiedades)

# Guardar el DataFrame en un archivo Excel
df.to_excel('propiedades_mercadolibre.xlsx', index=False)

# Cerrar el navegador de manera segura
try:
    browser.quit()
except OSError as e:
    print(f"Error al cerrar el navegador: {e}")
finally:
    print(f"Se extrajeron {len(propiedades)} propiedades")

