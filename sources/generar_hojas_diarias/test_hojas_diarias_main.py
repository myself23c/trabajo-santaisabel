import curses
import os
import subprocess

# Directorio de este archivo, donde están los scripts del submenú
SCRIPT_DIR = os.path.dirname(__file__)

# Lista de scripts disponibles en este submenú
scripts = [
    'generar_total_consultas_periodo.py',
    'generar_referidos_periodo.py',
    'generar_con_sindrome_febril.py',
    'generar_consulta_embarazadas.py',
    'generar_estado_nutricional_por_edades.py',
    'generar_tabla_nutricional_por_edades.py',
    'generar_suive_valores.py',
    'consultas_diarias_por_dia.py',
    'generar_hojadiaria_excel_por_fecha.py',
    'generar_dumpeo_csv_a_excel_fecha.py'
]


def run_script(script_name):
    """
    Ejecuta el script seleccionado en una terminal separada,
    usando la ruta absoluta y estableciendo el directorio de trabajo
    para resolver rutas relativas dentro de los scripts.
    """
    curses.endwin()
    try:
        script_path = os.path.join(SCRIPT_DIR, script_name)
        # Ejecutar con cwd en SCRIPT_DIR para que las rutas relativas funcionen
        subprocess.run(['python3', script_path], check=True, cwd=SCRIPT_DIR)
    finally:
        input("\nPresiona Enter para regresar al menú principal...")
        curses.doupdate()


def main_menu(stdscr):
    """
    Interfaz del submenú para ejecutar los scripts de Hojas Diarias.
    """
    # Configuración de curses
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.keypad(True)

    # Pares de colores
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Título
        title = "📋 Hojas Diarias"
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, w//2 - len(title)//2, title)
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Opciones
        for idx, script in enumerate(scripts):
            x = 2
            y = 3 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, script)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, script)
                stdscr.attroff(curses.color_pair(2))

        stdscr.refresh()

        key = stdscr.getch()
        if key in (ord('q'), 27):  # 'q' o ESC para volver al menú principal
            break
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(scripts) - 1:
            current_row += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            run_script(scripts[current_row])

    # Restaurar al salir
    stdscr.keypad(False)
    curses.echo()
