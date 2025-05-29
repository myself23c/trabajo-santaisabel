import pandas as pd
from docxtpl import DocxTemplate
from unidecode import unidecode

# 1. Leer el CSV con encoding utf-8 (ajusta nombre de archivo si es necesario)
df = pd.read_csv('pacientes-diciembre-test-final.csv', encoding='utf-8')

# 2. Normalizar los nombres de columna: quitar acentos, pasar a minúsculas y usar guiones bajos
df.columns = [
    unidecode(col).strip().lower().replace(' ', '_')
    for col in df.columns
]
print("Columnas del CSV:", df.columns.tolist())

# 3. Asegurar que el ID sea cadena
df['id'] = df['id'].astype(str)

# 4. Función para concatenar campos de “prevención” (solo incluye las que existen en el CSV)
def concatenate_prevencion(row):
    fields = [
        'relacion_temporal', 'dm2', 'has', 'ira', 'asma', 'conjuntivitis', 'otitis',
        'deteccion_salud_mental', 'deteccion_adicciones', 'deteccion_violencia_mujer',
        'prueba_edi', 'resultado_edi', 'resultado_battelle',
        'eda_tratamiento', 'ira_tratamiento', 'aplicacion_cedula_cancer_ano',
        'intervenciones_gerontologicas', 'esquema_vacunacion',
        'promocion_de_la_salud', 'folio_receta', 'referido', 'alergia'
    ]
    partes = []
    for f in fields:
        if f in row:
            valor = row[f] if pd.notna(row[f]) else 'vacío'
            partes.append(f"{f}: {valor}")
    return ' | '.join(partes)

# 5. Función para generar acciones según edad y sexo
def generar_acciones_por_edad_y_sexo(edad_str, sexo_str):
    try:
        edad = int(edad_str)
    except:
        return "Edad no válida"
    sexo = sexo_str.upper()
    if sexo == 'H':
        if edad < 5:
            return ("Revisar cartilla de vacunación, instruir lavado dental correcto, "
                    "señalar signos de alarma de cáncer y vacunación, alerta de trastornos de aprendizaje.")
        elif edad <= 19:
            return "Se le da platica de prevención de adicciones y accidentes; revisar cartilla de salud."
        else:
            return "Se le informa de la importancia de detección de enfermedades crónico-degenerativas, control de peso y prevención de accidentes, asi como la importancia de deteccion de cancer de prostata y prevencion de esta"
    elif sexo == 'M':
        if edad < 5:
            return ("se realiza revision cartilla de vacunación, instruir lavado dental, alertar sobre cáncer infantil, "
                    "nutrición y trastornos de aprendizaje.")
        elif edad <= 19:
            return "se instruye sobre prevención de adicciones y accidentes;se  revisa cartilla de salud y prevencion de embarazos no deseados"
        else:
            return ("Detección de cáncer cervicouterino y de mama; instruir auto-exploración y preparación "
                    "para Papanicolaou, control de peso y prevención de accidentes.")
    return "Datos insuficientes"

# 6. Selección de IDs (último o lista)
option = input("Última fila (U) o lista de IDs (L)? ")
if option.upper() == 'U':
    ids = [df.iloc[-1]['id']]
elif option.upper() == 'L':
    ids = [i.strip() for i in input("IDs separados por coma: ").split(',')]
else:
    print("Opción no válida."); exit()

print("IDs seleccionados:", ids)
df_filtrado = df[df['id'].isin(ids)]
print("Filtrado:", df_filtrado)

# 7. Ruta de la plantilla Word
template_path = 'plantillas/NOTAMEDICA.docx'

# 8. Crear un documento por cada registro
for _, row in df_filtrado.iterrows():
    # Generar acciones
    acciones = generar_acciones_por_edad_y_sexo(row.get('edad', ''), row.get('sexo', ''))
    # Armar contexto para la plantilla
    context = {
        'nombre': row.get('nombre', 'vacío'),
        'apellido_paterno': row.get('apellido_paterno', 'vacío'),
        'apellido_materno': row.get('apellido_materno', 'vacío'),
        'edad': row.get('edad', 'vacío'),
        'sexo': row.get('sexo', 'vacío'),
        'lugar_de_nacimiento': row.get('lugar_de_nacimiento', 'vacío'),
        'fecha_de_nacimiento': row.get('fecha_de_nacimiento', 'vacío'),
        'curp': row.get('curp', 'vacío'),
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
        'cc': row.get('cc', 'vacío'),
        'plan': row.get('plan', 'vacío'),
        'subjetivo': row.get('subjetivo', 'vacío'),
        'neurologico': row.get('neurologico', 'vacío'),
        'cabeza': row.get('cabeza', 'vacío'),
        'torax': row.get('torax', 'vacío'),
        'abdomen': row.get('abdomen', 'vacío'),
        'extremidades': row.get('extremidades', 'vacío'),
        'analisis': row.get('analisis', 'vacío'),
        'diagnostico': row.get('diagnostico', 'vacío'),
        'tratamiento': row.get('tratamiento', 'vacío'),
        'medicamentos': row.get('medicamentos', 'vacío'),
        'pronostico': row.get('pronostico', 'vacío'),
        'primera_vez_ano': row.get('primera_vez_ano', 'vacío'),
        # Campos de prevención concatenados
        'prevencion': concatenate_prevencion(row),
        'acciones': acciones,
        # Añade más si tu plantilla los requiere...
    }

    doc = DocxTemplate(template_path)
    doc.render(context)
    # Nombre de archivo basado en apellidos y ID
# Ahora, solo nombre + id
    nombre_archivo = unidecode(f"{row.get('nombre','')}_{row['id']}")
    output_path = f"notas_medicas/{nombre_archivo.replace(' ', '_')}.docx"

    doc.save(output_path)
    print(f"Documento creado: {output_path}")
