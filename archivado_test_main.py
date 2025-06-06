import curses
import subprocess
#from sources.generar_hojas_diarias.hojas_diarias_main import mostrar_submenu

# Lista de scripts disponibles\   
scripts = [
    'test_capturar_datos.py',
    'test_generar_nota_acciones.py',
    'test_receta_pdf.py',
    'imprimir-ubuntu.py',
    'test_solicitud_laboratorios.py',
    'test-solicitud-imagenologia.py',
    "imprimir_unico_archivo.py",
 #   'mostrar_submenu'
    
]





def run_script(script):
    """Ejecuta el script seleccionado en una terminal separada."""
    curses.endwin()
    try:
        subprocess.run(['python3', script])
    finally:
        input("\nPresiona Enter para regresar al menú principal...")
        curses.doupdate()


def main_menu(stdscr):
    """Interfaz principal que permite seleccionar y ejecutar scripts."""
    # Configuración inicial
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.cbreak()
    stdscr.keypad(True)

    # Definir pares de colores (fondo, texto)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # Selección resaltada
    curses.init_pair(2, curses.COLOR_YELLOW, -1)                # Título
    curses.init_pair(3, curses.COLOR_GREEN, -1)                 # Pie de página

    current_row = 0
    h, w = stdscr.getmaxyx()

    while True:
        stdscr.clear()

        # Título centrado
        title = "📂 Selector de Scripts"
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(1, w//2 - len(title)//2, title)
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

        # Instrucciones
        instruction = "Usa ↑/↓ y Enter para seleccionar. 'q' para salir."
        stdscr.addstr(3, w//2 - len(instruction)//2, instruction)

        # Crear ventana de menú
        menu_h = len(scripts) + 2
        menu_w = max(len(s) for s in scripts) + 4
        start_y = h//2 - menu_h//2
        start_x = w//2 - menu_w//2
        menu_win = curses.newwin(menu_h, menu_w, start_y, start_x)
        menu_win.keypad(True)
        menu_win.box()

        # Mostrar opciones
        for idx, script in enumerate(scripts):
            x = 2
            y = 1 + idx
            if idx == current_row:
                menu_win.attron(curses.color_pair(1))
                menu_win.attron(curses.A_BOLD)
                menu_win.addstr(y, x, script)
                menu_win.attroff(curses.A_BOLD)
                menu_win.attroff(curses.color_pair(1))
            else:
                menu_win.addstr(y, x, script)

        stdscr.attron(curses.color_pair(3))
        footer = "Mi App Interactiva - v1.0"
        stdscr.addstr(h-2, w//2 - len(footer)//2, footer)
        stdscr.attroff(curses.color_pair(3))

        stdscr.refresh()
        menu_win.refresh()

        # Esperar input
        key = menu_win.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(scripts) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            stdscr.clear()
            msg = f"Ejecutando {scripts[current_row]}..."
            stdscr.addstr(h//2, w//2 - len(msg)//2, msg)
            stdscr.refresh()
            run_script(scripts[current_row])

    # Restaurar configuración
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()

if __name__ == "__main__":
    curses.wrapper(main_menu)
