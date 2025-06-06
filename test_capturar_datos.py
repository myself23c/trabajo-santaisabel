import csv
import os
from datetime import datetime
from test_hoja_diaria_acciones_test import get_prevention_data
import json
from sources.utilidades.patient_utils import find_last_consultation


def validar_entrada_numerica(prompt):
    while True:
        entrada = input(prompt)
        try:
            if entrada == "0" or float(entrada):  # Permitir 0 y números decimales
                return entrada
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número válido o 0.")


def validar_entrada_texto(prompt):
    while True:
        entrada = input(prompt)
        if entrada.strip():  # Permitir cualquier texto no vacío
            return entrada
        print("Entrada no válida. Por favor, ingresa un texto válido.")


def validar_fecha(prompt):
    while True:
        entrada = input(prompt)
        try:
            if entrada == "0":
                return entrada
            datetime.strptime(entrada, "%d/%m/%Y")  # Cambiado a formato dd/mm/aaaa
            return entrada
        except ValueError:
            print("Fecha no válida. Debe estar en formato dd/mm/aaaa o ser 0.")


def get_input_or_default(prompt, defaults):
    options = "\n".join([f"{i + 1}: {default}" for i, default in enumerate(defaults)])
    full_prompt = f"{prompt} (Elige una opción o deja en blanco para escribir tu propio texto):\n{options}\n> "
    response = input(full_prompt)
    if response.isdigit() and 1 <= int(response) <= len(defaults):
        return defaults[int(response) - 1]
    return response if response else input(f"{prompt}: ")


def create_csv(data, filename):
    file_exists = os.path.isfile(filename)

    if file_exists:
        # Leer encabezados existentes
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if 'ID' not in fieldnames:
                fieldnames = ['ID'] + fieldnames
    else:
        # Crear encabezados nuevos desde el diccionario
        fieldnames = ['ID'] + list(data.keys())

    # Asegurarse de que todos los campos estén incluidos
    for key in data:
        if key not in fieldnames:
            fieldnames.append(key)

    # Contar filas existentes para asignar ID
    if file_exists:
        with open(filename, 'r', encoding='utf-8') as f:
            num_lines = sum(1 for _ in f) - 1  # excluir encabezado
    else:
        num_lines = 0

    # Escribir datos
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        data_with_id = {'ID': num_lines}
        data_with_id.update(data)

        writer.writerow(data_with_id)




