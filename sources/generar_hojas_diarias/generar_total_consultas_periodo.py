#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime

def leer_fechas_usuario():
    """
    Pide al usuario una fecha en formato dd/mm/aaaa y la convierte a datetime.
    Sigue pidiendo hasta obtener un valor válido.
    """
    while True:
        fecha_str = input("Introduce una fecha(dd/mm/aaaa): ").strip()
        try:
            fecha_dt = datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha_dt
        except ValueError:
            print("Formato incorrecto. Usa dd/mm/aaaa, por ejemplo 05/12/2024.")

def contar_consultas(ruta_csv, fecha_inicio, fecha_fin):
    """
    Cuenta cuántas filas en el CSV tienen fecha_consulta entre fecha_inicio y fecha_fin (inclusive).
    """
    contador = 0
    # Abrimos explícitamente con UTF-8
    with open(ruta_csv, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            try:
                fecha_consulta = datetime.strptime(fila['fecha_consulta'], "%d/%m/%Y")
            except (ValueError, KeyError):
                # Si falla el parseo o no existe la columna, la ignoramos
                continue

            # Comprobamos si fecha_consulta está en el rango [inicio, fin]
            if fecha_inicio <= fecha_consulta <= fecha_fin:
                contador += 1

    return contador

def main():
    ruta = "../../pacientes-diciembre-test-final.csv"
    print("¿intriduce fechha inicial para comenzar a contar las consultas?")
    fecha_inicio = leer_fechas_usuario()
    print("¿Hasta qué fecha quieres contar consultas?")
    fecha_fin = leer_fechas_usuario()

    # Asegurarnos de que fecha_inicio <= fecha_fin
    if fecha_fin < fecha_inicio:
        print("La fecha fin es anterior a la fecha inicio. Intercambiando valores...")
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio

    total = contar_consultas(ruta, fecha_inicio, fecha_fin)
    print(f"\nTotal de consultas entre {fecha_inicio.strftime('%d/%m/%Y')} y {fecha_fin.strftime('%d/%m/%Y')}: >>>> {total} <<<<")

if __name__ == "__main__":
    main()
