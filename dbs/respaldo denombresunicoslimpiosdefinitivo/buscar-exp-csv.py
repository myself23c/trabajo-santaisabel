import pandas as pd
from fuzzywuzzy import process
from colorama import Fore, Style, init
from datetime import datetime
from submenu_grupos import submenu_grupos
import os

# Inicializar colorama
init(autoreset=True)

# Cargar la base de datos desde el archivo CSV
db_file = 'dbs/nombres_unicos_limpio.csv'
# Cargar la base de datos desde el archivo CSV con codificación latin1
#data = pd.read_csv(db_file, encoding='latin1')
data = pd.read_csv(db_file, encoding='latin1')

# Convertir todas las columnas de texto a minúsculas para insensibilidad a mayúsculas/minúsculas
data['nombre_completo'] = data['nombre_completo'].str.lower()
data['apellidos_de_la_familia'] = data['apellidos_de_la_familia'].str.lower()
data['numero_de_expediente'] = data['numero_de_expediente'].fillna("").astype(str)

# Agregar columnas 'apellidos_de_la_familia' y 'numero_de_expediente' si no existen
if 'apellidos_de_la_familia' not in data.columns:
    data['apellidos_de_la_familia'] = ""
if 'numero_de_expediente' not in data.columns:
    data['numero_de_expediente'] = ""

def guardar_cambios():
    """Guarda los cambios en la base de datos."""
    data.to_csv(db_file, index=False)
    print("Cambios guardados exitosamente.")

def menu():
    """Muestra el menú principal."""
    print("======== MENU PRINCIPAL ========")
    print("1. Buscar miembro y agregar si no existe")
    print("2. Buscar miembro y mostrar toda la información")
    print("3. Modificar información de un miembro")
    print("4. Submenu de expedientes")
    print("5. Submenu de grupos/cronicos/ninosano/planificacion")
    print("0. Salir")
    print("================================")

def buscar_miembro(nombre, exacto=False):
    """Busca miembros en la base de datos con una coincidencia del 93% o exacta."""
    nombre = nombre.lower()
    coincidencias = process.extractBests(nombre, data['nombre_completo'], score_cutoff=93) if not exacto else [(nombre, 100)]
    if not coincidencias:
        return None
    return [c[0] for c in coincidencias]


#####test
def buscar_en_grupos(nombre):
    """Busca un nombre en todos los archivos Excel y ODS en la carpeta ./grupos."""
    carpeta_grupos = './grupos'
    resultados = []

    if not os.path.exists(carpeta_grupos):
        return ["La carpeta 'grupos' no existe"]

    for archivo in os.listdir(carpeta_grupos):
        if archivo.endswith('.xlsx') or archivo.endswith('.ods'):
            ruta_archivo = os.path.join(carpeta_grupos, archivo)
            try:
                df = pd.read_excel(ruta_archivo, engine='openpyxl') if archivo.endswith('.xlsx') else pd.read_excel(ruta_archivo, engine='odf')
                for columna in df.columns:
                    if df[columna].astype(str).str.contains(nombre, case=False, na=False).any():
                        resultados.append(archivo)
                        break
            except Exception as e:
                print(f"Error al leer {archivo}: {e}")

    return resultados if resultados else ["No está en ningún grupo"]

def mostrar_resultados(nombres, info_completa=False, editar_desde_busqueda=False):
    """Muestra resultados de coincidencias."""
    global data  # Se hace global para que la columna agregada se refleje en todo el DataFrame
    for nombre in nombres:
        persona = data[data['nombre_completo'] == nombre]

        # Actualizar la columna 'grupos_donde_aparece' con la información de los grupos donde aparece el nombre
        grupos = ', '.join(buscar_en_grupos(nombre))
        data.loc[data['nombre_completo'] == nombre, 'grupos_donde_aparece'] = grupos

        if info_completa:
            # Refrescar la variable persona para reflejar el cambio en la columna 'grupos_donde_aparece'
            persona = data[data['nombre_completo'] == nombre]

            # Preparar la salida formateada tipo "clave-valor"
            for _, row in persona.iterrows():
                print("\n------ Información Completa ------")
                for col in persona.columns:
                    print(f"{Fore.YELLOW}{col}{Style.RESET_ALL}: {row[col]}")
                print("\n" + "=" * 40 + "\n")  # Separador visual entre registros

        else:
            print("------ Resultado ------")
            print(f"{Fore.GREEN}Nombre: {nombre}{Style.RESET_ALL}")
            expediente = persona['numero_de_expediente'].values[0] if persona['numero_de_expediente'].values[0] else "No tiene"
            apellidos = persona['apellidos_de_la_familia'].values[0] if persona['apellidos_de_la_familia'].values[0] else "No tiene"
            grupos = persona['grupos_donde_aparece'].values[0] if 'grupos_donde_aparece' in persona.columns else "No está en ningún grupo"
            print(f"{Fore.CYAN}Número de expediente: {expediente}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Apellidos de la familia: {apellidos}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Grupos donde aparece: {grupos}{Style.RESET_ALL}")

            # Permitir edición si se selecciona editar desde la búsqueda
            if editar_desde_busqueda:
                opcion_editar = input("¿Deseas modificar la información de esta persona? (s/n): ").lower()
                if opcion_editar == 's':
                    nuevo_apellidos = input("Ingresa los nuevos apellidos de la familia: ")
                    nuevo_expediente = input("Ingresa el nuevo número de expediente: ")
                    while not nuevo_expediente.isdigit():
                        nuevo_expediente = input("Expediente inválido. Ingresa solo números: ")
                    data.loc[data['nombre_completo'] == nombre, 'apellidos_de_la_familia'] = nuevo_apellidos.lower()
                    data.loc[data['nombre_completo'] == nombre, 'numero_de_expediente'] = nuevo_expediente
                    guardar_cambios()
                    print("Información actualizada.")
    print("=================================")

