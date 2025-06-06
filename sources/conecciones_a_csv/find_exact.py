from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    col = input("Ingrese el nombre de la columna para búsqueda exacta: ").strip()
    val = input("Ingrese el valor exacto a buscar: ").strip()
    try:
        try:
            val_num = float(val)
            results = db.find_records_by_exact_match(col, val_num)
        except ValueError:
            results = db.find_records_by_exact_match(col, val)
        print(results)
    except Exception as e:
        print(f"Error: {e}")