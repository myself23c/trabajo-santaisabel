#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime, timedelta

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

def generar_dias_laborables_inicio_fin(fecha_inicio, fecha_fin):
    """
    Genera una lista de fechas (tipo datetime.date) entre fecha_inicio y fecha_fin (inclusive)
    que correspondan a días de lunes a viernes.
    """
    dias = []
    actual = fecha_inicio
    while actual <= fecha_fin:
        if actual.weekday() < 5:  # 0=Lunes, 4=Viernes
            dias.append(actual)
        actual += timedelta(days=1)
    return dias

def main():
    # Ruta al archivo CSV
    ruta_csv = "../../pacientes-diciembre-test-final.csv"
    
    # Solicitar fechas de inicio y fin
    print("Ingrese rango de fechas para filtrar consultas:")
    fecha_inicio = solicitar_fecha("  Fecha de inicio (dd/mm/aaaa): ")
    fecha_fin    = solicitar_fecha("  Fecha de fin    (dd/mm/aaaa): ")
    print()
    
    # Leer el CSV con pandas, asumiendo codificación UTF-8
    try:
        df = pd.read_csv(
            ruta_csv,
            encoding="utf-8",
            dtype={"fecha_consulta": str}
        )
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo en '{ruta_csv}'. Verifica la ruta.")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    # Convertir 'fecha_consulta' a datetime (día/mes/año), errores -> NaT
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

    # Generar lista de días laborables en el rango completo
    dias_laborables = generar_dias_laborables_inicio_fin(fecha_inicio, fecha_fin)

    # Agrupar el dataframe filtrado por fecha (solo la parte date)
    # y obtener conteo de cuántas consultas hay por cada fecha exacta
    # Esto devuelve un Series donde el índice es datetime.date y el valor es la cantidad
    conteo_por_fecha = df_filtrado["fecha_consulta"].dt.date.value_counts().to_dict()

    # Mostrar resultados:
    print(f"Conteo de consultas por día (solo Lunes a Viernes) entre {fecha_inicio.strftime('%d/%m/%Y')} y {fecha_fin.strftime('%d/%m/%Y')}:")
    print("-------------------------------------------------------------------------------")
    for dia in dias_laborables:
        cantidad = conteo_por_fecha.get(dia, 0)
        print(f"{dia.strftime('%d/%m/%Y')}: {cantidad} consulta{'s' if cantidad != 1 else ''}")

    # Mostrar las fechas laborables sin ninguna consulta (cantidad == 0)
    faltantes = [dia for dia in dias_laborables if conteo_por_fecha.get(dia, 0) == 0]
    if faltantes:
        print("\nFechas laborables sin consultas registradas:")
        for dia in faltantes:
            print(f"  - {dia.strftime('%d/%m/%Y')}")
    else:
        print("\nNo faltan fechas laborables: todas tienen al menos una consulta.")

if __name__ == "__main__":
    main()
