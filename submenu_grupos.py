import os
import pandas as pd
from fuzzywuzzy import process

# Ruta de la base de datos principal
db_file = '/home/juan/Escritorio/trabajo-santaisabel/carpeta/python-proyectos/dbs/nombres_unicos_limpio.csv'

# Ruta de la carpeta con los archivos de grupos
grupo_dir = '/home/juan/Escritorio/trabajo-santaisabel/carpeta/python-proyectos/grupos'

# Columnas iniciales del archivo de grupo
columnas_iniciales = [
    'nombre_completo', 'edad', 'sexo', 'lugar_nacimiento', 
    'fecha_nacimiento', 'curp', 'apellidos_de_la_familia', 
    'numero_de_expediente'
]

def cargar_datos_principal():
    """Carga los datos de la base de datos principal."""
    try:
        data = pd.read_csv(db_file, encoding='utf-8')
        return data
    except Exception as e:
        print(f"Error al cargar la base de datos principal: {e}")
        return pd.DataFrame()

def listar_archivos_grupos():
    """Lista los archivos de grupos en la carpeta ./grupos."""
    return [f for f in os.listdir(grupo_dir) if f.endswith('.xlsx') or f.endswith('.ods')]

def crear_grupo():
    """Crea un nuevo archivo de grupo ODS con las columnas iniciales."""
    nombre_archivo = input("Ingrese el nombre del archivo de grupo a crear: ") + '.ods'
    archivo_path = os.path.join(grupo_dir, nombre_archivo)
    try:
        df = pd.DataFrame(columns=columnas_iniciales)
        df.to_excel(archivo_path, index=False, engine='odf')
        print(f"Grupo '{nombre_archivo}' creado con columnas iniciales.")
    except Exception as e:
        print(f"Error al crear el grupo: {e}")

def buscar_paciente(nombre, data):
    """Busca coincidencias de un nombre en la base de datos principal."""
    if 'nombre_completo' not in data.columns:
        print("La columna 'nombre_completo' no está disponible en los datos proporcionados.")
        return None

    coincidencias = process.extractBests(nombre, data['nombre_completo'], score_cutoff=90)
    if coincidencias:
        print("Coincidencias encontradas:")
        for idx, resultado in enumerate(coincidencias):
            nombre, score = resultado[0], resultado[1]
            print(f"{idx + 1}. {nombre} (Coincidencia: {score}%)")
        try:
            seleccion = int(input("Seleccione el número de la coincidencia: ")) - 1
            if 0 <= seleccion < len(coincidencias):
                nombre_seleccionado = coincidencias[seleccion][0]
                return data[data['nombre_completo'] == nombre_seleccionado].iloc[0]
        except (ValueError, IndexError):
            print("Selección inválida.")
    else:
        print("No se encontró ninguna coincidencia con el 90% o más.")
    return None

def agregar_paciente_a_grupo(paciente, archivo_grupo):
    """Agrega un paciente al archivo de grupo seleccionado si no está ya en él."""
    archivo_path = os.path.join(grupo_dir, archivo_grupo)
    try:
        grupo_data = pd.read_excel(archivo_path, engine='odf')
    except Exception as e:
        print(f"Error al leer el archivo del grupo: {e}")
        grupo_data = pd.DataFrame(columns=columnas_iniciales)

    # Asegurar que las columnas iniciales estén presentes
    for columna in columnas_iniciales:
        if columna not in grupo_data.columns:
            grupo_data[columna] = None

    #grupo_data = grupo_data.dropna(how='all', axis=1)

    # Validar y agregar paciente
    paciente_dict = {col: paciente.get(col, None) for col in columnas_iniciales}
    paciente_df = pd.DataFrame([paciente_dict])

    if 'nombre_completo' in grupo_data.columns:
        if not (grupo_data['nombre_completo'] == paciente.get('nombre_completo', '')).any():
            grupo_data = pd.concat([grupo_data, paciente_df], ignore_index=True)
            try:
                grupo_data.to_excel(archivo_path, index=False, engine='odf')
                print(f"Paciente {paciente.get('nombre_completo', 'Desconocido')} agregado al grupo {archivo_grupo}.")
            except Exception as e:
                print(f"Error al guardar el archivo del grupo: {e}")
        else:
            print(f"El paciente {paciente.get('nombre_completo', 'Desconocido')} ya existe en {archivo_grupo}.")
    else:
        print("La columna 'nombre_completo' no está presente en el archivo del grupo. No se puede agregar el paciente.")

def mostrar_pacientes_en_grupo(archivo_grupo):
    """Muestra todos los pacientes en el archivo de grupo seleccionado."""
    archivo_path = os.path.join(grupo_dir, archivo_grupo)
    try:
        grupo_data = pd.read_excel(archivo_path, engine='odf')
        print(f"Pacientes en el grupo {archivo_grupo}:")
        print(grupo_data)
    except Exception as e:
        print(f"Error al leer el archivo del grupo: {e}")

def submenu_grupos():
    """Submenú para manejar los grupos."""
    data = cargar_datos_principal()

    if data.empty:
        print("No se pudo cargar la base de datos principal. Regresando al menú principal.")
        return

    while True:
        print("======== SUBMENU GRUPOS ========")
        print("1. Buscar y agregar paciente a un grupo")
        print("2. Mostrar pacientes en un grupo")
        print("3. Crear nuevo grupo")
        print("0. Regresar al menú principal")
        print("================================")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre = input("Ingrese el nombre del paciente a buscar: ")
            paciente = buscar_paciente(nombre, data)
            if paciente is not None:
                archivos_grupos = listar_archivos_grupos()
                if archivos_grupos:
                    print("Seleccione el grupo para agregar al paciente:")
                    for idx, archivo in enumerate(archivos_grupos):
                        print(f"{idx + 1}. {archivo}")
                    try:
                        seleccion_grupo = int(input("Seleccione el número del grupo: ")) - 1
                        if 0 <= seleccion_grupo < len(archivos_grupos):
                            agregar_paciente_a_grupo(paciente, archivos_grupos[seleccion_grupo])
                        else:
                            print("Selección inválida.")
                    except ValueError:
                        print("Entrada inválida.")
                else:
                    print("No hay grupos disponibles.")
        elif opcion == '2':
            archivos_grupos = listar_archivos_grupos()
            if archivos_grupos:
                print("Seleccione el grupo para mostrar pacientes:")
                for idx, archivo in enumerate(archivos_grupos):
                    print(f"{idx + 1}. {archivo}")
                try:
                    seleccion_grupo = int(input("Seleccione el número del grupo: ")) - 1
                    if 0 <= seleccion_grupo < len(archivos_grupos):
                        mostrar_pacientes_en_grupo(archivos_grupos[seleccion_grupo])
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Entrada inválida.")
            else:
                print("No hay grupos disponibles.")
        elif opcion == '3':
            crear_grupo()
        elif opcion == '0':
            break
        else:
            print("Opción inválida. Intente de nuevo.")