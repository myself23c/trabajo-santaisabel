import pandas as pd
from docxtpl import DocxTemplate
from unidecode import unidecode

# Leer el archivo CSV con encoding latin1
df = pd.read_csv('pacientes-diciembre-test-final.csv', encoding='utf-8')

# Normalizar los nombres de las columnas
df.columns = [unidecode(col).strip().lower() for col in df.columns]

# Imprimir los nombres de las columnas para verificar
print("Columnas del CSV:", df.columns)



# Asegurarse de que la columna 'id' es de tipo cadena
df['id'] = df['id'].astype(str)

# Función para concatenar las variables en prevencion
def concatenate_prevencion(row):
    fields = [
        'referido', 'embarazada', 'cronicodegenerativo', 'eda_menor', 'ira_menor', 'intervension_saludmental',
        'relacion temporal por motivo', 'derechohabiencia', 'migrante', 'glucosa resultado obtenido a traves de',
        'intervenciones de salud mental y adicciones', 'riesgos', 'plan de seguridad', 'trimestre', 'complicaciones',
        'otras acciones a embarazadas', 'otros eventos', 'edi tipo', 'resultado edi', 'resultado battelle',
        'eda plan tratamiento', 'ira tratamiento', 'aplicacion de cedula cancer en el ano', 'intervenciones gerontologicas',
        'esquema de vacunacion', 'referido por', 'teleconsulta / interpretacion diagnostica', 'modalidad'
    ]
    return ' '.join([f"{field}: {str(row[field])}" if pd.notna(row[field]) else f"{field}: vacio" for field in fields if field in row])

# Función para generar acciones basadas en la edad y el sexo
def generar_acciones_por_edad_y_sexo(edad_str, sexo_str):
    try:
        edad = int(edad_str)  # Convertir edad a número
    except ValueError:
        return "Edad no válida"

    sexo = sexo_str.upper()  # Asegurarse de que el sexo esté en mayúsculas

    if sexo == "H":
        if edad < 5:
            return "se le revisa cartilla de vacunacion asi como se le comenta a adulto que acompana la improtancvia de el lavado de dientes correctas, se instruye sobre signos y sintomas de alarma de cancer, asi como de instruir de la improtancia de la vacunacion y se comentan signos y sintomas del algun transtorno del aprendizaje"
        elif 6 <= edad <= 19:
            return "SE LE INSTRUYE SOBRE PREVENCION DE ADICCIONES ASI COMO PREVENCION DE ACCIDENTES, SE LE REVISA LA CARTILLA DE SALUD"
        elif edad > 20:
            return "SE LE COMENTA SOBRE LA IMPORTANCIA DE DETECCIONES DE ENFERMEDADES CRONICO DEGENERATIVAS Y PREVENCION DE ACCIDENTES CONTROL DE PESO Y SE REVISA CARTILLA"
    elif sexo == "M":
        if edad < 5:
            return "SE REVISA LA CARTILLA DE VACUNACION ASI COMO SE LE COMENTA  AL ADULTO QUE ACOMPANA LA IMPROTNCIA DEL LEVADO CORRECTO DE DIENTES, SE ISNTRUYE DE SIGNOS Y SINTOMAS DE ALARMA DE CANCER, DE BUENA NUTRICION, LA IMPROTNACIA DE LA VACUNACION Y SINGOS Y SINTOAMS DE ALGUN TRANSTORNO DEL APRENDIZAJE"
        elif 6 <= edad <= 19:
            return "SE LE INSTRUYE SOBRE PREVENCION DE ADICCIONES ASI COMO PREVENCION DE ACCIDENTES, SE LE REVISA LA CARTILLA DE SALUD"
        elif edad > 20:
            return "tSE LE COMENTA SOBRE LA IMPORTANCIA DE DETECCIONES DE ENFERMEDADES CRONICO DEGENERATIVAS Y PREVENCION DE CANCER CERVICOUTERINO Y CANCER DE MAMA Y SE LE INSTRUYE COMO REALIZARCE LA EXPLORACION Y LA INFORMACION DE COMO VENIR PREPARADA PARA REALIZAR PAPANICOLAO Y FECHASPREVENCION DE ACCIDENTES CONTROL DE PESO Y SE REVISA CARTILLA"
    return "Datos no válidos para generar acciones"

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

# Plantilla de Word
template_path = 'plantillas/NOTAMEDICA.docx'

