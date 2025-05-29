import pandas as pd
from odf.opendocument import load
from odf.text import P, Span
from unidecode import unidecode

# Leer el archivo CSV con encoding latin1
df = pd.read_csv('pacientes-diciembre-test-final.csv', encoding='utf-8')

# Normalizar los nombres de las columnas
df.columns = [unidecode(col).strip().lower() for col in df.columns]

# Imprimir los nombres de las columnas para verificar
print("Columnas del CSV:", df.columns)

# Renombrar manualmente las columnas con caracteres extraños


# Asegurarse de que la columna 'id' es de tipo cadena
df['id'] = df['id'].astype(str)

# Preguntar al usuario si desea crear un archivo para la última fila o para una lista de IDs específicos
option = input("Desea crear un archivo para la última fila (U) o para una lista de IDs específicos (L)? ")

if option.upper() == 'U':
    ids = [str(df.iloc[-1]['id'])]
elif option.upper() == 'L':
    ids_input = input("Ingrese la lista de IDs separados por comas: ")
    ids = [id.strip() for id in ids_input.split(',')]
else:
    print("Opción no válida")
    exit()

# Imprimir los IDs seleccionados
print("IDs seleccionados:", ids)

# Filtrar el DataFrame para obtener solo las filas con los IDs especificados
df_filtered = df[df['id'].isin(ids)]

# Verificar el filtrado
print("Filtrado del DataFrame:", df_filtered)

# Ruta a la plantilla de ODT
template_path = 'plantillas/receta_plantilla.odt'

# Función para reemplazar texto en nodos
def replace_text_in_element(element, replacements):
    if element.tagName in ('text:p', 'text:span'):
        for key, value in replacements.items():
            for child in element.childNodes:
                if child.nodeType == child.TEXT_NODE and f'{{{{{key}}}}}' in child.data:
                    child.data = child.data.replace(f'{{{{{key}}}}}', str(value))
    for child in element.childNodes:
        replace_text_in_element(child, replacements)

# Crear documentos para cada fila filtrada
for index, row in df_filtered.iterrows():
    context = {
        'nombre': row['nombre'] if 'nombre:' in row and pd.notna(row['nombre:']) else 'vacio',
        'edad': row['edad'] if 'edad:' in row and pd.notna(row['edad:']) else 'vacio',
        'sexo': row['sexo'] if 'sexo:' in row and pd.notna(row['sexo:']) else 'vacio',
        'lugar_de_nacimiento': row['lugar de nacimiento:'] if 'lugar de nacimiento:' in row and pd.notna(row['lugar de nacimiento:']) else 'vacio',
        'fecha_de_nacimiento': row['fecha de nacimiento:'] if 'fecha de nacimiento:' in row and pd.notna(row['fecha de nacimiento:']) else 'vacio',
        'curp': row['curp:'] if 'curp:' in row and pd.notna(row['curp:']) else 'vacio',
        'numero_de_expediente': row['numero_de_expediente'] if 'n. de expediente:' in row and pd.notna(row['n. de expediente:']) else 'vacio',
        'fecha': row['fecha'] if 'fecha:' in row and pd.notna(row['fecha:']) else 'vacio',
        'diagnostico': row['diagnostico'] if 'diagnostico:' in row and pd.notna(row['diagnostico:']) else 'vacio',
        'n_de_expediente': row['n. de expediente:'] if 'n. de expediente:' in row and pd.notna(row['n. de expediente:']) else 'vacio'
    }

    # Cargar la plantilla
    doc = load(template_path)

    # Reemplazar las variables en el texto del documento
    for paragraph in doc.getElementsByType(P):
        replace_text_in_element(paragraph, context)

    # Asegurarse de que el nombre sea una cadena
    nombre = row['nombre'] if 'nombre' in row and pd.notna(row['nombre']) else 'vacio'
    nombre = str(nombre)
    nombre = unidecode(nombre)
    output_path = f"notas_medicas/receta-{nombre.replace(' ', '_')}_{row['id']}.odt"
    doc.save(output_path)
    print(f"Documento creado: {output_path}")
