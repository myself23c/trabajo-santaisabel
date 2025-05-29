def get_prevention_data():
    def validate_input(prompt, valid_options, allow_any=False):
        while True:
            user_input = input(prompt).strip().lower()
            if allow_any or user_input == "0" or user_input in valid_options:
                return user_input
            print(f"Entrada no válida. Las opciones válidas son: {', '.join(valid_options)} o '0'. Inténtalo de nuevo.")

    prevention_data = {}


    

    prevention_data['primera_vez_ano'] = validate_input(
        "Es primera vez en el año? (si/no): ",
        ['si', 'no']
    )
    prevention_data['relacion_temporal'] = validate_input(
        "Relación temporal por motivo: (primera-vez/subsecuente): ",
        ['primera-vez', 'subsecuente']
    )

    prevention_data['nutricion'] = validate_input(
        "Estado nutricional del paciente : (desnutricion/bajo-peso/peso-normal/sobrepeso/obesidad): ",
        ['desnutricion', 'bajo-peso' , 'peso-normal', 'sobrepeso', 'obesidad']
    )

    prevention_data['febril'] = validate_input(
        "hay sospecha de sindrome febril? (nofebril/sindromefebril): ",
        ['nofebril', 'sindromefebril']
    )

    prevention_data['embarazada'] = validate_input(
        "paciente embarazada? (sinembarazo/embarazada): ",
        ['sinembarazo', 'embarazada']
    )

    prevention_data['dm2'] = validate_input(
        "Es diabetico? (si/no): ",
        ['si', 'no']
    )

    prevention_data['has'] = validate_input(
        "Es hipertenso? (si/no): ",
        ['si', 'no']
    )

    prevention_data['eda'] = validate_input(
        "viene por infeccion de gastrointestinal? (si/no): ",
        ['si', 'no']
    )

    prevention_data['ira'] = validate_input(
        "viene por infeccion de vias respiratorias? (si/no): ",
        ['si', 'no']
    )

    prevention_data['asma'] = validate_input(
        "viene por asma? (si/no): ",
        ['si', 'no']
    )   
    
    prevention_data['conjuntivitis'] = validate_input(
        "viene por conjuntivitis? (si/no): ",
        ['si', 'no']
    )   
    
    prevention_data['otitis'] = validate_input(
        "viene por otitis? (si/no): ",
        ['si', 'no']
    )   


    prevention_data['deteccion_salud_mental'] = validate_input(
        "Detección de salud mental? (no/psicosocial/farmacologico/ambos): ",
        ['no', 'psicosocial', 'farmacologico', 'ambos']
    )
    prevention_data['folio_receta'] = validate_input(
        "Escribir folio de la receta: ",
        [],
        allow_any=True
    )
    prevention_data['promocion_de_la_salud'] = validate_input(
        "Promoción de la salud presenta cartilla? (sipresenta/nopresenta): ",
        ['sipresenta', 'nopresenta']
    )
    prevention_data['linea_vida'] = validate_input(
        "Consulta línea de vida? (si/no): ",
        ['si', 'no']
    )
    prevention_data['esquema_vacunacion'] = validate_input(
        "Promoción de la salud, tiene esquema de vacunación completo? (norealizada/esquemacompleto/esquemaincompleto): ",
        ['norealizada', 'esquemacompleto', 'esquemaincompleto']
    )
    prevention_data['referido'] = validate_input(
        "Es referido? (noreferido/referido): ",
        ['noreferido', 'referido']
    )
    prevention_data['deteccion_adicciones'] = validate_input(
        "Detección de adicciones salió positiva y a cuál? (norealizada/alcohol/tabaco/farmacos/cannabis/cocaina/metanfetaminas/inhalables/opiaceos/tranquilizantes): ",
        ['norealizada', 'alcohol', 'tabaco', 'farmacos', 'cannabis', 'cocaina', 'metanfetaminas', 'inhalables', 'opiaceos', 'tranquilizantes']
    )
    prevention_data['deteccion_violencia_mujer'] = validate_input(
        "Detección violencia hacia la mujer 15 años o más? (norealizada/sinviolencia/violencia): ",
        ['norealizada', 'sinviolencia', 'violencia']
    )
    prevention_data['prueba_edi'] = validate_input(
        "EDI TIPO (norealizada/inicial/subsecuente): ",
        ['norealizada', 'inicial', 'subsecuente']
    )
    prevention_data['resultado_edi'] = validate_input(
        "RESULTADO EDI (NOREALIZADA: 0, INICIAL: 1. VERDE, 2.AMARILLO, 3.ROJO; SUBSECUENTE: 4.RECUPERADO DE REZAGO, 5.RECUPERADO DE RIESGO DE RETRASO, 6.EN SEGUIMIENTO): ",
        ['norealizada', '1', '2', '3', '4', '5', '6']
    )
    prevention_data['resultado_battelle'] = validate_input(
        "RESULTADO BATTELLE (0. NOREALIZADA, 1.MAYOR O IGUAL A 90, 2.DE 89 A 80, 3.MENOR O IGUAL A 79): ",
        ['0', '1', '2', '3']
    )
    prevention_data['eda_tratamiento'] = validate_input(
        "EDA PLAN TRATAMIENTO (0.norealizada, 1.A, 2.B, 3.C): ",
        ['0', '1', '2', '3']
    )
    prevention_data['ira_tratamiento'] = validate_input(
        "IRA TRATAMIENTO (no/sintomatico/antibiotico): ",
        ['no', 'sintomatico', 'antibiotico']
    )
    prevention_data['aplicacion_cedula_cancer_ano'] = validate_input(
        "APLICACIÓN DE CÉDULA CÁNCER EN EL AÑO (norealizada/primera/segunda): ",
        ['norealizada', 'primera', 'segunda']
    )
    prevention_data['INTERVENCIONES_GERONTOLOGICAS'] = validate_input(
        "INTERVENCIONES GERONTOLÓGICAS (1.SINTOMATOLOGÍA DEPRESIVA PREVENTIVA, 2.ALTERACIONES DE LA MEMORIA PREVENTIVA, 3.ACTIVIDADES INSTRUMENTALES Y ACTIVIDADES BÁSICAS DE LA VIDA DIARIA PREVENTIVA, 4.SÍNDROME DE CAÍDAS PREVENTIVA, 5.INCONTINENCIA URINARIA PREVENTIVA, 6.MOTRICIDAD PREVENTIVA, 7.ASESORÍA NUTRICIONAL PREVENTIVA, 8.SINTOMATOLOGÍA DEPRESIVA TRATAMIENTO, 9.ALTERACIONES DE LA MEMORIA TRATAMIENTO, 10.ACTIVIDADES INSTRUMENTALES Y ACTIVIDADES BÁSICAS DE LA VIDA DIARIA TRATAMIENTO, 11.SÍNDROME DE CAÍDAS TRATAMIENTO, 12.INCONTINENCIA URINARIA TRATAMIENTO, 13.MOTRICIDAD TRATAMIENTO, 14.ASESORÍA NUTRICIONAL TRATAMIENTO): ",
        [str(i) for i in range(1, 15)]
    )
    prevention_data['alergia'] = validate_input(
        "Alergia a algún medicamento? (no/a cuál?): ",
        [],
        allow_any=True
    )

    prevention_data['telefono'] = validate_input(
        "se requiere saber numero de telefono? (no/cual es?): ",
        [],
        allow_any=True
    )



    prevention_data['CHISME'] = validate_input(
        ">>>>>>Algún chisme: ",
        [],
        allow_any=True
    )

    return prevention_data
