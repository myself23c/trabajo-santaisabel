#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import unicodedata
from rapidfuzz import fuzz


def normalize_text(s: str) -> str:
    """
    Elimina tildes y convierte a minúsculas para comparación insensible a acentos.
    """
    s = unicodedata.normalize('NFD', str(s))
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    return s.lower()


def find_last_consultation(name: str, dob_str: str,
                           csv_path: str = 'pacientes-diciembre-test-final.csv') -> str:
    """
    Busca en el CSV la última consulta de un paciente cuyo nombre y fecha de nacimiento coincidan.
    Retorna una cadena formateada con cada campo en línea separada.
    Si no hay coincidencia, retorna un mensaje indicándolo.
    """
    # Carga y normalización
    df = pd.read_csv(
        csv_path,
        parse_dates=['fecha_consulta', 'fecha_de_nacimiento'],
        dayfirst=True,
        encoding='utf-8'
    )
    df['nombre_norm'] = df['nombre'].apply(normalize_text)

    # Validar y parsear fecha de nacimiento
    dob = pd.to_datetime(dob_str, dayfirst=True, errors='coerce')
    if pd.isna(dob):
        raise ValueError(f"Fecha de nacimiento inválida: {dob_str!r}")

    # Filtrar por fecha exacta
    df_dob = df[df['fecha_de_nacimiento'] == dob]
    if df_dob.empty:
        return "No se encontró ningún paciente que coincidiera con la fecha proporcionada."  

    # Fuzzy matching de nombre
    query_norm = normalize_text(name)
    df_dob = df_dob.copy()
    df_dob['score'] = df_dob['nombre_norm'].apply(lambda x: fuzz.ratio(query_norm, x))
    best = df_dob.sort_values(['score', 'fecha_consulta'], ascending=[False, False]).iloc[0]

    # Formatear resultado
    lines = ["-- Última consulta encontrada --"]
    lines.append(f"fecha_consulta       : {best['fecha_consulta'].strftime('%Y-%m-%d')}")
    lines.append(f"nombre               : {best['nombre']}")
    lines.append(f"fecha_de_nacimiento  : {best['fecha_de_nacimiento'].strftime('%Y-%m-%d')}")
    lines.append(f"curp                 : {best['curp']}")
    lines.append(f"numero_de_expediente : {best['numero_de_expediente']}")
    lines.append(f"subjetivo            : {best['subjetivo']}")
    lines.append(f"analisis             : {best['analisis']}")
    lines.append(f"diagnostico          : {best['diagnostico']}")
    lines.append(f"tratamiento          : {best['tratamiento']}")
    lines.append(f">>>alergia           : {best['alergia']}")
    lines.append("---- fin de registro ----")

    return "\n".join(lines)
