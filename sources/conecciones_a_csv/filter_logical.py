from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    expr = input("Ingrese la expresión lógica (JS-like): ").strip()
    cols_input = input("Ingrese las columnas a devolver separadas por comas (o deje vacío para todas): ").strip()
    if cols_input:
        return_cols = [c.strip() for c in cols_input.split(',') if c.strip()]
    else:
        return_cols = None
    try:
        results = db.filter_by_logical_query(expr, return_cols)
        print(results)
    except Exception as e:
        print(f"Error al filtrar con expresión lógica: {e}")