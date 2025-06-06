import os
import sys
import curses
import subprocess
import importlib

# Para que Python encuentre el paquete sources desde la raíz del proyecto
sys.path.insert(0, os.getcwd())

# Definimos los elementos del menú con tipo y destino
enhanced_menu_items = [
    {"label": ">> Capturar datos del paciente <<",           "type": "file",    "target": "test_capturar_datos.py"},
    {"label": "> Generar nota medica",    "type": "file",    "target": "test_generar_nota_acciones.py"},
    {"label": "> Generar Receta PDF",               "type": "file",    "target": "test_receta_pdf.py"},
    {"label": "> Imprimir Ubuntu receta y nota medica ala vez",          "type": "file",    "target": "imprimir-ubuntu.py"},
    {"label": "-+Generar consulta *subcecuente* o de *evolucion*",            "type": "file",    "target": "crear_nueva_consulta_subsecuente_fake.py"},
    {"label": "-Generar Solicitud LABs",            "type": "file",    "target": "test_solicitud_laboratorios.py"},
    {"label": "-Generar Solicitud Imagenología",   "type": "file",    "target": "test-solicitud-imagenologia.py"},
    {"label": "-Generar historia clinica",   "type": "file",    "target": "generar_historia_clinica.py"},
    {"label": "-Imprimir un único archivo generado","type": "file",    "target": "imprimir_unico_archivo.py"},
    {"label": "[TODOS]>submenu< Imprimir papeleria formatos en blanco exp,enfermeria etc.",   "type": "file",    "target": "imprimir_formatos_en_blanco_papeleria.py"},
    {"label": "[TODOS]>submenu< buscar expedientes csv +numero de exp, apellidos de la familia, etc","type": "file",    "target": "buscar_expedientes_csv.py"},
    {"label": ">submenu< generador de Hojas Diarias del doctor juan",            "type": "submenu","module": "sources.generar_hojas_diarias.test_hojas_diarias_main","func": "main_menu"},
     {
        "label": ">submenu< Buscador Pacientes e informacion del doctor juan",
        "type":   "submenu",
        "module": "sources.buscador_pacientes.buscador_pacientes_main",
        "func":   "main_menu"
    },
    
    {"label": "[TODOS]+DETECCIONES+ Ver lista de pacientes ID por fecha y sexo",   "type": "file",    "target": "detecciones_lista_id.py"},
    {"label": "[TODOS]+DETECCIONES+ Generar detecciones unicas en el año de un paciente",   "type": "file",    "target": "detecciones_generador.py"},
    {"label": "[TODOS]+DETECCIONES+ Imprimir detecciones",   "type": "file",    "target": "imprimir_detecciones.py"},
    {"label": "*Acceso a la base de datos",   "type": "file",    "target": "sources/conecciones_a_csv/main.py"},
    {"label": "Recordatorios de informacion por fecha",   "type": "file",    "target": "sources/utilidades/menu_recordatorios.py"},
    
]

def run_script(path):
    """Ejecuta el script seleccionado en una terminal separada."""
    curses.endwin()
    try:
        subprocess.run(['python3', path], check=True)
    finally:
        input("\nPresiona Enter para regresar al menú…")
        curses.doupdate()


def main_menu(stdscr):
    """Interfaz principal que permite seleccionar y ejecutar scripts o submenús."""
    # Configuración inicial de curses
    curses.curs_set(0)
    curses.start_color()               # Habilitar colores
    curses.use_default_colors()        # Permitir fondo por defecto (-1)
    stdscr.keypad(True)

    # Definir pares de colores (fondo, texto)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # Selección resaltada
    curses.init_pair(2, curses.COLOR_YELLOW, -1)                # Título
    curses.init_pair(3, curses.COLOR_GREEN, -1)                 # Pie de página

    current = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Título centrado
        title = "📂 Selector de Scripts"
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(1, w//2 - len(title)//2, title)
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

        # Instrucciones
        instruction = "Usa ↑/↓ y Enter para seleccionar. 'q' o ESC para salir."
        stdscr.addstr(3, w//2 - len(instruction)//2, instruction)

        # Ventana de menú
        menu_h = len(enhanced_menu_items) + 2
        menu_w = max(len(item["label"]) for item in enhanced_menu_items) + 4
        start_y = h//2 - menu_h//2
        start_x = w//2 - menu_w//2
        menu_win = curses.newwin(menu_h, menu_w, start_y, start_x)
        menu_win.keypad(True)
        menu_win.box()

        # Mostrar opciones
        for idx, item in enumerate(enhanced_menu_items):
            x = 2
            y = 1 + idx
            label = item["label"]
            if idx == current:
                menu_win.attron(curses.color_pair(1) | curses.A_BOLD)
                menu_win.addstr(y, x, label)
                menu_win.attroff(curses.A_BOLD)
                menu_win.attroff(curses.color_pair(1))
            else:
                menu_win.addstr(y, x, label)

        # Pie de página
        footer = "Mi App de consulta de santa isabel dr.munoz"
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(h-2, w//2 - len(footer)//2, footer)
        stdscr.attroff(curses.color_pair(3))

        stdscr.refresh()
        menu_win.refresh()

        # Capturar entrada
        key = menu_win.getch()
        if key in (ord('q'), 27):  # 'q' o ESC para salir
            break
        elif key == curses.KEY_UP and current > 0:
            current -= 1
        elif key == curses.KEY_DOWN and current < len(enhanced_menu_items) - 1:
            current += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = enhanced_menu_items[current]
            if selected["type"] == "file":
                run_script(selected["target"])
            else:
                # Import dinámico para el submenú: ejecutar main_menu del módulo cargado
                try:
                    module = importlib.import_module(selected["module"])
                    func = getattr(module, selected["func"])
                except (ImportError, AttributeError) as e:
                    curses.endwin()
                    print(f"Error al cargar el submenú: {e}")
                    input("\nPresiona Enter para continuar…")
                    curses.doupdate()
                else:
                    func(stdscr)

    # Restaurar configuración al salir
    stdscr.keypad(False)
    curses.echo()

if __name__ == "__main__":
    curses.wrapper(main_menu)
