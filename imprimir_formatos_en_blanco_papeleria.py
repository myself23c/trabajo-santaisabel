import os
import subprocess
import sys

def listar_subcarpetas(directorio_base):
    """
    Devuelve una lista de los nombres de las subcarpetas en `directorio_base`.
    """
    try:
        entradas = os.listdir(directorio_base)
    except FileNotFoundError:
        print(f"No se encontró el directorio: {directorio_base}")
        return []

    subcarpetas = [nombre for nombre in entradas
                   if os.path.isdir(os.path.join(directorio_base, nombre))]
    return sorted(subcarpetas)

def listar_archivos_validados(directorio, extensiones_permitidas):
    """
    Devuelve una lista de rutas completas de archivos en `directorio`
    que tengan extensiones en `extensiones_permitidas`.
    """
    try:
        entradas = os.listdir(directorio)
    except FileNotFoundError:
        print(f"No se encontró el directorio: {directorio}")
        return []

    archivos = []
    for nombre in entradas:
        ruta_completa = os.path.join(directorio, nombre)
        if os.path.isfile(ruta_completa):
            _, ext = os.path.splitext(nombre.lower())
            if ext in extensiones_permitidas:
                archivos.append(ruta_completa)

    return sorted(archivos)

def imprimir_archivo(archivo, impresora):
    """
    Envía un único archivo a la impresora indicada usando LibreOffice.
    """
    try:
        subprocess.run(
            ["libreoffice", "--pt", impresora, archivo],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        print(f"  ✔ '{os.path.basename(archivo)}' enviado a la impresora '{impresora}'.")
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr.decode().strip() if e.stderr else "Error desconocido"
        print(f"  ✘ Error al imprimir '{os.path.basename(archivo)}': {stderr_msg}")

def main():
    # Ruta base de las carpetas de formatos en blanco (un nivel de subcarpetas)
    directorio_base = os.path.join(os.path.dirname(__file__), "formatos_imprimir_en_blanco")
    impresora_predeterminada = "Brother_DCP_T220_USB"

    # 1. Listar subcarpetas en ./formatos_imprimir_en_blanco
    subcarpetas = listar_subcarpetas(directorio_base)
    if not subcarpetas:
        print("No se encontraron subcarpetas en 'formatos_imprimir_en_blanco'.")
        return

    print("Seleccione la >[CARPETA]< a la que desea ingresar:")
    for idx, carpeta in enumerate(subcarpetas, start=1):
        print(f"  {idx}. {carpeta}")
    try:
        opcion_carpeta = int(input(f"Ingrese el número de carpeta (1-{len(subcarpetas)}): ").strip())
        if opcion_carpeta < 1 or opcion_carpeta > len(subcarpetas):
            print("Opción de carpeta fuera de rango. Saliendo.")
            return
    except ValueError:
        print("Entrada no válida. Debe ingresar un número entero. Saliendo.")
        return

    carpeta_elegida = subcarpetas[opcion_carpeta - 1]
    ruta_carpeta = os.path.join(directorio_base, carpeta_elegida)

    # 2. Listar archivos dentro de la carpeta elegida (extensiones permitidas)
    extensiones = {
        ".pdf",      # PDF
        ".xls", ".xlsx",      # Excel
        ".doc", ".docx",      # Word
        ".odt", ".ods", ".odp", ".jpg"  # LibreOffice (Writer, Calc, Impress)
    }
    archivos_disponibles = listar_archivos_validados(ruta_carpeta, extensiones)
    if not archivos_disponibles:
        print(f"No se encontraron archivos válidos en '{carpeta_elegida}'.")
        return

    print(f"\nArchivos disponibles en '{carpeta_elegida}':")
    for idx, ruta in enumerate(archivos_disponibles, start=1):
        nombre = os.path.basename(ruta)
        print(f"  {idx}. {nombre}")

    # 3. Pedir al usuario que seleccione uno o más archivos (por números separados por comas)
    entrada = input(f"\nIngrese los números de los archivos a imprimir, separados por comas: ").strip()
    if not entrada:
        print("No se ingresaron archivos. Saliendo.")
        return

    # Parsear selección
    seleccion_indices = set()
    for parte in entrada.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if not parte.isdigit():
            print(f"La entrada '{parte}' no es un número válido. Saliendo.")
            return
        num = int(parte)
        if num < 1 or num > len(archivos_disponibles):
            print(f"El número '{num}' está fuera de rango. Saliendo.")
            return
        seleccion_indices.add(num - 1)  # 0-based

    archivos_seleccionados = [archivos_disponibles[i] for i in sorted(seleccion_indices)]
    if not archivos_seleccionados:
        print("No se seleccionaron archivos válidos. Saliendo.")
        return

    # 4. Preguntar cuántas copias (1-10)
    try:
        copias = int(input("¿Cuántas copias desea imprimir de cada archivo? (1-10): ").strip())
        if copias < 1 or copias > 10:
            print("La cantidad de copias debe estar entre 1 y 10. Saliendo.")
            return
    except ValueError:
        print("Entrada no válida. Debe ingresar un número entero. Saliendo.")
        return

    # 5. Imprimir: por cada archivo seleccionado, enviar `copias` trabajos de impresión
    print(f"\nIniciando impresión de {len(archivos_seleccionados)} archivo(s), {copias} copia(s) cada uno:\n")
    for ruta_archivo in archivos_seleccionados:
        nombre_archivo = os.path.basename(ruta_archivo)
        print(f"-> Imprimiendo '{nombre_archivo}' ({copias} copia(s)):")
        for copia_num in range(1, copias + 1):
            print(f"   Copia {copia_num} de '{nombre_archivo}'...", end=" ")
            imprimir_archivo(ruta_archivo, impresora_predeterminada)

    print("\nProceso de impresión finalizado.")

if __name__ == "__main__":
    main()
