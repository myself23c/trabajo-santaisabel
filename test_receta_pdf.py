import os
import pandas as pd
from odf.opendocument import load
from odf.text import P
from unidecode import unidecode

# 0. Crear carpeta de salida si no existe
os.makedirs('notas_medicas', exist_ok=True)

# 1. Leer el CSV
df = pd.read_csv('pacientes-diciembre-test-final.csv', encoding='utf-8')

# 2. Normalizar nombres de columna
df.columns = [
    unidecode(col).strip().lower().replace(' ', '_')
    for col in df.columns
]
print("Columnas del CSV:", df.columns.tolist())

# 3. Asegurar que 'id' sea cadena
df['id'] = df['id'].astype(str)

# 4. Selección de IDs
option = input("Última fila (U) o lista de IDs (L)? ")
if option.upper() == 'U':
    ids = [df.iloc[-1]['id']]
elif option.upper() == 'L':
    ids = [s.strip() for s in input("IDs separados por coma: ").split(',')]
else:
    print("Opción no válida")
    exit()

print("IDs seleccionados:", ids)
df_filtered = df[df['id'].isin(ids)]
print("Filtrado:", df_filtered)

# 5. Ruta de la plantilla ODT
template_path = 'plantillas/receta_plantilla.odt'

# 6. Función para reemplazo de texto
def replace_text_in_element(element, replacements):
    if element.tagName in ('text:p', 'text:span'):
        for key, value in replacements.items():
            for child in element.childNodes:
                if child.nodeType == child.TEXT_NODE and f'{{{{{key}}}}}' in child.data:
                    child.data = child.data.replace(f'{{{{{key}}}}}', str(value))
    for child in element.childNodes:
        replace_text_in_element(child, replacements)

# 7. Generación de documentos
for _, row in df_filtered.iterrows():
    # Contexto para plantilla
    context = {
        'nombre':        row.get('nombre', 'vacío'),
        'edad':          row.get('edad', 'vacío'),
        'sexo':          row.get('sexo', 'vacío'),
        'lugar_de_nacimiento':   row.get('lugar_de_nacimiento', 'vacío'),
        'fecha_de_nacimiento':   row.get('fecha_de_nacimiento', 'vacío'),
        'curp':          row.get('curp', 'vacío'),
        'numero_de_expediente':  row.get('numero_de_expediente', 'vacío'),
        'fecha':         row.get('fecha_consulta', 'vacío'),
        'diagnostico':   row.get('diagnostico', 'vacío'),
        # añade más campos acá si tu plantilla los usa
    }

    # Cargar y reemplazar
    doc = load(template_path)
    for p in doc.getElementsByType(P):
        replace_text_in_element(p, context)

    # Generar nombre de archivo: solo nombre + id
    nombre_sin_acentos = unidecode(str(row.get('nombre', '')))
    safe_nombre = nombre_sin_acentos.strip().replace(' ', '_')
    output_path = f"notas_medicas/receta-{safe_nombre}_{row['id']}.odt"

    doc.save(output_path)
    print(f"Documento creado: {output_path}")
