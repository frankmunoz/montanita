import base64
import os
from bs4 import BeautifulSoup

def empaquetar_todo(archivo_entrada, archivo_salida):
    if not os.path.exists(archivo_entrada):
        print(f"Error: No se encuentra el archivo {archivo_entrada}")
        return

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 1. Convertir Imágenes a Base64
    for img in soup.find_all('img'):
        ruta_img = img.get('src')
        if ruta_img and not ruta_img.startswith(('http', 'data:')):
            if os.path.exists(ruta_img):
                with open(ruta_img, "rb") as f_img:
                    codificado = base64.b64encode(f_img.read()).decode('utf-8')
                    ext = os.path.splitext(ruta_img)[1][1:]
                    img['src'] = f"data:image/{ext};base64,{codificado}"
                print(f"Imagen incrustada: {ruta_img}")

    # 2. Incrustar CSS externo
    for link in soup.find_all('link', rel='stylesheet'):
        ruta_css = link.get('href')
        if ruta_css and os.path.exists(ruta_css):
            with open(ruta_css, 'r', encoding='utf-8') as f_css:
                nuevo_style = soup.new_tag('style')
                nuevo_style.string = f_css.read()
                link.replace_with(nuevo_style)
            print(f"CSS incrustado: {ruta_css}")

    # 3. Incrustar JS externo
    for script in soup.find_all('script', src=True):
        ruta_js = script.get('src')
        if ruta_js and os.path.exists(ruta_js):
            with open(ruta_js, 'r', encoding='utf-8') as f_js:
                nuevo_script = soup.new_tag('script')
                nuevo_script.string = f_js.read()
                script.replace_with(nuevo_script)
            print(f"JS incrustado: {ruta_js}")

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f"\n--- ¡ÉXITO! ---")
    print(f"Se ha creado el archivo: {archivo_salida}")

# CONFIGURA AQUÍ TUS NOMBRES DE ARCHIVO
empaquetar_todo('index.html', 'LISTO_PARA_ENVIAR.html')
