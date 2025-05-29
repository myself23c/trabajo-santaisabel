from PIL import Image
import pytesseract
import os

def extract_text_from_image(image_path):
    # Asegúrate de que pytesseract puede encontrar tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Abre la imagen
    image = Image.open(image_path)
    # Usa pytesseract para extraer texto
    text = pytesseract.image_to_string(image)
    return text

def save_text_to_file(text, image_path):
    # Obtiene el nombre base del archivo de imagen sin la extensión
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    # Define la ruta del archivo de texto
    text_file_path = f"{base_name}.txt"
    # Escribe el texto en el archivo
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

image_path = 'Captura3.JPG'
text = extract_text_from_image(image_path)
save_text_to_file(text, image_path)
print(f"Texto extraído guardado en {os.path.splitext(image_path)[0]}.txt")
