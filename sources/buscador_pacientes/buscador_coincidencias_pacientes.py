#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import unicodedata
import json
import re

def normalize_text(s: str) -> str:
    """
    Elimina tildes y convierte a minúsculas para comparación insensible a acentos.
    """
    s = unicodedata.normalize('NFD', str(s))
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    return s.lower()

def main():
    # 1. Cargar CSV y parsear fechas en formato dd/mm/aaaa
    df = pd.read_csv(
        '../../pacientes-diciembre-test-final.csv',
        parse_dates=['fecha_consulta', 'fecha_de_nacimiento'],
        dayfirst=True,
        encoding='utf-8'
    )

    # 2. Normalizar columnas de texto para búsqueda
    text_cols = ['plan', 'subjetivo', 'analisis', 'diagnostico', 'tratamiento', 'pronostico']
    for col in text_cols:
        df[f'{col}_norm'] = df[col].apply(normalize_text)

    # 3. Leer palabras clave del usuario
    raw = input('Ingrese palabra(s) clave separadas por comas o espacios: ').strip()
    # separar por comas, puntos y comas o espacios
    keywords = [normalize_text(k) for k in re.split(r'[,;\s]+', raw) if k]

    if not keywords:
        print("No se ingresaron palabras clave. Saliendo.")
        return

    # 4. Filtrar filas que contengan al menos una de las keywords en cualquiera de las columnas
    mask = pd.Series(False, index=df.index)
    for kw in keywords:
        # en cada columna "norm" comprobamos si aparece la kw
        m = False
        for col in text_cols:
            m = m | df[f'{col}_norm'].str.contains(kw, na=False)
        mask = mask | m

    df_res = df[mask].sort_values('fecha_consulta', ascending=False)

    # 5. Construir lista de dicts para JSON (incluye plan y pronostico)
    output = []
    for _, row in df_res.iterrows():
        output.append({
            "fecha_consulta": row['fecha_consulta'].strftime('%Y-%m-%d') if pd.notna(row['fecha_consulta']) else None,
            "nombre": row['nombre'],
            "edad": int(row['edad']) if pd.notna(row['edad']) else None,
            "sexo": row['sexo'],
            "fecha_de_nacimiento": row['fecha_de_nacimiento'].strftime('%Y-%m-%d') if pd.notna(row['fecha_de_nacimiento']) else None,
            "curp": row['curp'],
            "tension_arterial": row['tension_arterial'],
            "dxtx": row['dxtx'],
            "plan": row['plan'],
            "subjetivo": row['subjetivo'],
            "analisis": row['analisis'],
            "diagnostico": row['diagnostico'],
            "tratamiento": row['tratamiento'],
            
            "pronostico": row['pronostico']
        })

    # 6. Serializar a JSON
    json_str = json.dumps(output, ensure_ascii=False, indent=2)

    # 7. Mostrar por terminal
    print(json_str)
    print(">>> se genero un archivo llamado >>> coincidencias.txt <<< con los datos matcheados.")

    # 8. Guardar en archivo .txt
    with open('coincidencias.txt', 'w', encoding='utf-8') as f:
        f.write(json_str)

if __name__ == '__main__':
    main()
