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
    print("=== Resumen de condiciones por fecha, sexo y edad ===\n")
    inicio = leer_fecha_usuario("Fecha de inicio (dd/mm/aaaa): ")
    fin    = leer_fecha_usuario("Fecha de fin    (dd/mm/aaaa): ")

    # Asegurar orden correcto de fechas
    if fin < inicio:
        print("La fecha fin es anterior a la inicio; intercambiando valores.")
        inicio, fin = fin, inicio

    # Columnas a evaluar
    condiciones = ["dm2", "has", "ira", "asma", "conjuntivitis", "otitis" , "eda"]

    # Inicializar resultados
    resultados = {
        cond: {"total": 0, "detalles": []}
        for cond in condiciones
    }

    # Leer CSV y acumular datos
    with open(ruta, encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Parsear y filtrar por fecha_consulta
            try:
                fecha = datetime.strptime(fila["fecha_consulta"], "%d/%m/%Y")
            except (KeyError, ValueError):
                continue
            if not (inicio <= fecha <= fin):
                continue

            # Para cada condición, contar 'si' y registrar sexo+edad
            for cond in condiciones:
                if fila.get(cond, "").strip().lower() == "si":
                    resultados[cond]["total"] += 1
                    # Obtener sexo
                    sexo = fila.get("sexo", "").strip().upper()
                    sexo = sexo if sexo in ("H", "M") else "?"
                    # Obtener edad
                    try:
                        edad = int(fila.get("edad", "").strip())
                    except ValueError:
                        edad = "?"
                    resultados[cond]["detalles"].append(f"{sexo}{edad}")

    # Preparar tabla
    print("El valor de M = es igual a mujer y el de H = hombre, ej M34 seria mujer 34 años")
    encabezados = ["CONDICIÓN", "TOTAL", "DETALLES (sexo+edad)"]
    filas = []
    total_general = 0
    for cond in condiciones:
        total = resultados[cond]["total"]
        detalles = resultados[cond]["detalles"]
        detalles_str = ", ".join(detalles) if detalles else "-"
        filas.append([cond.upper(), str(total), detalles_str])
        total_general += total

    # Fila de total general
    filas.append(["TOTAL GENERAL", str(total_general), "-"])

    # Calcular ancho de cada columna
    anchos = [len(encabezados[i]) for i in range(len(encabezados))]
    for fila in filas:
        for i, celda in enumerate(fila):
            anchos[i] = max(anchos[i], len(celda))

    # Imprimir encabezado
    header_line = " | ".join(encabezados[i].ljust(anchos[i]) for i in range(len(encabezados)))
    separator  = "-+-".join("-" * anchos[i] for i in range(len(encabezados)))
    print("\n" + header_line)
    print(separator)

    # Imprimir filas
    for fila in filas:
        print(" | ".join(fila[i].ljust(anchos[i]) for i in range(len(fila))))

if __name__ == "__main__":
    main()
