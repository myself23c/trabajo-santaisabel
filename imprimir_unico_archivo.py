import os
import subprocess


def obtener_ultimos_archivos(directorio, num_archivos=6):
    """
    Devuelve una lista de los últimos `num_archivos` ordenados por fecha de modificación descendente.
    """
    try:
        archivos = sorted(
            (os.path.join(directorio, f) for f in os.listdir(directorio)),
            key=lambda f: os.path.getmtime(f),
            reverse=True
        )
        return archivos[:num_archivos]
    except Exception as e:
        print(f"Error al obtener los archivos: {e}")
        return []


def imprimir_archivo(archivo, impresora):
    """
    Envía un único archivo a la impresora indicada.
    """
    try:
        print(f"Imprimiendo: {archivo}")
        subprocess.run(["libreoffice", "--pt", impresora, archivo], check=True)
        print(f"Archivo '{archivo}' enviado a la impresora '{impresora}' con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al imprimir {archivo}: {e.stderr.decode()}")


def main():
    # Carpeta de notas médicas junto al script
    directorio = os.path.join(os.path.dirname(__file__), 'notas_medicas')
    impresora_predeterminada = "Brother_DCP_T220_USB"

    # Obtener los últimos 6 archivos
    ultimos_archivos = obtener_ultimos_archivos(directorio, num_archivos=6)

    if not ultimos_archivos:
        print("No se encontraron archivos en la carpeta 'notas_medicas'.")
        return

    # Mostrar lista numerada al usuario
    print("Seleccione el archivo que desea imprimir:")
    for idx, ruta in enumerate(ultimos_archivos, start=1):
        nombre = os.path.basename(ruta)
        print(f"  {idx}. {nombre} (modificado: {os.path.getmtime(ruta)})")

    # Solicitar selección
    try:
        opcion = int(input("Ingrese el número del archivo (1-{}): ".format(len(ultimos_archivos))))
        if 1 <= opcion <= len(ultimos_archivos):
            archivo_seleccionado = ultimos_archivos[opcion - 1]
            imprimir_archivo(archivo_seleccionado, impresora_predeterminada)
        else:
            print("Opción fuera de rango. Saliendo.")
    except ValueError:
        print("Entrada no válida. Debe ingresar un número.")


if __name__ == "__main__":
    main()
