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


def leer_rango_edad():
    """
    Pide al usuario un rango de edad mínimo y máximo (enteros entre 0 y 200).
    Repite hasta obtener valores válidos y asegura min <= max.
    """
    while True:
        try:
            edad_min = int(input("Edad mínima (0–200): ").strip())
            edad_max = int(input("Edad máxima (0–200): ").strip())
        except ValueError:
            print("Por favor, ingresa números enteros válidos.")
            continue
        if not (0 <= edad_min <= 200 and 0 <= edad_max <= 200):
            print("Las edades deben estar entre 0 y 200.")
            continue
        if edad_max < edad_min:
            print("La edad máxima es menor que la mínima; intercambiando valores.")
            edad_min, edad_max = edad_max, edad_min
        return edad_min, edad_max


def main():
    ruta = "../../pacientes-diciembre-test-final.csv"
    print("=== Filtrar pacientes por fechas y edad ===\n")

    inicio = leer_fecha_usuario("Fecha de inicio (dd/mm/aaaa): ")
    fin    = leer_fecha_usuario("Fecha de fin    (dd/mm/aaaa): ")
    if fin < inicio:
        print("La fecha fin es anterior a la inicio; intercambiando.")
        inicio, fin = fin, inicio

    edad_min, edad_max = leer_rango_edad()

    pacientes = []
    columnas = [
        "nombre", "edad", "sexo", "curp",
        "numero_de_expediente", "fecha_consulta",
        "diagnostico", "telefono", "nutricion"
    ]

    # Leer y filtrar pacientes
    with open(ruta, encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Fecha
            try:
                fecha = datetime.strptime(fila.get("fecha_consulta", ""), "%d/%m/%Y")
            except ValueError:
                continue
            if not (inicio <= fecha <= fin):
                continue

            # Edad
            try:
                edad = int(fila.get("edad", "").strip())
            except ValueError:
                continue
            if not (edad_min <= edad <= edad_max):
                continue

            # Construir registro completo
            registro = {col: fila.get(col, "").strip() for col in columnas}
            pacientes.append(registro)

    if not pacientes:
        print("\nNo se encontraron pacientes que cumplan esos criterios.")
        return

    # Calcular anchos para la tabla
    anchos = {}
    for col in columnas:
        anchos[col] = max(len(col), *(len(p[col]) for p in pacientes))

    # Imprimir cabecera de tabla
    cabecera = " | ".join(col.upper().ljust(anchos[col]) for col in columnas)
    separador = "-+-".join("-" * anchos[col] for col in columnas)
    print("\n" + cabecera)
    print(separador)

    # Imprimir filas de pacientes
    for p in pacientes:
        fila_fmt = " | ".join(p[col].ljust(anchos[col]) for col in columnas)
        print(fila_fmt)

    print(f"\nTotal de pacientes encontrados: {len(pacientes)}")

    # Contar totales por categoría de nutrición
    categorias = ['desnutricion', 'bajo-peso', 'peso-normal', 'sobrepeso', 'obesidad']
    conteo = {cat: 0 for cat in categorias}
    for p in pacientes:
        cat = p.get('nutricion', '').lower()
        if cat in conteo:
            conteo[cat] += 1
        else:
            conteo[cat] = conteo.get(cat, 0) + 1

    print("\nResumen de pacientes por categoría de nutrición:")
    for cat in categorias:
        etiqueta = cat.replace('-', ' ').capitalize()
        print(f"{etiqueta}: {conteo.get(cat, 0)}")

if __name__ == "__main__":
    main()
