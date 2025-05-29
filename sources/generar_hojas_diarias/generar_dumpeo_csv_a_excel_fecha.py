#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime

def leer_fecha_usuario(prompt):
    """
    Pide al usuario una fecha con el mensaje `prompt` en formato dd/mm/aaaa
    y la convierte a datetime.date. Repite hasta obtener una fecha válida.
    """
    while True:
        s = input(prompt).strip()
        try:
            return datetime.strptime(s, "%d/%m/%Y").date()
        except ValueError:
            print("Formato incorrecto. Usa dd/mm/aaaa, por ejemplo 05/12/2024.")

def main():
    ruta_csv = "../../pacientes-diciembre-test-final.csv"
    print("=== Extraer rango de fechas a Excel ===\n")

    # Pedir rango de fechas
    fecha_ini = leer_fecha_usuario("Fecha de inicio (dd/mm/aaaa): ")
    fecha_fin = leer_fecha_usuario("Fecha de fin    (dd/mm/aaaa): ")
    if fecha_fin < fecha_ini:
        print("La fecha fin es anterior a la inicio; intercambiando valores.")
        fecha_ini, fecha_fin = fecha_fin, fecha_ini

    # Pedir nombre de archivo de salida
    nombre = input("Nombre del archivo de salida (sin extensión): ").strip()
    if not nombre:
        print("Nombre inválido. Abortando.")
        return
    archivo_salida = f"{nombre}.xlsx"

    # Leer CSV con pandas
    df = pd.read_csv(
        ruta_csv,
        encoding="utf-8",
        dtype=str,  # leer todo como texto para evitar errores
        sep=","
    )

    # Convertir y filtrar por fecha_consulta
    df["fecha_consulta"] = pd.to_datetime(
        df["fecha_consulta"],
        format="%d/%m/%Y",
        dayfirst=True,
        errors="coerce"
    )
    df_filtrado = df[
        (df["fecha_consulta"].dt.date >= fecha_ini) &
        (df["fecha_consulta"].dt.date <= fecha_fin)
    ].copy()

    if df_filtrado.empty:
        print("\nNo se encontraron filas en ese rango de fechas.")
        return

    # Guardar a Excel
    df_filtrado.to_excel(archivo_salida, index=False)
    print(f"\nArchivo '{archivo_salida}' creado con {len(df_filtrado)} filas.")

if __name__ == "__main__":
    main()
