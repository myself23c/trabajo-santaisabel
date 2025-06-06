from csv_middleware import CSVMiddleware

def run(db: CSVMiddleware):
    idx = input("Ingrese el índice de la fila: ").strip()
    if idx.isdigit():
        record = db.get_record_by_index(int(idx))
        if record is not None:
            print(record)
        else:
            print("Índice fuera de rango.")
    else:
        print("Índice inválido. Debe ser un número entero.")