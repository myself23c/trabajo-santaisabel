#!/usr/bin/env python3
# recordatorios_menu.py

import os
import json
import datetime
import sys
from dotenv import load_dotenv, find_dotenv

# 1. Buscar automáticamente el .env hacia arriba en los padres del script
#    find_dotenv() retornará la ruta absoluta donde encuentre el archivo ".env".
ruta_env = find_dotenv(filename=".env", raise_error_if_not_found=True)

# 2. Cargar las variables desde ese .env
load_dotenv(ruta_env)

# 3. Obtener la ruta del CSV
ruta_recordatorios = os.getenv("RECORDATORIOS_JSON_PATH")  # ya viene como string
if not ruta_recordatorios:
    raise RuntimeError("No se encontró DB_PATH en el .env")



# Nombre del archivo JSON donde se guardan los recordatorios
JSON_FILE = ruta_recordatorios


def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def cargar_recordatorios():
    """
    Lee y devuelve la lista de recordatorios desde JSON_FILE.
    Si no existe o está corrupto, devuelve lista vacía.
    Cada recordatorio es un dict con claves: "date" (str dd/mm/aaaa),
    "text" (str), "days" (int).
    """
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos if isinstance(datos, list) else []
    except (json.JSONDecodeError, IOError):
        print(f"Aviso: no se pudo leer o interpretar {JSON_FILE}. Se ignorará su contenido.")
        return []


def guardar_recordatorios(lista):
    """
    Guarda la lista de recordatorios en JSON_FILE (sobrescribe).
    """
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
    except IOError:
        print(f"Error: no se pudo escribir en {JSON_FILE}.")


def fecha_valida(fecha_str):
    """
    Valida que fecha_str esté en formato dd/mm/aaaa y retorne objeto datetime.date;
    si no, devuelve None.
    """
    try:
        return datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        return None


def obtener_recordatorios_activos(lista):
    """
    Dada la lista de recordatorios (cada uno con 'date', 'text', 'days'),
    devuelve una lista de strings formateadas para imprimir, solo con los
    que están activos HOY.
    """
    hoy = datetime.date.today()
    lineas = []
    for rec in lista:
        fecha_rec = fecha_valida(rec.get("date", ""))
        if not fecha_rec:
            continue
        dias = rec.get("days", 0)
        fecha_fin = fecha_rec + datetime.timedelta(days=(dias - 1))
        if fecha_rec <= hoy <= fecha_fin:
            texto = rec.get("text", "").strip()
            linea = f"{rec['date']} — {texto}"
            lineas.append(linea)
    return lineas


def imprimir_cuadro(lineas):
    """
    Recibe una lista de strings (cada una es una línea de recordatorio activo).
    Si la lista está vacía, imprime un mensaje genérico.
    Luego dibuja un 'cuadro' ASCII alrededor.
    """
    if not lineas:
        lineas = ["No hay recordatorios activos para hoy."]
    ancho = max(len(l) for l in lineas)
    # Borde superior
    print("+" + "-" * (ancho + 2) + "+")
    for l in lineas:
        espacios = " " * (ancho - len(l))
        print(f"| {l}{espacios} |")
    # Borde inferior
    print("+" + "-" * (ancho + 2) + "+")


def imprimir_todos(lista):
    """
    Imprime todos los recordatorios guardados con índice, fecha, texto y días.
    """
    if not lista:
        print("No hay recordatorios guardados.")
        return
    print("Listado de todos los recordatorios:")
    for idx, rec in enumerate(lista, start=1):
        fecha = rec.get("date", "")
        texto = rec.get("text", "").strip()
        dias = rec.get("days", 0)
        print(f"[{idx}] {fecha} — {texto} (días: {dias})")


def agregar_recordatorio(lista):
    """
    Pide por terminal los datos de un recordatorio, lo valida y añade a lista.
    Luego guarda en JSON y confirma al usuario.
    """
    while True:
        fecha_str = input("Fecha del recordatorio (dd/mm/aaaa): ").strip()
        fecha = fecha_valida(fecha_str)
        if fecha:
            break
        else:
            print("♦ Formato incorrecto. Debes ingresar una fecha en formato dd/mm/aaaa.")

    while True:
        texto = input("Texto del recordatorio: ").strip()
        if texto:
            break
        else:
            print("♦ El texto no puede quedar vacío. Intenta nuevamente.")

    while True:
        dias_str = input("¿Cuántos días se mostrará? (número entero ≥ 1): ").strip()
        try:
            dias = int(dias_str)
            if dias >= 1:
                break
            else:
                print("♦ Debes ingresar un número entero mayor o igual a 1.")
        except ValueError:
            print("♦ Valor inválido. Debes ingresar un número entero.")

    nuevo = {"date": fecha_str, "text": texto, "days": dias}
    lista.append(nuevo)
    guardar_recordatorios(lista)
    print("\n✓ Recordatorio agregado correctamente.")
    input("\nPresiona Enter para continuar...")


def ver_todos(lista):
    """
    Muestra todos los recordatorios guardados y espera a que el usuario presione Enter.
    """
    clear_screen()
    print("=== TODOS LOS RECORDATORIOS ===\n")
    imprimir_todos(lista)
    input("\nPresiona Enter para volver al menú...")


def quitar_recordatorio(lista):
    """
    Muestra todos los recordatorios con índice, pide al usuario cuál eliminar
    y lo borra de la lista si es válido. Luego guarda en JSON.
    """
    if not lista:
        print("No hay recordatorios para eliminar.")
        input("\nPresiona Enter para continuar...")
        return

    clear_screen()
    print("=== ELIMINAR RECORDATORIO ===\n")
    imprimir_todos(lista)
    while True:
        idx_str = input("\nIngresa el número del recordatorio que deseas quitar (ó 0 para cancelar): ").strip()
        try:
            idx = int(idx_str)
            if idx == 0:
                print("Operación cancelada.")
                input("\nPresiona Enter para continuar...")
                return
            if 1 <= idx <= len(lista):
                rec = lista.pop(idx - 1)
                guardar_recordatorios(lista)
                print(f"\n✓ Recordatorio '{rec['date']} — {rec['text']}' eliminado.")
                input("\nPresiona Enter para continuar...")
                return
            else:
                print(f"♦ Debes ingresar un número entre 1 y {len(lista)}, o 0 para cancelar.")
        except ValueError:
            print("♦ Debes ingresar un número válido.")


def main():
    while True:
        lista = cargar_recordatorios()
        # Pantalla principal
        clear_screen()
        print("=== MENÚ DE RECORDATORIOS ===\n")
        print("1) Agregar nuevo recordatorio")
        print("2) Ver todos los recordatorios")
        print("3) Quitar un recordatorio")
        print("4) Salir\n")
        print("=== Recordatorios activos hoy ===")
        activos = obtener_recordatorios_activos(lista)
        imprimir_cuadro(activos)
        print("\nSelecciona una opción (1-4): ", end="")

        opcion = input().strip()
        if opcion == "1":
            clear_screen()
            print("=== AGREGAR RECORDATORIO ===\n")
            agregar_recordatorio(lista)
        elif opcion == "2":
            ver_todos(lista)
        elif opcion == "3":
            quitar_recordatorio(lista)
        elif opcion == "4":
            clear_screen()
            print("¡Hasta luego!")
            sys.exit(0)
        else:
            print("♦ Opción inválida. Ingresa un número entre 1 y 4.")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
