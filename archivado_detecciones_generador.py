import os
import glob
import pandas as pd
from docxtpl import DocxTemplate
from unidecode import unidecode

# --- Configuración de rutas ---
PLANTILLAS_DIR = './plantillas_generales'
OUTPUT_DOCS_DIR = './detecciones_generadas'
EXCEL_DIR = './detecciones_concentrado'
CSV_FILE = 'pacientes-diciembre-test-final.csv'
EXCEL_FILE = os.path.join(EXCEL_DIR, 'detecciones_concentrado.xlsx')

# Asegurarnos de que existan los directorios de salida
os.makedirs(OUTPUT_DOCS_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)

# --- 1. Leer y normalizar el CSV ---
df = pd.read_csv(CSV_FILE, encoding='utf-8')
df.columns = [
    unidecode(col).strip().lower().replace(' ', '_')
    for col in df.columns
]
df['id'] = df['id'].astype(str)  # Asegurar ID como cadena

print("Columnas del CSV:", df.columns.tolist())

# --- 2. Selección de IDs ---
option = input("¿Última fila (U) o lista de IDs (L)? ")
if option.upper() == 'U':
    ids = [df.iloc[-1]['id']]
elif option.upper() == 'L':
    ids = [i.strip() for i in input("IDs separados por coma: ").split(',')]
else:
    print("Opción no válida.")
    exit()

print("IDs seleccionados:", ids)
df_filtrado = df[df['id'].isin(ids)].copy()

# --- 3. Listar plantillas disponibles ---
plantillas = glob.glob(os.path.join(PLANTILLAS_DIR, '*.docx'))
plantillas_basename = [os.path.basename(p) for p in plantillas]

if not plantillas:
    print(f"No se encontraron plantillas en {PLANTILLAS_DIR}")
    exit()

print("\nPlantillas disponibles:")
for idx, nombre in enumerate(plantillas_basename, 1):
    print(f"  {idx}. {nombre}")

# Elegir plantilla
while True:
    try:
        seleccion = int(input("\nSelecciona una plantilla (número): "))
        if 1 <= seleccion <= len(plantillas):
            break
        else:
            print("Número fuera de rango.")
    except ValueError:
        print("Introduce un número válido.")

template_path = plantillas[seleccion - 1]
template_name = plantillas_basename[seleccion - 1]
print(f"Usando plantilla: {template_name}")

# Añadir columna con el nombre de la plantilla usada
df_filtrado['plantilla_usada'] = template_name

# --- 4. Generar documentos ---
for _, row in df_filtrado.iterrows():
    # Construir contexto para la plantilla
    context = {
        'nombres': row.get('nombres', ''),
        'apellido_paterno': row.get('apellido_paterno', ''),
        'apellido_materno': row.get('apellido_materno', ''),
        'edad': row.get('edad', ''),
        'sexo': row.get('sexo', ''),
        'curp': row.get('curp', ''),
        'fecha_de_nacimiento': row.get('fecha_de_nacimiento', ''),
        'lugar_de_nacimiento': row.get('lugar_de_nacimiento', ''),
        'numero_de_expediente': row.get('numero_de_expediente', ''),
        'fecha': row.get('fecha_consulta', ''),
        'hora': row.get('hora', ''),
        'peso': row.get('peso', ''),
        'talla': row.get('talla', ''),
        'tension_arterial': row.get('tension_arterial', ''),
        'fc': row.get('fc', ''),
        'fr': row.get('fr', ''),
        'temperatura': row.get('temperatura', ''),
        'dxtx': row.get('dxtx', ''),
        'imc': row.get('imc', ''),
        #'plan': row.get('plan', ''),
        #'subjetivo': row.get('subjetivo', ''),
        #'analisis': row.get('analisis', ''),
        'diagnostico': row.get('diagnostico', ''),
        #'tratamiento': row.get('tratamiento', ''),
    }

    # Renderizar y guardar docx
    doc = DocxTemplate(template_path)
    doc.render(context)
    # Construir nombre de archivo: nombre_base + plantilla para evitar sobreescrituras
    base_nombre = unidecode(f"{row.get('nombres','')}_{row['id']}").replace(' ', '_')
    plantilla_slug = unidecode(os.path.splitext(template_name)[0]).strip().replace(' ', '_')
    salida_docx = os.path.join(OUTPUT_DOCS_DIR, f"{base_nombre}_{plantilla_slug}.docx")
    doc.save(salida_docx)
    print(f"Documento creado: {salida_docx}")

# --- 5. Guardar Excel concentrado (append) ---
if os.path.exists(EXCEL_FILE):
    df_exist = pd.read_excel(EXCEL_FILE, engine='openpyxl', dtype=str)
    df_combinado = pd.concat([df_exist, df_filtrado], ignore_index=True)
    df_combinado.drop_duplicates(subset=['id', 'plantilla_usada'], inplace=True)
else:
    df_combinado = df_filtrado

df_combinado.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
print(f"\nExcel concentrado actualizado en: {EXCEL_FILE}")
