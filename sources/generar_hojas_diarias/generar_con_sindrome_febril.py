#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime

def leer_fecha_usuario(prompt):
    """
    Pide al usuario una fecha con el mensaje `prompt` en formato dd/mm/aaaa
    y la convierte a datetime. Repite hasta obtener una fecha válida.
    """
    while True:
        fecha_str = input(prompt).strip()
        try:
            return datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            print("Formato incorrecto. Usa dd/mm/aaaa, por ejemplo 05/12/2024.")

def main():
    ruta = "../../pacientes-diciembre-test-final.csv"
    print("=== Filtrar pacientes con síndrome febril por rango de fechas ===\n")
    inicio = leer_fecha_usuario("Fecha de inicio (dd/mm/aaaa): ")
    fin    = leer_fecha_usuario("Fecha de fin    (dd/mm/aaaa): ")

    # Si el usuario invirtió las fechas, las intercambiamos
    if fin < inicio:
        inicio, fin = fin, inicio

    pacientes = []
    columnas = [
        "nombre", "edad", "sexo", "curp",
        "numero_de_expediente", "fecha_consulta",
        "diagnostico", "telefono"
    ]

    # Leer y filtrar
    with open(ruta, encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Parsear y filtrar por fecha
            try:
                fecha = datetime.strptime(fila["fecha_consulta"], "%d/%m/%Y")
            except (KeyError, ValueError):
                continue
            if not (inicio <= fecha <= fin):
                continue
            # Filtrar sólo los casos con síndrome febril
            if fila.get("febril", "").strip().lower() != "sindromefebril":
                continue
            # Añadir los datos de interés
            pacientes.append({col: fila.get(col, "").strip() for col in columnas})

    if not pacientes:
        print("\nNo se encontraron pacientes con síndrome febril en ese rango de fechas.")
        return

    # Calcular ancho de cada columna
    anchos = {}
    for col in columnas:
        máximo = max(len(col), *(len(p[col]) for p in pacientes))
        anchos[col] = máximo

    # Cabecera
    cabecera = " | ".join(col.upper().ljust(anchos[col]) for col in columnas)
    separador = "-+-".join("-" * anchos[col] for col in columnas)
    print("\n" + cabecera)
    print(separador)

    # Filas de datos
    for p in pacientes:
        fila_fmt = " | ".join(p[col].ljust(anchos[col]) for col in columnas)
        print(fila_fmt)

    print(f"\nTotal de pacientes con síndrome febril: {len(pacientes)}")

if __name__ == "__main__":
    main()
