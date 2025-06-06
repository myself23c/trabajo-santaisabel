#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import unicodedata
import json
from rapidfuzz import process, fuzz

def normalize_text(s: str) -> str:
    """
    Elimina tildes y convierte a minúsculas para comparación insensible a acentos.
    """
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    return s.lower()

def main():
    # 1. Cargar el CSV y parsear fechas (ambas en formato dd/mm/aaaa)
    df = pd.read_csv(
        '../../pacientes-diciembre-test-final.csv',
        parse_dates=['fecha_consulta', 'fecha_de_nacimiento'],
        dayfirst=True,
        encoding='utf-8'
    )

    # 2. Añadir columna normalizada para comparar sin acentos
    df['nombre_norm'] = df['nombre'].astype(str).apply(normalize_text)

    # 3. Pedir al usuario el nombre a buscar
    query = input('Ingrese el nombre a buscar: ').strip()
    query_norm = normalize_text(query)

    # 4. Construir dict índice→nombre_norm para RapidFuzz
    choices = df['nombre_norm'].to_dict()

    # 5. Buscar coincidencias con puntaje >= 94%
    matches = process.extract(
        query_norm,
        choices,
        scorer=fuzz.ratio,
        score_cutoff=94,
        limit=None
    )

    if not matches:
        print(json.dumps([], ensure_ascii=False, indent=2))
        return

    # 6. Obtener índices coincidentes y ordenar por fecha_consulta desc
    matched_idxs = [idx for (_n, _s, idx) in matches]
    df_res = df.loc[matched_idxs].sort_values('fecha_consulta', ascending=False)

    # 7. Seleccionar y formatear columnas
    output = []
    for _, row in df_res.iterrows():
        output.append({
            "fecha_consulta": row['fecha_consulta'].strftime('%Y-%m-%d'),
            "nombre": row['nombre'],
            "edad": int(row['edad']) if not pd.isna(row['edad']) else None,
            "sexo": row['sexo'],
            "fecha_de_nacimiento": row['fecha_de_nacimiento'].strftime('%Y-%m-%d'),
            "curp": row['curp'],
            "tension_arterial": row['tension_arterial'],
            "dxtx": row['dxtx'],
            "subjetivo": row['subjetivo'],
            "analisis": row['analisis'],
            "diagnostico": row['diagnostico'],
            "tratamiento": row['tratamiento']
        })

    # 8. Imprimir JSON con indentación
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
