import curses
import os
import subprocess

# Lista de scripts disponibles
scripts = ['generar_total_consultas_periodo.py', 'generar_referidos_periodo.py' , 'generar_con_sindrome_febril.py',  'generar_consulta_embarazadas.py' ,  'generar_estado_nutricional_por_edades.py' ,  'generar_tabla_nutricional_por_edades.py',  'generar_suive_valores.py' ,  'consultas_diarias_por_dia.py' ,  'generar_hojadiaria_excel_por_fecha.py']

def run_script(script):
    """Ejecuta el script seleccionado en una terminal separada."""
    curses.endwin()  # Salir temporalmente de curses
    try:
        subprocess.run(['python3', script])  # Ejecuta el script seleccionado
    finally:
        input("Presiona Enter para regresar al menú principal...")  # Espera a que el usuario presione Enter
        curses.initscr()  # Vuelve a iniciar curses


def main_menu(stdscr):
    """Interfaz principal que permite seleccionar y ejecutar scripts."""
    curses.curs_set(0)
    curses.start_color()  # Iniciar el modo color en curses

    # Definir colores personalizados
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Texto verde sobre fondo negro
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Texto blanco para opciones no seleccionadas

    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Selecciona un script para ejecutar (Usa las flechas ↑ ↓ y Enter):")

        # Mostrar opciones
        for idx, script in enumerate(scripts):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))  # Resaltar en verde
                stdscr.addstr(idx + 2, 0, script)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))  # Texto blanco para opciones no seleccionadas
                stdscr.addstr(idx + 2, 0, script)
                stdscr.attroff(curses.color_pair(2))

        key = stdscr.getch()

        # Navegar con flechas
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(scripts) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter para seleccionar
            stdscr.clear()
            stdscr.addstr(0, 0, f"Ejecutando {scripts[current_row]}...")
            stdscr.refresh()
            run_script(scripts[current_row])
            stdscr.addstr(2, 0, "Presiona cualquier tecla para regresar al menú principal.")
            stdscr.getch()

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main_menu)