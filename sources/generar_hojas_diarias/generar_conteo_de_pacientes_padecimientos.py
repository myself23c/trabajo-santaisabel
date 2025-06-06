#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime

def solicitar_fecha(mensaje):
    """
    Solicita al usuario una fecha en formato dd/mm/aaaa y la convierte a datetime.date.
    """
    while True:
        fecha_str = input(mensaje).strip()
        try:
            return datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            print("Formato inválido. Asegúrate de usar dd/mm/aaaa. Intenta nuevamente.\n")

def main():
    # Ruta al archivo CSV
    ruta_csv = "../../pacientes-diciembre-test-final.csv"
    
    # Solicitar fechas de inicio y fin
    print("Ingrese rango de fechas para filtrar consultas:")
    fecha_inicio = solicitar_fecha("  Fecha de inicio (dd/mm/aaaa): ")
    fecha_fin    = solicitar_fecha("  Fecha de fin    (dd/mm/aaaa): ")
    print()
    
    # Leer el CSV con pandas, asumiendo codificación UTF-8
    # NOTA: si 'fecha_consulta' viene en otro formato, pd.to_datetime con dayfirst=True lo maneja.
    try:
        df = pd.read_csv(
            ruta_csv,
            encoding="utf-8",
            dtype={
                "primera_vez_ano": str,
                "relacion_temporal": str,
                "edad": object,           # Podría venir como texto o número
                "diagnostico": str
            }
        )
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo en '{ruta_csv}'. Verifica la ruta.")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    # Convertir 'fecha_consulta' a datetime (día/mes/año)
    # Si pandas detecta automáticamente el formato correcto, no será necesario convertir manualmente,
    # pero para garantizar que se interprete como dd/mm/yyyy usamos dayfirst=True.
    try:
        df["fecha_consulta"] = pd.to_datetime(df["fecha_consulta"], dayfirst=True, errors="coerce")
    except Exception as e:
        print(f"Error convirtiendo 'fecha_consulta' a fecha: {e}")
        return

    # Eliminar filas donde la conversión a fecha dio NaT
    df = df.dropna(subset=["fecha_consulta"])

    # Filtrar por rango de fechas (inclusive)
    mask_fechas = (
        (df["fecha_consulta"].dt.date >= fecha_inicio) &
        (df["fecha_consulta"].dt.date <= fecha_fin)
    )
    df_filtrado = df.loc[mask_fechas].copy()

    # Si no hay filas en el rango, informar y salir
    if df_filtrado.empty:
        print("No se encontraron registros de 'fecha_consulta' en el rango especificado.")
        return

    # --- Conteo de 'primera_vez_ano' ("si" / "no") ---
    # Normalizamos a minúsculas para evitar discrepancias
    primera_vez_serie = df_filtrado["primera_vez_ano"].astype(str).str.lower().str.strip()
    conteo_si = (primera_vez_serie == "si").sum()
    conteo_no = (primera_vez_serie == "no").sum()

    # --- Conteo de 'relacion_temporal' ("primera-vez" / "subsecuente") ---
    rt_serie = df_filtrado["relacion_temporal"].astype(str).str.lower().str.strip()
    conteo_primera_vez = (rt_serie == "primera-vez").sum()
    conteo_subsecuente = (rt_serie == "subsecuente").sum()

    # --- Conteo de 'edad' < 11 ---
    # Convertimos a numérico y consideramos NaN como no contado
    edades = pd.to_numeric(df_filtrado["edad"], errors="coerce")
    conteo_menor_11 = (edades < 11).sum()

    # --- Conteo en 'diagnostico' por términos ---
    terminos = ["faringitis", "gastroenteritis", "amigdalitis", "bronquitis"]
    # Preparamos la serie en minúsculas para búsquedas
    diag_serie = df_filtrado["diagnostico"].astype(str).str.lower()

    conteos_diagnostico = {}
    for termino in terminos:
        # .str.contains(termino) devuelve True si aparece en cualquier parte
        conteos_diagnostico[termino] = diag_serie.str.contains(termino, na=False).sum()

    # --- Mostrar resultados en terminal ---
    print("Resultados del análisis:")
    print("------------------------")
    print(f"Total de filas en rango [{fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}]: {len(df_filtrado)}\n")

    print("1) 'primera_vez_ano':")
    print(f"   - si: {conteo_si}")
    print(f"   - no: {conteo_no}\n")

    print("2) 'relacion_temporal':")
    print(f"   - primera-vez : {conteo_primera_vez}")
    print(f"   - subsecuente : {conteo_subsecuente}\n")

    print("3) 'edad' < 11 años:")
    print(f"   - menores de 11: {conteo_menor_11}\n")

    print("4) 'diagnostico' (conteo por término):")
    for termino, cuenta in conteos_diagnostico.items():
        print(f"   - '{termino}': {cuenta}")

if __name__ == "__main__":
    main()
