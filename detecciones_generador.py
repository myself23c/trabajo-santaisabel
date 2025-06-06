import os
import glob
import pandas as pd
import re
from docxtpl import DocxTemplate
from unidecode import unidecode

# --- Configuración de rutas ---
PLANTILLAS_DIR = './plantillas_generales'
OUTPUT_DOCS_DIR = './detecciones_generadas'
EXCEL_DIR = './detecciones_concentrado'  # Carpeta raíz donde están (o estarán) los excels con detecciones
CSV_FILE = 'pacientes-diciembre-test-final.csv'
EXCEL_FILE = os.path.join(EXCEL_DIR, 'detecciones_concentrado.xlsx')

# Asegurarnos de que existan los directorios necesarios
os.makedirs(OUTPUT_DOCS_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)

# --- Funciones auxiliares ---

def normalize_str(s):
    """
    Normaliza una cadena: convierte a string, quita espacios al inicio/fin,
    colapsa múltiples espacios en uno solo y convierte a minúsculas.
    Ejemplo: "  Juan   Manuel " --> "juan manuel"
    """
    if pd.isna(s):
        return ''
    return ' '.join(str(s).split()).lower()

def cargar_registros_existentes(root_dir):
    """
    Busca recursivamente todos los .xlsx en root_dir y subcarpetas,
    y concatena en un único DataFrame. Si falla al leer algún archivo,
    lo omite con un mensaje.
    """
    patrón_excel = os.path.join(root_dir, '**', '*.xlsx')
    rutas = glob.glob(patrón_excel, recursive=True)
    dfs = []
    for ruta in rutas:
        try:
            # Leer con dtype=str para evitar conversiones automáticas
            df_tmp = pd.read_excel(ruta, engine='openpyxl', dtype=str)
            dfs.append(df_tmp)
        except Exception as e:
            print(f"Advertencia: no se pudo leer '{ruta}': {e}")
    if dfs:
        df_todos = pd.concat(dfs, ignore_index=True)
    else:
        df_todos = pd.DataFrame(
            columns=[
                'nombres',
                'apellido_materno',
                'apellido_paterno',
                'fecha_de_nacimiento',
                'plantilla_usada'
            ]
        )
    return df_todos

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

# --- NUEVO: Mostrar información básica (ID, nombre, edad, sexo) del(los) paciente(s) seleccionado(s) ---
if df_filtrado.empty:
    print("No se encontraron pacientes con el(los) ID(s) proporcionado(s).")
    exit()
else:
    print("\nInformación del(los) paciente(s) seleccionado(s):")
    # Ajustar los nombres de columna según tu CSV; aquí asumimos que las columnas se llaman 'id', 'nombres', 'edad', 'sexo'
    cols_a_mostrar = []
    if 'id' in df_filtrado.columns:
        cols_a_mostrar.append('id')
    if 'nombre' in df_filtrado.columns:
        cols_a_mostrar.append('nombre')
    if 'edad' in df_filtrado.columns:
        cols_a_mostrar.append('edad')
    if 'sexo' in df_filtrado.columns:
        cols_a_mostrar.append('sexo')

    # Mostrar solo esas columnas
    print(df_filtrado[cols_a_mostrar].to_string(index=False))
    print()

# --- 3. Cargar todas las detecciones existentes para detectar duplicados ---
print("Cargando registros existentes de detecciones (para evitar duplicados)...")
df_existentes = cargar_registros_existentes(EXCEL_DIR)

# Construir un conjunto de claves normalizadas (nombres, amaterno, apaterno, fecha, plantilla)
existing_keys = set()
for _, fila in df_existentes.iterrows():
    nm = normalize_str(fila.get('nombres', ''))
    am = normalize_str(fila.get('apellido_materno', ''))
    ap = normalize_str(fila.get('apellido_paterno', ''))
    fn = str(fila.get('fecha_de_nacimiento', '')).strip()
    pu = normalize_str(fila.get('plantilla_usada', ''))
    clave = (nm, am, ap, fn, pu)
    existing_keys.add(clave)
print(f"Total de detecciones existentes cargadas: {len(existing_keys)}\n")

# --- 4. Listar plantillas disponibles ---
plantillas = glob.glob(os.path.join(PLANTILLAS_DIR, '*.docx'))
plantillas_basename = [os.path.basename(p) for p in plantillas]

if not plantillas:
    print(f"No se encontraron plantillas en {PLANTILLAS_DIR}")
    exit()

print("Detecciones (plantillas) disponibles:")
for idx, nombre in enumerate(plantillas_basename, 1):
    print(f"  {idx}. {nombre}")

seleccion_raw = input("\nSelecciona las plantillas (números separados por coma): ")
try:
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

