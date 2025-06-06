#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime

CSV_FILE = 'pacientes-diciembre-test-final.csv'
DATE_FORMAT = '%d/%m/%Y'

def parse_date(s: str) -> datetime.date:
    """Convierte una cadena dd/mm/aaaa en un objeto date."""
    return datetime.strptime(s, DATE_FORMAT).date()

def prompt_date(prompt: str) -> datetime.date:
    """Pide al usuario una fecha hasta que sea válida."""
    while True:
        s = input(prompt).strip()
        try:
            return parse_date(s)
        except ValueError:
            print("❌ Fecha inválida. Usa el formato dd/mm/aaaa.")

def build_table(rows, headers):
    # Calcular ancho de cada columna
    widths = []
    for h in headers:
        max_data = max((len(str(r[h])) for r in rows), default=0)
        widths.append(max(len(h), max_data))
    # Línea de separación completa
    sep = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'
    # Fila de encabezado
    header_row = '|' + '|'.join(f' {h.ljust(w)} ' for h, w in zip(headers, widths)) + '|'

    lines = [sep, header_row, sep]
    # Agregar cada fila de datos seguida de sep
    for r in rows:
        row = '|' + '|'.join(f' {str(r[h]).ljust(w)} ' for h, w in zip(headers, widths)) + '|'
        lines.append(row)
        lines.append(sep)

    return '\n'.join(lines)

def main():
    print("=== Filtrar pacientes por fecha de consulta ===")
    fecha_inicial = prompt_date("Fecha inicial (dd/mm/aaaa): ")
    fecha_final   = prompt_date("Fecha final   (dd/mm/aaaa): ")

    if fecha_final < fecha_inicial:
        print("❌ La fecha final debe ser igual o posterior a la inicial.")
        return

    headers = ["ID", "nombre", "fecha_consulta", "edad","sexo"]
    resultados = []

    # Leer y filtrar el CSV
    with open(CSV_FILE, encoding='utf-8', newline='') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            try:
                fc = parse_date(fila['fecha_consulta'])
            except (KeyError, ValueError):
                continue
            if fecha_inicial <= fc <= fecha_final:
                resultados.append({h: fila.get(h, '') for h in headers})

    if not resultados:
        print("⚠️  No se encontraron registros en el rango especificado.")
    else:
        tabla = build_table(resultados, headers)
        print("\n" + tabla)

if __name__ == '__main__':
    main()
