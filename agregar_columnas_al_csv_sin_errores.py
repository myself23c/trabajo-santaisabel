import csv
import os

# Ruta del archivo original
archivo_original = 'pacientes-diciembre-test-final.csv'

# Preguntar al usuario si desea agregar una columna
respuesta = input("¿Quieres agregar una nueva columna? (s/n): ").strip().lower()

if respuesta != 's':
    print("No se agregará ninguna columna.")
    exit()

# Obtener el nombre de la nueva columna
nueva_columna = input("Escribe el nombre de la nueva columna: ").strip()

# Crear el nombre del nuevo archivo
archivo_nuevo = f'con_{nueva_columna}_{archivo_original}'

# Leer los datos del archivo original
with open(archivo_original, 'r', newline='', encoding='utf-8') as archivo_entrada:
    lector = csv.DictReader(archivo_entrada)
    filas = list(lector)
    encabezados = lector.fieldnames.copy()

# Verificar si la columna ya existe
if nueva_columna in encabezados:
    print(f"La columna '{nueva_columna}' ya existe en el archivo.")
    exit()

# Agregar la nueva columna al final de los encabezados
encabezados.append(nueva_columna)

# Agregar 'nulo' en la nueva columna para cada fila existente
for fila in filas:
    fila[nueva_columna] = 'nulo'

# Escribir los datos en un nuevo archivo CSV
with open(archivo_nuevo, 'w', newline='', encoding='utf-8') as archivo_salida:
    escritor = csv.DictWriter(archivo_salida, fieldnames=encabezados)
    escritor.writeheader()
    escritor.writerows(filas)

print(f"Nueva columna '{nueva_columna}' agregada exitosamente.")
print(f"Archivo creado: {archivo_nuevo}")

