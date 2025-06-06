from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    col = input("Ingrese el nombre de la columna para filtrar: ").strip()
    operator = input("Ingrese operador (==, !=, >, <, >=, <=): ").strip()
    val = input("Ingrese el valor para comparar: ").strip()
    try:
        try:
            val_num = float(val)
            results = db.filter_records_by_condition(col, operator, val_num)
        except ValueError:
            results = db.filter_records_by_condition(col, operator, val)
        print(results)
    except Exception as e:
        print(f"Error: {e}")