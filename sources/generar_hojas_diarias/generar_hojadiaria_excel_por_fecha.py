#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
import os
from datetime import datetime

def main():
    # Pedir al usuario el nombre del archivo de salida (sin extensión)
    filename = input("Ingrese el nombre del archivo Excel a generar (sin extensión): ").strip()
    if not filename:
        print("Nombre de archivo inválido.")
        return

    # Pedir fecha de inicio y fecha de fin
    fecha_inicio_str = input("Ingrese la fecha de inicio (dd/mm/aaaa): ").strip()
    fecha_fin_str = input("Ingrese la fecha de fin (dd/mm/aaaa): ").strip()
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha inválido. Use dd/mm/aaaa.")
        return
    if fecha_inicio > fecha_fin:
        print("La fecha de inicio no puede ser posterior a la fecha de fin.")
        return

    # Determinar la ruta al Escritorio del usuario actual
    home = Path.home()
    desktop = home / 'Escritorio'
    if not desktop.exists():
        desktop = home / 'Desktop'
    output_path = desktop / f"{filename}.xlsx"

    # Ruta relativa al CSV de entrada
    script_dir = Path(__file__).resolve().parent
    csv_path = (script_dir / '..' / '..' / 'pacientes-diciembre-test-final.csv').resolve()

    # Leer el archivo CSV con codificación UTF-8
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return

    # Convertir 'fecha_consulta' a datetime y filtrar por rango
    if 'fecha_consulta' not in df.columns:
        print("La columna 'fecha_consulta' no se encuentra en el CSV.")
        return
    df['fecha_consulta'] = pd.to_datetime(df['fecha_consulta'], dayfirst=True, errors='coerce')
    mask = (df['fecha_consulta'] >= fecha_inicio) & (df['fecha_consulta'] <= fecha_fin)
    df = df.loc[mask]

    # Lista de columnas a extraer
    cols = [
        'ID', 'nombre', 'nombres', 'apellido_paterno', 'apellido_materno',
        'edad', 'sexo', 'lugar_de_nacimiento', 'fecha_de_nacimiento', 'curp',
        'numero_de_expediente', 'fecha_consulta', 'hora', 'peso', 'talla',
        'tension_arterial', 'fc', 'fr', 'temperatura', 'dxtx', 'imc',
        'diagnostico', 'primera_vez_ano', 'relacion_temporal', 'dm2', 'has',
        'ira', 'asma', 'conjuntivitis', 'otitis', 'deteccion_salud_mental',
        'folio_receta', 'promocion_de_la_salud', 'linea_vida', 'esquema_vacunacion',
        'referido', 'deteccion_adicciones', 'deteccion_violencia_mujer',
        'prueba_edi', 'resultado_edi', 'resultado_battelle', 'eda_tratamiento',
        'ira_tratamiento', 'aplicacion_cedula_cancer_ano',
        'INTERVENCIONES GERONTOLOGICAS', 'alergia', 'CHISME', 'telefono',
        'febril', 'embarazada'
    ]

    # Verificar columnas faltantes
    missing = [c for c in cols if c not in df.columns]
    if missing:
        print("Las siguientes columnas no se encontraron en el CSV:", missing)

    # Seleccionar solo las columnas existentes
    available_cols = [c for c in cols if c in df.columns]
    df_sel = df[available_cols]

    # Exportar a Excel
    try:
        df_sel.to_excel(output_path, index=False)
        print(f"Archivo Excel guardado en: {output_path}")
    except Exception as e:
        print(f"Error al escribir el archivo Excel: {e}")


if __name__ == '__main__':
    main()
