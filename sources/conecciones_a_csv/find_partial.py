from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    col = input("Ingrese el nombre de la columna para búsqueda parcial: ").strip()
    substr = input("Ingrese la subcadena a buscar: ").strip()
    try:
        results = db.find_records_by_partial_match(col, substr)
        print(results)
    except Exception as e:
        print(f"Error: {e}")