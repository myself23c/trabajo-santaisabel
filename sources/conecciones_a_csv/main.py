import os
import sys
import importlib.util
from csv_middleware import CSVMiddleware

# Nombre del CSV por defecto (UTF-8)
CSV_PATH = './pacientes-diciembre-test-final.csv'

# Carpeta actual (módulos al mismo nivel)
WORKDIR = os.path.dirname(os.path.abspath(__file__))

# Intentar inicializar la base de datos CSV
try:
    db = CSVMiddleware(CSV_PATH)
except Exception as e:
    print(f"Error al inicializar el middleware: {e}")
    sys.exit(1)

# Cargar dinámicamente todos los archivos .py (excepto main.py y csv_middleware.py)
modules = {}
for filename in os.listdir(WORKDIR):
    if filename.endswith('.py') and filename not in ('main.py', 'csv_middleware.py'):
        module_name = filename[:-3]
        filepath = os.path.join(WORKDIR, filename)
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            if hasattr(module, 'run') and callable(module.run):
                modules[module_name] = module.run
        except Exception:
            pass

# Menú automático basado en archivos detectados
def print_menu():
    print("\n===== Menú de Opciones =====")
    for i, key in enumerate(sorted(modules.keys()), start=1):
        print(f"{i}. {key}.py")
    print("0. Salir")

# Guía rápida de operadores para el usuario
print("Guía rápida en caso de usar consultas lógicas (JS-like):")
print("  Comparaciones: ==, !=, >, <, >=, <=")
print("  Lógicos JS: && (AND), || (OR)")
print("  Para nombres de columnas use comillas dobles \"columna\". Ej: \"nombre\" == \"juan\"")

while True:
    print_menu()
    choice = input("Seleccione una opción: ").strip()
    if choice == '0':
        print("Saliendo. ¡Hasta luego!")
        break
    try:
        idx = int(choice) - 1
        key = sorted(modules.keys())[idx]
        modules[key](db)
    except (ValueError, IndexError):
        print("Opción no válida. Intente nuevamente.")
    except Exception as e:
        print(f"Error al ejecutar {key}.py: {e}")