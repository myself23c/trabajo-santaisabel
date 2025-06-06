from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    col = input("Ingrese el nombre de la columna para valores únicos: ").strip()
    try:
        unique_vals = db.get_unique_values(col)
        print(f"Valores únicos en '{col}': {unique_vals}")
    except Exception as e:
        print(f"Error: {e}")