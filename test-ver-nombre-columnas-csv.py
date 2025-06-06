import pandas as pd

# Ruta de la base de datos principal
db_file = 'dbs/nombres_unicos_limpio.csv'

try:
    # Cargar los datos del archivo CSV
    data = pd.read_csv(db_file, encoding='utf-8')
    # Mostrar las columnas presentes en el archivo
    print("Columnas presentes en el archivo CSV:")
    print(data.columns.tolist())
except Exception as e:
    print(f"Error al cargar o procesar el archivo: {e}")