###### test


def agregar_miembro(nombre):
    """Agrega un nuevo miembro con datos ingresados."""
    print("No se encontró una coincidencia.")
    sexo = input("Ingresa el sexo (H para hombre, M para mujer): ").upper()
    while sexo not in ['H', 'M']:
        sexo = input("Sexo inválido. Ingresa H para hombre o M para mujer: ").upper()
    apellidos = input("Ingresa los apellidos de la familia: ")
    expediente = input("Ingresa el número de expediente: ")
    while not expediente.isdigit():
        expediente = input("Expediente inválido. Ingresa solo números: ")
    
    nueva_persona = pd.DataFrame({
        'nombre_completo': [nombre.lower()],
        'sexo': [sexo],
        'apellidos_de_la_familia': [apellidos.lower()],
        'numero_de_expediente': [expediente]
    })
    
    global data
    data = pd.concat([data, nueva_persona], ignore_index=True)
    print("Miembro agregado exitosamente.")
    guardar_cambios()

def modificar_miembro(nombre):
    """Permite modificar toda la información de un miembro."""
    coincidencias = buscar_miembro(nombre)
    if coincidencias:
        print("Coincidencias encontradas:")
        mostrar_resultados(coincidencias, info_completa=True)
        nombre = input("Ingresa el nombre exacto de la persona que deseas modificar: ")
        if nombre in coincidencias:
            for col in data.columns:
                nuevo_valor = input(f"Modificar {col} (Dejar en blanco para no modificar): ")
                if nuevo_valor:
                    data.loc[data['nombre_completo'] == nombre, col] = nuevo_valor.lower() if col == 'nombre_completo' else nuevo_valor
            guardar_cambios()
            print("Información actualizada correctamente.")
    else:
        print("No se encontró ninguna coincidencia.")

def obtener_edad(fecha_nacimiento, edad):
    """Calcula la edad con fecha de nacimiento o columna de edad si es posible."""
    if pd.notna(fecha_nacimiento):
        try:
            fecha_nac = datetime.strptime(str(fecha_nacimiento), "%d/%m/%Y")
            today = datetime.today()
            calculated_age = today.year - fecha_nac.year - ((today.month, today.day) < (fecha_nac.month, fecha_nac.day))
            return calculated_age
        except ValueError:
            pass
    if pd.notna(edad) and str(edad).isdigit():
        return int(edad)
    return None

def buscar_por_expediente():
    expediente = input("Ingrese el número de expediente a buscar: ")
    
    try:
        # Convertir el número ingresado y los de la columna a enteros
        expediente_int = int(float(expediente))
        data['numero_de_expediente'] = data['numero_de_expediente'].apply(lambda x: int(float(x)) if x else 0)
        
        personas = data[data['numero_de_expediente'] == expediente_int]
        
        if not personas.empty:
            print(f"Personas con el expediente {expediente}:")
            print(personas[['nombre_completo', 'edad', 'sexo', 'lugar_nacimiento', 'fecha_nacimiento', 'curp', 'apellidos_de_la_familia', 'numero_de_expediente']])
        else:
            print(f"No se encontraron personas con el número de expediente {expediente}")
    except ValueError:
        print("Por favor ingrese un número de expediente válido.")

def listar_expedientes():
    expedientes = data.groupby('numero_de_expediente')['nombre_completo'].apply(list).sort_index()
    for numero, integrantes in expedientes.items():
        print(f"{Fore.CYAN}Expediente {numero}:{Style.RESET_ALL} {' - '.join(integrantes)}")


def listar_expedientes_libres():
    ocupados = data['numero_de_expediente'].dropna().astype(int).unique()
    libres = [i for i in range(1, 301) if i not in ocupados]
    print("Expedientes libres del 1 al 300:")
    print(", ".join(map(str, libres)))

def listar_por_rango_edad(inicio, fin):
    data['calculated_age'] = data.apply(lambda row: obtener_edad(row['fecha_nacimiento'], row['edad']), axis=1)
    rango = data[(data['calculated_age'] >= inicio) & (data['calculated_age'] <= fin)].sort_values(by='calculated_age')
    print(rango[['nombre_completo', 'calculated_age', 'sexo']])

