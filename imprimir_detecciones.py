"""
import os
import subprocess


def obtener_ultimos_archivos(directorio, num_archivos=6):

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

    try:
        print(f"Imprimiendo: {archivo}")
        subprocess.run(["libreoffice", "--pt", impresora, archivo], check=True)
        print(f"Archivo '{archivo}' enviado a la impresora '{impresora}' con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al imprimir {archivo}: {e.stderr.decode()}")


def main():
    # Carpeta de notas médicas junto al script
    directorio = os.path.join(os.path.dirname(__file__), 'detecciones_generadas')
    impresora_predeterminada = "Brother_DCP_T220_USB"

    # Obtener los últimos 6 archivos
    ultimos_archivos = obtener_ultimos_archivos(directorio, num_archivos=6)

    if not ultimos_archivos:
        print("No se encontraron archivos en la carpeta 'detecciones_generadas'.")
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

    
"""



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
        # En libreoffice, e.stderr puede ser None a veces, así que comprobamos antes de decodificar
        mensaje_error = e.stderr.decode() if e.stderr else str(e)
        print(f"Error al imprimir {archivo}: {mensaje_error}")


def main():
    # Carpeta de notas médicas junto al script
    directorio = os.path.join(os.path.dirname(__file__), 'detecciones_generadas')
    impresora_predeterminada = "Brother_DCP_T220_USB"

    # Obtener los últimos 6 archivos
    ultimos_archivos = obtener_ultimos_archivos(directorio, num_archivos=6)

    if not ultimos_archivos:
        print("No se encontraron archivos en la carpeta 'detecciones_generadas'.")
        return

    # Mostrar lista numerada al usuario
    print("Seleccione el/los archivo(s) que desea imprimir:")
    for idx, ruta in enumerate(ultimos_archivos, start=1):
        nombre = os.path.basename(ruta)
        fecha_mod = os.path.getmtime(ruta)
        print(f"  {idx}. {nombre} (modificado: {fecha_mod})")

    # Solicitar selección (puede ser un solo número o varios separados por comas, p. ej. 2,5,6)
    entrada = input("Ingrese el/los número(s) del(los) archivo(s) (1-{}), separados por comas: ".format(len(ultimos_archivos)))

    # Procesar la entrada: dividir por comas y convertir a enteros
    indices = []
    try:
        # Eliminamos espacios en blanco y filtramos elementos vacíos
        partes = [p.strip() for p in entrada.split(',') if p.strip() != ""]
        if not partes:
            raise ValueError("No se ingresó ningún número válido.")
        for p in partes:
            numero = int(p)
            indices.append(numero)
    except ValueError:
        print("Entrada no válida. Debe ingresar números separados por comas (por ejemplo: 1,3,5).")
        return

    # Validar cada índice y preparar la lista de archivos a imprimir
    archivos_a_imprimir = []
    for numero in indices:
        if 1 <= numero <= len(ultimos_archivos):
            archivos_a_imprimir.append(ultimos_archivos[numero - 1])
        else:
            print(f"Opción fuera de rango: {numero}. Saliendo.")
            return

    # Imprimir cada archivo seleccionado
    for archivo in archivos_a_imprimir:
        imprimir_archivo(archivo, impresora_predeterminada)


if __name__ == "__main__":
    main()