def main():
    while True:
        print("\nIntroduce los siguientes datos:\n")

        
        nombres = validar_entrada_texto("Nombres: ")
        apellido_paterno = validar_entrada_texto("Apellido paterno: ")
        apellido_materno = validar_entrada_texto("Apellido materno: ")
        nombre = nombres + " " + apellido_paterno + " " + apellido_materno
        edad = validar_entrada_numerica("Edad: ")
        sexo = validar_entrada_texto("Sexo(H: hombre, M: mujer): ")
        lugar_nacimiento = validar_entrada_texto("Lugar de Nacimiento: ")
        fecha_nacimiento = validar_fecha("Fecha de Nacimiento (dd/mm/aaaa): ")
        ultima_consulta = find_last_consultation(nombre, fecha_nacimiento) # funcion para buscar la ultima consulta del paciente y sus datos
        print(ultima_consulta)
        curp = input("CURP: ")
        numero_de_expediente = validar_entrada_numerica("Poner número de expediente: ")

        fecha_consulta = datetime.now().strftime("%d/%m/%Y")
        hora_consulta = datetime.now().strftime("%H:%M:%S")

        peso = validar_entrada_numerica("Peso en kilos: ")
        talla = validar_entrada_numerica("Talla en metros, ej. 1.5: ")
        

        peso_float_temporal = float(peso)
        talla_float_temporal = float(talla)
        imc_temporal = peso_float_temporal / (talla_float_temporal * talla_float_temporal)
        print(f">>> El imc es(recuerdalo):> {imc_temporal} <" )
        cc = input("cc no se que sea: ")
        fc = validar_entrada_numerica("Frecuencia Cardiaca (FC): ")
        ta = input("Tensión Arterial (TA): ")
        temp = validar_entrada_numerica("Temperatura (TEMP): ")
        dxtx = validar_entrada_numerica("Destroxis (DXTX): ")
        fr = validar_entrada_numerica("Frecuencia Respiratoria (FR): ")

        p_defaults = ["PACIENTE SIN ANTECEDENTES DE IMPORTANCIA, NIEGA ENFERMEDADES CRONICODEGENERATIVAS, NIEGA ALERGIA A MEDICAMENTOS"]
        p = get_input_or_default("Plan (P)", p_defaults)

        s_defaults = ["[F]PACIENTE ACUDE A LA CONSULTA EXTERNA POR REFERIR DOLOR FARINGEO DE 2 DIAS DE EVOLUCION ACOMPAÑADO DE CEFALEA ESCURRIMIENTO NASAL DE COLOR VERDE SIN TEMPERATURA, Y TOS CON FLEMAS NIEGA DIFICULTAD PARA RESPIRAR O SINTOMATOLOGI GRAVE","[C]PACIENTE ACUDE A LA CONSULTA POR PRESENTAR DOLORES ABDOMINALES LEVES CON LEVE INFALAMCION DEL MISMO QUE AUMENTA AL COMER COSAS IRRITANTES, NIEGA DIARREA, VOMITOS O FIEBRE"]
        s = get_input_or_default("Subjetivo (S)", s_defaults)

        o_neuro_defaults = ["PACIENTE CONCIENTE REACTIVO EN SUS 3 ESFERAS NEUROLOGICAS, COOPERADOR AL MOMENTO DE ATENDERLO, NO DATOS DE ALTERACIONES"]
        o_neuro = get_input_or_default("Neurológico (O_Neuro)", o_neuro_defaults)

        o_cabeza_defaults = ["[N]MUCOSAS HIDRATADAS DE BUEN COLOR, FARINGE NORMAL NO DATOS DE INFECCION ACTIVA, CUELLO SIN GANGLIOS PALPABLES","[F]MUCOSAS HIDRATAS DE BUEN COLOR, FARINGE HIPERICAS, NO PRESENCIA DE SECRECION PURULENTA","[A]MUCOSAS HIDRATAS DE BUEN COLOR FARINGE CON SECRECION PURULENTA, AMIGDALAS HIPRETROFICAS","[C]MUCOSAS CON LEVE DESHIDRATACION, FARINGE NORMAL NO DATOS DE INFECCION ACTIVA"]
        o_cabeza = get_input_or_default("Cabeza (O_Cabeza)", o_cabeza_defaults)

        o_torax_defaults = ["TORAX CON MURMULLO VESICULAR PRESENTE SIN AGREGADOS, CON BUENA ENTRADA Y SALIDA DE AIRE, AMPLEXION Y AMPLEXACION CORRECTOS SIN DATOS DE DIFICULTAD RESPIRATORIA ACTIVA"]
        o_torax = get_input_or_default("Tórax (O_Torax)", o_torax_defaults)

        o_abdomen_defaults = ["[N]ABDOMEN BLANDO DEPRESIBLE NO DOLOROSO A LA PALPACION PROFUNDA O LEVE, NO SE PALPAN TUMORACIONES, BORDE HEPATICO CORRECTO, PERITALSIS CORRECTA, MCBURNEY NEGATIVO ,JORDANO NEGATIVO NO DATOS DE IRRITACION PERITONEAL EN ESTE MOMENTO O SINTOMATOLOGIA DE ABDOMEN AGUDO, NO SE PALPAN HERNIAS", "[COLITIS]ABDOMEN BLANDO DEPRESIBLE TIMPANICO, LEVEMENTE DOLOROSO A LA PALPACION LEVE,PERISTALSIS AUMENTADA, NO SE PALPAN TUMORACIONES, BORDE HEPATICO CORRECTO, PERITALSIS CORRECTA, MCBURNEY NEGATIVO ,JORDANO NEGATIVO NO DATOS DE IRRITACION PERITONEAL EN ESTE MOMENTO O SINTOMATOLOGIA DE ABDOMEN AGUDO, NO SE PALPAN HERNIAS"]
        o_abdomen = get_input_or_default("Abdomen (O_Abdomen)", o_abdomen_defaults)

        o_extremidades_defaults = ["[N]PACIENTE CON EXTREMIDADES INTEGRAS NO DATOS DE EDEMA O PROBLEMAS VASCULARES O NEURALGIAS, PULSO PEDIO PRESENTA, NO PRESENCIAS DE ULCERAS EN PIES O PLANTAS DE LAS MISMAS, NO DATOS DE INFECCION MICOTICA"]
        o_extremidades = get_input_or_default("Extremidades (O_Extremidades)", o_extremidades_defaults)

        a_defaults = ["[F]PACIENTE QUE POR SI SINTOMATOLOGIA DE DOLOR FARINGEO, ESCURRIMIENTO NASAL SIN FIEBRE SE LLEGA A LA CONCLUSION DE PACIENTE CURSANDO CON FARINGITIS VIRAL SIN DATOS DE ALARMA","[A] PACIENTE QUE POR SU SINTOMATOLOGIA ARTRALGIAS MIALGIAS Y SECRECION PURULENTA SE LLEGA A LA CONSLUSION DE PACIENTE CON AMIGDALITIS", "[C] PACIENTE EL CUAL CON SU SINTOMATOLOGIA DE COLICOS ABDOMIANLES INFLAMACION DEL MISMO SIN DIARREA O TEMPERATURA SE LLEGA A LA CONLUSION DE QUE CURSA CON COLITIS"]
        a = get_input_or_default("Análisis (A)", a_defaults)

        diagnostico_defaults = ["Texto por defecto Diagnóstico"]
        diagnostico = get_input_or_default("Diagnóstico", diagnostico_defaults)

        tratamiento_defaults = ["[F] PARACETAMOL 1X8 POR 3 DIAS, LORATADINA 1X12 POR 4 DIAS, AMBROXOL 8MLX8 POR 5 DIAS", "[A]METAMIZOL SODICO 1X8 POR 4 DIAS REPOSO Y ABUNDANTES LIQUIDOS, AMOXICILINA CON ACIDO CLAVULANICO 1X8 POR 6 DIAS REPOSO Y TOMAR ABUNDANTES LIQUIDOS"]
        tratamiento = get_input_or_default("Tratamiento", tratamiento_defaults)

        medicamentos = []
        for i in range(1, 4):
            nombre_medicamento = input(f"Nombre del medicamento {i}: ")
            dosis_medicamento = input(f"Dosis del medicamento {i}: ")
            medicamentos.append(f"{nombre_medicamento}: {dosis_medicamento}")

        p2_defaults = ["pronostico bueno"]
        p2 = get_input_or_default("Pronóstico: ", p2_defaults)

        peso_float = float(peso)
        talla_float = float(talla)
        imc = peso_float / (talla_float * talla_float)

        data = {
            'nombre': nombre,
            'nombres': nombres,
            'apellido_paterno': apellido_paterno,
            'apellido_materno': apellido_materno,
            'edad': edad,
            'sexo': sexo,
            'lugar_de_nacimiento': lugar_nacimiento,
            'fecha_de_nacimiento': fecha_nacimiento,
            'curp': curp,
            'numero_de_expediente': numero_de_expediente,
            'fecha_consulta': fecha_consulta,
            'hora': hora_consulta,
            'peso': peso,
            'talla': talla,
            'tension_arterial': ta,
            'fc': fc,
            'fr': fr,
            'temperatura': temp,
            'dxtx': dxtx,
            'imc': imc,
            'cc': cc,
            'plan': p,
            'subjetivo': s,
            'neurologico': o_neuro,
            'cabeza': o_cabeza,
            'torax': o_torax,
            'abdomen': o_abdomen,
            'extremidades': o_extremidades,
            'analisis': a,
            'diagnostico': diagnostico,
            'tratamiento': tratamiento,
            'medicamentos': '; '.join(medicamentos),
            'pronostico': p2
        }

        prevention_data = get_prevention_data()
        data.update(prevention_data)

        csv_filename = "pacientes-diciembre-test-final.csv"

        create_csv(data, csv_filename)

        cont = input("¿Quieres añadir otra entrada? (s/n): ")
        if cont.lower() != 's':
            break


if __name__ == "__main__":
    main()
