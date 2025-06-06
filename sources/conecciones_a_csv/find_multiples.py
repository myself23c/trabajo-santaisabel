from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    cols_input = input("Ingrese los nombres de columnas separados por comas: ").strip()
    cols = [c.strip() for c in cols_input.split(',') if c.strip()]
    substr = input("Ingrese la subcadena a buscar en las columnas: ").strip()
    try:
        results = db.find_records_in_multiple_columns(cols, substr)
        print(results)
    except Exception as e:
        print(f"Error: {e}")