def listar_por_genero(genero):
    data['calculated_age'] = data.apply(lambda row: obtener_edad(row['fecha_nacimiento'], row['edad']), axis=1)
    genero_filtrado = data[(data['sexo'] == genero) & (data['calculated_age'].notna())].sort_values(by='calculated_age')
    print(genero_filtrado[['nombre_completo', 'calculated_age', 'sexo']])


def listar_por_sexo_y_rango_edad():
    """Lista personas según el sexo y un rango de edad proporcionado."""
    # Preguntar el sexo
    sexo = input("Ingrese el sexo (H para hombre, M para mujer, T para todos): ").upper()
    while sexo not in ['H', 'M', 'T']:
        sexo = input("Sexo inválido. Ingrese H para hombre, M para mujer o T para todos: ").upper()
    
    # Preguntar el rango de edad
    try:
        edad_inicio = int(input("Ingrese la edad inicial del rango: "))
        edad_fin = int(input("Ingrese la edad final del rango: "))
    except ValueError:
        print("Edad inválida. Debe ingresar números.")
        return
    
    # Calcular edades
    data['calculated_age'] = data.apply(lambda row: obtener_edad(row['fecha_nacimiento'], row['edad']), axis=1)
    
    # Filtrar según el sexo y el rango de edad
    if sexo == 'T':
        filtro = (data['calculated_age'] >= edad_inicio) & (data['calculated_age'] <= edad_fin)
    else:
        filtro = (data['sexo'] == sexo) & (data['calculated_age'] >= edad_inicio) & (data['calculated_age'] <= edad_fin)
    
    # Obtener y mostrar los resultados
    resultados = data[filtro].sort_values(by='calculated_age')
    if resultados.empty:
        print("No se encontraron personas que coincidan con los criterios.")
    else:
        print(resultados[['nombre_completo', 'calculated_age', 'sexo']])



def mostrar_submenu_expediente():
    """Muestra el submenu de opciones para manejar expedientes."""
    print("======== SUBMENU EXPEDIENTES ========")
    print("1. Buscar personas por número de expediente")
    print("2. Lista de todos los números de expediente y sus integrantes")
    print("3. Lista de expedientes libres del 1 al 300")
    print("4. Submenu de rangos de edad")
    print("0. Regresar al menú principal")
    print("================================")

def submenu_rangos_edad():
    """Muestra el submenu para ordenamiento por rangos de edad y género."""
    print("======== SUBMENU RANGOS DE EDAD ========")
    print("1. Lista de personas de 0 a 5 años de edad")
    print("2. Lista de personas de 6 a 12 años de edad")
    print("3. Lista de todos los hombres ordenados por edad")
    print("4. Lista de todas las mujeres ordenadas por edad")
    print("5. Lista por sexo y rango de edad")  # Nueva opción añadida
    print("0. Regresar al menú de expedientes")
    print("================================")

def ejecutar_submenu_expediente(opcion):
    if opcion == '1':
        buscar_por_expediente()
    elif opcion == '2':
        listar_expedientes()
    elif opcion == '3':
        listar_expedientes_libres()
    elif opcion == '4':
        while True:
            submenu_rangos_edad()
            subopcion = input("Seleccione una opción de rangos de edad: ")
            if subopcion == '1':
                listar_por_rango_edad(0, 5)
            elif subopcion == '2':
                listar_por_rango_edad(6, 12)
            elif subopcion == '3':
                listar_por_genero('M')
            elif subopcion == '4':
                listar_por_genero('F')
            elif subopcion == '5':
                listar_por_sexo_y_rango_edad()                 
            elif subopcion == '0':
                break
            else:
                print("Opción inválida, intente de nuevo.")
    elif opcion == '0':
        return False
    else:
        print("Opción inválida, intente de nuevo.")
    return True

def ejecutar_opcion(opcion):
    """Ejecuta la opción seleccionada."""
    if opcion == '1':
        nombre = input("Ingresa el nombre del miembro a buscar o agregar: ")
        coincidencias = buscar_miembro(nombre)
        if coincidencias:
            print("Coincidencias encontradas:")
            mostrar_resultados(coincidencias, editar_desde_busqueda=True)
        else:
            agregar_miembro(nombre)
    elif opcion == '2':
        nombre = input("Ingresa el nombre para buscar coincidencias: ")
        coincidencias = buscar_miembro(nombre)
        if coincidencias:
            mostrar_resultados(coincidencias, info_completa=True)
        else:
            print("No se encontró ninguna coincidencia.")
    elif opcion == '3':
        nombre = input("Ingresa el nombre de la persona para modificar: ")
        modificar_miembro(nombre)
    elif opcion == '4':
        while True:
            mostrar_submenu_expediente()
            subopcion = input("Seleccione una opción: ")
            if not ejecutar_submenu_expediente(subopcion):
                break
    elif opcion == '5':
        submenu_grupos()            
    elif opcion == '0':
        print("Saliendo del programa.")
    else:
        print("Opción inválida. Intente de nuevo.")

# Programa principal
while True:
    menu()
    opcion = input("Seleccione una opción: ")
    if opcion == '0':
        break
    ejecutar_opcion(opcion)
