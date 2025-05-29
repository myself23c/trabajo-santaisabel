import pandas as pd
from docxtpl import DocxTemplate
from unidecode import unidecode

# 1. Leer el CSV con encoding utf-8
df = pd.read_csv('pacientes-diciembre-test-final.csv', encoding='utf-8')

# 2. Normalizar nombres de columnas
df.columns = [
    unidecode(col).strip().lower().replace(' ', '_')
    for col in df.columns
]
print("Columnas del CSV:", df.columns.tolist())

# 3. Asegurar que el ID sea cadena
df['id'] = df['id'].astype(str)

# 4. Solicitar datos familiares por input
abuelos_paternos = input("Abuelos paternos: ")
abuelos_maternos = input("Abuelos maternos: ")
madre = input("Madre: ")
padre = input("Padre: ")

# 5. Selección de IDs
option = input("Última fila (U) o lista de IDs (L)? ")
if option.upper() == 'U':
    ids = [df.iloc[-1]['id']]
elif option.upper() == 'L':
    ids = [i.strip() for i in input("IDs separados por coma: ").split(',')]
else:
    print("Opción no válida.")
    exit()

print("IDs seleccionados:", ids)
df_filtrado = df[df['id'].isin(ids)]

# 6. Ruta de la plantilla
template_path = 'plantillas/HISTORIA_CLINICA_PARA_PLANTILLA_V1.docx'

# 7. Crear documentos
for _, row in df_filtrado.iterrows():
    context = {
        'nombres': row.get('nombre', 'vacío'),
        'apellido_paterno': row.get('apellido_paterno', 'vacío'),
        'apellido_materno': row.get('apellido_materno', 'vacío'),
        'edad': row.get('edad', 'vacío'),
        'sexo': row.get('sexo', 'vacío'),
        'curp': row.get('curp', 'vacío'),
        'fecha_de_nacimiento': row.get('fecha_de_nacimiento', 'vacío'),
        'lugar_de_nacimiento': row.get('lugar_de_nacimiento', 'vacío'),
        'numero_de_expediente': row.get('numero_de_expediente', 'vacío'),
        'fecha': row.get('fecha_consulta', 'vacío'),
        'hora': row.get('hora', 'vacío'),
         
        
        
        
        'peso': row.get('peso', 'vacío'),
        'talla': row.get('talla', 'vacío'),
        'tension_arterial': row.get('tension_arterial', 'vacío'),
        'fc': row.get('fc', 'vacío'),
        'fr': row.get('fr', 'vacío'),
        'temperatura': row.get('temperatura', 'vacío'),
        'dxtx': row.get('dxtx', 'vacío'),
        'imc': row.get('imc', 'vacío'),
        'plan': row.get('plan', 'vacío'),
        'subjetivo': row.get('subjetivo', 'vacío'),

        'analisis': row.get('analisis', 'vacío'),
        'diagnostico': row.get('diagnostico', 'vacío'),
        'tratamiento': row.get('tratamiento', 'vacío'),

        'abuelos_paternos': abuelos_paternos,
        'abuelos_maternos': abuelos_maternos,
        'madre': madre,
        'padre': padre,
        # Agrega más campos si tu plantilla los requiere
    }

    doc = DocxTemplate(template_path)
    doc.render(context)

    nombre_archivo = unidecode(f"{row.get('nombre','')}_{row['id']}")
    output_path = f"notas_medicas/historia-clinica-{nombre_archivo.replace(' ', '_')}.docx"

    doc.save(output_path)
    print(f"Documento creado: {output_path}")
