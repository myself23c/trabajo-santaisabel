import csv
import os
from datetime import datetime

CSV_FILENAME = "pacientes-diciembre-test-final.csv"


def validar_entrada_texto(prompt):
    while True:
        entrada = input(prompt)
        if entrada.strip():
            return entrada
        print("Entrada no válida. Por favor, ingresa un texto válido.")


def validar_fecha_consulta(prompt):
    while True:
        entrada = input(prompt)
        try:
            fecha = datetime.strptime(entrada, "%d/%m/%Y")
            if fecha.weekday() >= 5:  # 5 = sábado, 6 = domingo
                print("La fecha no puede ser sábado ni domingo. Elige un día entre lunes y viernes.")
                continue
            return entrada
        except ValueError:
            print("Fecha no válida. Debe estar en formato dd/mm/aaaa. Intenta de nuevo.")


def cargar_todos_pacientes(filename):
    """
    Lee todo el archivo CSV y regresa una lista de diccionarios,
    donde cada diccionario es una fila (un paciente o consulta) con sus columnas.
    """
    if not os.path.isfile(filename):
        print(f"No existe el archivo {filename}.")
        return []

    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def obtener_paciente_por_id(pacientes, id_buscar):
    """
    Busca en la lista de diccionarios el que tenga 'ID' igual a id_buscar (como string).
    Regresa el diccionario de ese paciente o None si no se encuentra.
    """
    for row in pacientes:
        if row.get('ID') == str(id_buscar):
            return row
    return None


def obtener_ultimo_paciente(pacientes):
    """
    Regresa el último diccionario de la lista (última fila del CSV),
    o None si la lista está vacía.
    """
    if not pacientes:
        return None
    return pacientes[-1]


def create_csv(data, filename):
    """
    Similar a la función original: agrega al CSV una fila nueva con todos los campos de 'data'.
    Asigna un nuevo ID basado en el número de filas existentes.
    """
    file_exists = os.path.isfile(filename)

    if file_exists:
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            if 'ID' not in fieldnames:
                fieldnames = ['ID'] + fieldnames
    else:
        fieldnames = ['ID'] + list(data.keys())

    # Asegurar que todos los campos de 'data' estén en los encabezados
    for key in data:
        if key not in fieldnames:
            fieldnames.append(key)

    # Contar filas existentes (excluyendo encabezado)
    if file_exists:
        with open(filename, 'r', encoding='utf-8') as f:
            num_lines = sum(1 for _ in f) - 1
    else:
        num_lines = 0

    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        data_with_id = {'ID': num_lines}
        data_with_id.update(data)
        writer.writerow(data_with_id)


def main():
    pacientes = cargar_todos_pacientes(CSV_FILENAME)
    if not pacientes:
        print("No hay registros para consultas subsecuentes.")
        return

    print("¿Quieres generar una consulta subsecuente?")
    respuesta = input("(s/n): ").strip().lower()
    if respuesta != 's':
        print("Operación cancelada.")
        return

    # Pedir si usar ID o último paciente
    print("\nPara basar la consulta en un paciente existente, ingresa su ID.")
    print("Si deseas usar el último paciente registrado, deja en blanco y presiona Enter.")
    entrada_id = input("ID del paciente (o Enter para último): ").strip()

    if entrada_id == "":
        paciente_base = obtener_ultimo_paciente(pacientes)
        if paciente_base is None:
            print("No se encontró ningún paciente en el archivo.")
            return
        print(f"Usando al último paciente con ID = {paciente_base['ID']}.")
    else:
        if not entrada_id.isdigit():
            print("ID inválido. Debe ser un número entero.")
            return
        paciente_base = obtener_paciente_por_id(pacientes, int(entrada_id))
        if paciente_base is None:
            print(f"No se encontró paciente con ID = {entrada_id}.")
            return
        print(f"Usando al paciente con ID = {entrada_id}.")

    # Mostrar datos esenciales del paciente seleccionado
    print("\n--- Datos del paciente seleccionado ---")
    print(f"Nombre: {paciente_base.get('nombre', '')}")
    print(f"Edad: {paciente_base.get('edad', '')}")
    print(f"Sexo: {paciente_base.get('sexo', '')}")
    print(f"Fecha última consulta: {paciente_base.get('fecha_consulta', '')}")
    print(f"Diagnóstico: {paciente_base.get('diagnostico', '')}")
    print("---------------------------------------")

    # Copiar todos los campos del paciente seleccionado
    nueva_consulta = paciente_base.copy()
    # Eliminar 'ID' para que create_csv asigne uno nuevo
    if 'ID' in nueva_consulta:
        nueva_consulta.pop('ID')

    # Solicitar nueva información de la consulta
    print("\n--- Datos para la nueva consulta subsecuente ---")
    fecha_consulta = validar_fecha_consulta("Fecha de consulta (dd/mm/aaaa, lunes a viernes): ")
    hora_consulta = datetime.now().strftime("%H:%M:%S")

    subjetivo = validar_entrada_texto("Subjetivo (S): ")
    analisis = validar_entrada_texto("Análisis (A): ")
    diagnostico = validar_entrada_texto("Diagnóstico: ")
    tratamiento = validar_entrada_texto("Tratamiento: ")

    # Variables fijas para consulta subsecuente
    primera_vez_ano = "no"
    relacion_temporal = "subsecuente"

    # Sobrescribir en el dict todos los campos que cambian
    nueva_consulta['fecha_consulta'] = fecha_consulta
    nueva_consulta['hora'] = hora_consulta
    nueva_consulta['subjetivo'] = subjetivo
    nueva_consulta['analisis'] = analisis
    nueva_consulta['diagnostico'] = diagnostico
    nueva_consulta['tratamiento'] = tratamiento
    nueva_consulta['primera_vez_ano'] = primera_vez_ano
    nueva_consulta['relacion_temporal'] = relacion_temporal

    # Agregar la nueva fila al CSV
    create_csv(nueva_consulta, CSV_FILENAME)
    print(f"\nConsulta subsecuente agregada para paciente base ID = {paciente_base['ID']}.")


if __name__ == "__main__":
    main()
