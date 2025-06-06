from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    df = db.get_all_records()
    print(df)