# Crear documentos para cada fila filtrada
for index, row in df_filtered.iterrows():
    # Obtener edad y sexo
    edad = row['edad:'] if 'edad:' in row and pd.notna(row['edad:']) else 'vacio'
    sexo = row['sexo:'] if 'sexo:' in row and pd.notna(row['sexo:']) else 'vacio'

    # Generar acciones basadas en la edad y sexo
    acciones = generar_acciones_por_edad_y_sexo(edad, sexo)

    context = {
        'nombre': row['nombre:'] if 'nombre:' in row and pd.notna(row['nombre:']) else 'vacio',
        'edad': edad,
        'sexo': sexo,
        'lugar_de_nacimiento': row['lugar de nacimiento:'] if 'lugar de nacimiento:' in row and pd.notna(row['lugar de nacimiento:']) else 'vacio',
        'fecha_de_nacimiento': row['fecha de nacimiento:'] if 'fecha de nacimiento:' in row and pd.notna(row['fecha de nacimiento:']) else 'vacio',
        'curp': row['curp:'] if 'curp:' in row and pd.notna(row['curp:']) else 'vacio',
        'n_de_expediente': row['n. de expediente:'] if 'n. de expediente:' in row and pd.notna(row['n. de expediente:']) else 'vacio',
        'fecha': row['fecha:'] if 'fecha:' in row and pd.notna(row['fecha:']) else 'vacio',
        'hora': row['hora:'] if 'hora:' in row and pd.notna(row['hora:']) else 'vacio',
        'peso': row['peso:'] if 'peso:' in row and pd.notna(row['peso:']) else 'vacio',
        'talla': row['talla:'] if 'talla:' in row and pd.notna(row['talla:']) else 'vacio',
        'ta': row['t/a:'] if 't/a:' in row and pd.notna(row['t/a:']) else 'vacio',
        'fc': row['fc:'] if 'fc:' in row and pd.notna(row['fc:']) else 'vacio',
        'fr': row['fr:'] if 'fr:' in row and pd.notna(row['fr:']) else 'vacio',
        'temp': row['temp:'] if 'temp:' in row and pd.notna(row['temp:']) else 'vacio',
        'imc': row['imc:'] if 'imc:' in row and pd.notna(row['imc:']) else 'vacio',
        'cc': row['cc:'] if 'cc:' in row and pd.notna(row['cc:']) else 'vacio',
        'plan': row['plan:'] if 'plan:' in row and pd.notna(row['plan:']) else 'vacio',
        'subjetivo': row['subjetivo:'] if 'subjetivo:' in row and pd.notna(row['subjetivo:']) else 'vacio',
        'neurologico': row['neurologico:'] if 'neurologico:' in row and pd.notna(row['neurologico:']) else 'vacio',
        'cabeza': row['cabeza:'] if 'cabeza:' in row and pd.notna(row['cabeza:']) else 'vacio',
        'torax': row['torax:'] if 'torax:' in row and pd.notna(row['torax:']) else 'vacio',
        'abdomen': row['abdomen:'] if 'abdomen:' in row and pd.notna(row['abdomen:']) else 'vacio',
        'extremidades': row['extremidades:'] if 'extremidades:' in row and pd.notna(row['extremidades:']) else 'vacio',
        'analisis': row['analisis:'] if 'analisis:' in row and pd.notna(row['analisis:']) else 'vacio',
        'diagnostico': row['diagnostico:'] if 'diagnostico:' in row and pd.notna(row['diagnostico:']) else 'vacio',
        'tratamiento': row['tratamiento:'] if 'tratamiento:' in row and pd.notna(row['tratamiento:']) else 'vacio',
        'medicamentos': row['medicamentos:'] if 'medicamentos:' in row and pd.notna(row['medicamentos:']) else 'vacio',
        'plan_2': row['plan 2:'] if 'plan 2:' in row and pd.notna(row['plan 2:']) else 'vacio',
        'prevencion': concatenate_prevencion(row),
        'acciones': acciones  # Agregar las acciones generadas
    }

    # Crear y guardar el documento
    doc = DocxTemplate(template_path)
    doc.render(context)

    # Asegurarse de que el nombre sea una cadena
    nombre = row['nombre:'] if 'nombre:' in row and pd.notna(row['nombre:']) else 'vacio'
    nombre = str(nombre)
    nombre = unidecode(nombre)
    output_path = f"notas_medicas/{nombre.replace(' ', '_')}_{row['id']}.docx"
    doc.save(output_path)
    print(f"Documento creado: {output_path}")
