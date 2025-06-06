from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    cols = db.get_columns()
    print("Columnas disponibles:", cols)