#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime, timedelta

def leer_fecha_usuario(prompt):
    """
    Pide al usuario una fecha con el mensaje `prompt` en formato dd/mm/aaaa
    y la convierte a datetime. Repite hasta obtener una fecha válida.
    """
    while True:
        s = input(prompt).strip()
        try:
            return datetime.strptime(s, "%d/%m/%Y")
        except ValueError:
            print("Formato incorrecto. Usa dd/mm/aaaa, por ejemplo 05/12/2024.")

def leer_entero_usuario(prompt, default=0):
    """
    Pide al usuario un número entero. Si el usuario deja vacío, devuelve `default`.
    Repite hasta obtener un entero válido o vacío.
    """
    while True:
        s = input(prompt).strip()
        if s == "":
            return default
        try:
            return int(s)
        except ValueError:
            print("Por favor ingresa un número entero o deja vacío para 0.")

def main():
    ruta = "../../pacientes-diciembre-test-final.csv"
    print("=== Conteo diario de consultas con ajuste manual ===\n")
    fecha_inicio = leer_fecha_usuario("Fecha de inicio (dd/mm/aaaa): ")
    fecha_fin    = leer_fecha_usuario("Fecha de fin    (dd/mm/aaaa): ")

    # Asegurar orden correcto
    if fecha_fin < fecha_inicio:
        print("La fecha fin es anterior a la inicio; intercambiando.")
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio

    # Contar consultas por fecha
    conteo = {}
    with open(ruta, encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            try:
                fc = datetime.strptime(fila["fecha_consulta"], "%d/%m/%Y")
            except (KeyError, ValueError):
                continue
            if fecha_inicio <= fc <= fecha_fin:
                clave = fc.date()
                conteo[clave] = conteo.get(clave, 0) + 1

    # Generar lista de fechas en el rango
    dias = []
    d = fecha_inicio.date()
    while d <= fecha_fin.date():
        dias.append(d)
        d += timedelta(days=1)

    # Pedir ajuste extra por cada fecha
    extras = {}
    print("\nIntroduce un número extra para cada fecha (enter → 0):")
    for d in dias:
        fecha_str = d.strftime("%d/%m/%Y")
        c = leer_entero_usuario(f"  Extra para {fecha_str}: ")
        extras[d] = c

    # Preparar y mostrar tabla
    encabezados = ["FECHA", "DOCTOR-JUAN", "DOCTOR-FABIAN", "TOTAL"]
    filas = []
    for d in dias:
        cnt = conteo.get(d, 0)
        ext = extras.get(d, 0)
        filas.append([d.strftime("%d/%m/%Y"), str(cnt), str(ext), str(cnt + ext)])

    # Calcular anchos de columna
    anchos = [len(h) for h in encabezados]
    for fila in filas:
        for i, celda in enumerate(fila):
            anchos[i] = max(anchos[i], len(celda))

    # Imprimir encabezado
    header = " | ".join(encabezados[i].ljust(anchos[i]) for i in range(len(encabezados)))
    separator = "-+-".join("-" * anchos[i] for i in range(len(encabezados)))
    print("\n" + header)
    print(separator)

    # Imprimir filas
    for fila in filas:
        print(" | ".join(fila[i].ljust(anchos[i]) for i in range(len(fila))))

if __name__ == "__main__":
    main()
