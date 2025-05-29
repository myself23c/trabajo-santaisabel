import os
import subprocess
from datetime import datetime

def obtener_ultimos_archivos(directorio, num_archivos=2):
    try:
        archivos = sorted(
            (os.path.join(directorio, archivo) for archivo in os.listdir(directorio)),
            key=lambda f: os.path.getmtime(f),
            reverse=True
        )
        return archivos[:num_archivos]
    except Exception as e:
        print(f"Error al obtener los archivos: {str(e)}")
        return []

def imprimir_archivos(archivos, impresora_predeterminada):
    try:
        for archivo in archivos:
            print(f"Imprimiendo el archivo: {archivo}")
            subprocess.run(["libreoffice", "--pt", impresora_predeterminada, archivo], check=True)
            print(f"Archivo {archivo} enviado a la impresora {impresora_predeterminada} con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar imprimir el archivo {archivo}: {e.stderr.decode()}")

def main():
    directorio_notas_medicas = os.path.join(os.path.dirname(__file__), 'notas_medicas')
    impresora_predeterminada = "Brother_DCP_T220_USB"

    archivos = obtener_ultimos_archivos(directorio_notas_medicas)

    if not archivos:
        print("No se encontraron archivos en la carpeta 'notas_medicas'.")
        return

    imprimir_archivos(archivos, impresora_predeterminada)

if __name__ == "__main__":
    main()
