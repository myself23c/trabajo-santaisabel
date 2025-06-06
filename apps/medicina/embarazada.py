import datetime

def calcular_gestacion():
    fecha_str = input("Ingrese la fecha de la última regla (dd/mm/aaaa): ")
    try:
        fecha_ultima_regla = datetime.datetime.strptime(fecha_str, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha incorrecto. Por favor, ingrese en formato dd/mm/aaaa.")
        return

    hoy = datetime.datetime.today()
    delta = hoy - fecha_ultima_regla
    dias = delta.days
    semanas = dias // 7  # Aproximación a las semanas transcurridas

    # La fecha probable de parto se estima sumando 280 días (40 semanas) a la fecha de la última regla.
    fecha_probable_parto = fecha_ultima_regla + datetime.timedelta(days=280)

    print("\n--- Resultados ---")
    print(f"Semanas de gestación (aproximadas): {semanas} semanas")
    print("Fecha probable de parto:", fecha_probable_parto.strftime("%d/%m/%Y"))

def calcular_ultrasonido():
    fecha_ultra_str = input("Ingrese la fecha del ultrasonido (dd/mm/aaaa): ")
    try:
        fecha_ultra = datetime.datetime.strptime(fecha_ultra_str, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha incorrecto. Por favor, ingrese en formato dd/mm/aaaa.")
        return

    try:
        semanas_ultra = float(input("Ingrese las semanas de gestación que indica el ultrasonido: "))
    except ValueError:
        print("Valor inválido. Debe ser un número.")
        return

    hoy = datetime.datetime.today()
    # Calcular el incremento en semanas desde la fecha del ultrasonido hasta hoy
    delta_dias = (hoy - fecha_ultra).days
    incremento_semanas = delta_dias / 7.0

    # La gestación actual es la suma de las semanas del ultrasonido y el incremento de tiempo transcurrido
    gestacion_actual = semanas_ultra + incremento_semanas

    print("\n--- Resultados del Ultrasonido ---")
    print("Gestación actual aproximada:", round(gestacion_actual, 2), "semanas")
    print("Fecha del ultrasonido:", fecha_ultra.strftime("%d/%m/%Y"))

def main():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Calcular semanas de gestación y fecha probable de parto")
        print("2. Calcular gestación actual a partir de ultrasonido")
        print("3. Salir")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == "1":
            calcular_gestacion()
        elif opcion == "2":
            calcular_ultrasonido()
        elif opcion == "3":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