selected_templates = []
for i in indices:
    ruta_plantilla = plantillas[i - 1]
    nombre_plantilla = plantillas_basename[i - 1]
    selected_templates.append((ruta_plantilla, nombre_plantilla))

print("\nPlantillas seleccionadas:")
for _, nombre in selected_templates:
    print(f"  - {nombre}")

# --- 5. Generar documentos y recolectar nuevos datos para Excel (solo si no existen) ---
registros_nuevos = []

for template_path, template_name in selected_templates:
    plantilla_slug = unidecode(os.path.splitext(template_name)[0]).replace(' ', '_')

    for _, row in df_filtrado.iterrows():
        # Extraer campos clave para la detección
        nombres_raw = row.get('nombres', '')
        apellido_paterno_raw = row.get('apellido_paterno', '')
        apellido_materno_raw = row.get('apellido_materno', '')
        fecha_nac_raw = row.get('fecha_de_nacimiento', '')
        plantilla_raw = template_name  # el nombre de la plantilla (p.ej. "deteccion.docx")

        # Normalizar cadenas para comparar
        nm = normalize_str(nombres_raw)
        am = normalize_str(apellido_materno_raw)
        ap = normalize_str(apellido_paterno_raw)
        fn = str(fecha_nac_raw).strip()
        pu = normalize_str(plantilla_raw)

        clave_candidato = (nm, am, ap, fn, pu)

        if clave_candidato in existing_keys:
            # Si ya existe, no generar nada y avisar
            print(f"Ya existe detección para:")
            print(f"  > Nombres: '{nombres_raw}', Apellido Paterno: '{apellido_paterno_raw}', "
                  f"Apellido Materno: '{apellido_materno_raw}', Fecha Nac: '{fecha_nac_raw}', "
                  f"Plantilla: '{template_name}'.")
            print("No se creó el documento ni se registró en el Excel concentrado.\n")
            continue  # Saltar a la siguiente combinación

        # --- NO EXISTE: Generamos el documento y lo registramos ---
        # Construir contexto para la plantilla
        context = {
            'nombres': nombres_raw,
            'apellido_paterno': apellido_paterno_raw,
            'apellido_materno': apellido_materno_raw,
            'edad': row.get('edad', ''),
            'sexo': row.get('sexo', ''),
            'curp': row.get('curp', ''),
            'fecha_de_nacimiento': fecha_nac_raw,
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
            'diagnostico': row.get('diagnostico', ''),
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

        # Agregar registro a la lista de nuevos para el Excel
        nuevo_registro = {
            'nombres': nombres_raw,
            'apellido_materno': apellido_materno_raw,
            'apellido_paterno': apellido_paterno_raw,
            'fecha_de_nacimiento': fecha_nac_raw,
            'plantilla_usada': template_name,
            'edad': row.get('edad', ''),
            'sexo': row.get('sexo', ''),
            'curp': row.get('curp', ''),
            'lugar_de_nacimiento': row.get('lugar_de_nacimiento', ''),
            'numero_de_expediente': row.get('numero_de_expediente', ''),
            'fecha_consulta': row.get('fecha_consulta', ''),
            'hora': row.get('hora', ''),
            'peso': row.get('peso', ''),
            'talla': row.get('talla', ''),
            'tension_arterial': row.get('tension_arterial', ''),
            'fc': row.get('fc', ''),
            'fr': row.get('fr', ''),
            'temperatura': row.get('temperatura', ''),
            'dxtx': row.get('dxtx', ''),
            'imc': row.get('imc', ''),
            'diagnostico': row.get('diagnostico', ''),
        }
        registros_nuevos.append(nuevo_registro)

        # Agregar la clave a existing_keys para no duplicar dentro de este mismo ciclo
        existing_keys.add(clave_candidato)

        print("Registro agregado para el Excel concentrado.\n")

# --- 6. Guardar Excel concentrado con solo los registros nuevos ---
df_para_excel = pd.DataFrame(registros_nuevos)

if not df_para_excel.empty:
    if os.path.exists(EXCEL_FILE):
        try:
            df_main = pd.read_excel(EXCEL_FILE, engine='openpyxl', dtype=str)
        except Exception as e:
            print(f"Error al leer '{EXCEL_FILE}': {e}")
            df_main = pd.DataFrame()
        df_comb = pd.concat([df_main, df_para_excel], ignore_index=True)
    else:
        df_comb = df_para_excel

    df_comb.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    print(f"\nExcel concentrado actualizado en: {EXCEL_FILE}")
else:
    print("\nNo se agregaron nuevas detecciones al Excel concentrado (todo ya existía).")
