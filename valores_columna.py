import csv

# Ruta del archivo CSV
archivo_csv = 'pacientes-diciembre-test-final.csv'

# Leer y mostrar los valores de la columna 'sexo'
valores_sexo = []

with open(archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    
    if 'sexo' not in lector.fieldnames:
        print("La columna 'sexo' no existe en el archivo.")
    else:
        for fila in lector:
            valores_sexo.append(fila['febril'])

# Mostrar los resultados
print("Valores en la columna 'sexo':")
for i, valor in enumerate(valores_sexo, 1):
    print(f"{i}. {valor if valor.strip() else '(vacío)'}")
