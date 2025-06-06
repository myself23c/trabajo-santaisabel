from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    total = db.count_records()
    print(f"Número total de registros: {total}")