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
df['id'] = df['id'].astype(str)

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

print("\nDetecciones que hay disponibles:")
for idx, nombre in enumerate(plantillas_basename, 1):
    print(f"  {idx}. {nombre}")

# Ahora permitimos seleccionar varias plantillas separando por coma
seleccion_raw = input("\nSelecciona las plantillas (números separados por coma): ")
try:
    # Parsear los números y validarlos
    indices = [int(x.strip()) for x in seleccion_raw.split(',') if x.strip().isdigit()]
    if not indices:
        print("No ingresaste ningún número válido.")
        exit()
    for i in indices:
        if i < 1 or i > len(plantillas):
            print(f"El número {i} está fuera de rango.")
            exit()
except ValueError:
    print("Introduce números válidos separados por coma.")
    exit()

# Construir lista de plantillas seleccionadas
selected_templates = []
for i in indices:
    template_path = plantillas[i - 1]
    template_name = plantillas_basename[i - 1]
    selected_templates.append((template_path, template_name))

print("\nPlantillas seleccionadas:")
for _, nombre in selected_templates:
    print(f"  - {nombre}")

# --- 4. Generar documentos y recolectar datos para Excel ---
registros = []
for template_path, template_name in selected_templates:
    plantilla_slug = unidecode(os.path.splitext(template_name)[0]).replace(' ', '_')
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
            'fecha': row.get('fecha_consulta', ''),  # mapeo de csv a plantilla
            'hora': row.get('hora', ''),
            'peso': row.get('peso', ''),
            'talla': row.get('talla', ''),
            'tension_arterial': row.get('tension_arterial', ''),
            'fc': row.get('fc', ''),
            'fr': row.get('fr', ''),
            'temperatura': row.get('temperatura', ''),
            'dxtx': row.get('dxtx', ''),
            'imc': row.get('imc', ''),
            # 'plan': row.get('plan', ''),
            # 'subjetivo': row.get('subjetivo', ''),
            # 'analisis': row.get('analisis', ''),
            'diagnostico': row.get('diagnostico', ''),
            # 'tratamiento': row.get('tratamiento', ''),
        }
        
        # Renderizar y guardar docx
        doc = DocxTemplate(template_path)
        doc.render(context)
        
        base_nombre = unidecode(f"{row.get('nombre','')}_{row['id']}").replace(' ', '_')
        salida_docx = os.path.join(
            OUTPUT_DOCS_DIR,
            f"{base_nombre}_{plantilla_slug}.docx"
        )
        doc.save(salida_docx)
        print(f"Documento creado: {salida_docx}")
        
        # Agregar registro al listado para Excel
        record = context.copy()
        record['plantilla_usada'] = template_name
        registros.append(record)

# --- 5. Guardar Excel concentrado (append) usando solo registros ---
df_para_excel = pd.DataFrame(registros)
if os.path.exists(EXCEL_FILE):
    df_exist = pd.read_excel(EXCEL_FILE, engine='openpyxl', dtype=str)
    df_comb = pd.concat([df_exist, df_para_excel], ignore_index=True)
    df_comb.drop_duplicates(subset=['numero_de_expediente', 'plantilla_usada'], inplace=True)
else:
    df_comb = df_para_excel

df_comb.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
print(f"\nExcel concentrado actualizado en: {EXCEL_FILE}")
