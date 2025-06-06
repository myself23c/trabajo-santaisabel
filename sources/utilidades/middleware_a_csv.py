import pandas as pd

class CSVMiddleware:
    """
    Middleware en Python para acceder a un archivo CSV en modo solo lectura.
    Permite múltiples funciones/métodos para buscar, filtrar y obtener información del CSV.
    """

    def __init__(self, csv_path: str):
        """
        Inicializa el middleware cargando el CSV en un DataFrame de pandas.

        Args:
            csv_path (str): Ruta al archivo CSV. Se asume codificación UTF-8.
        """
        try:
            self.df = pd.read_csv(csv_path, encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta: {csv_path}")
        except Exception as e:
            raise Exception(f"Error al leer el CSV: {e}")

    def get_columns(self) -> list:
        """
        Devuelve la lista de nombres de columnas del CSV.

        Returns:
            list: Lista de strings con los nombres de las columnas.
        """
        return list(self.df.columns)

    def get_all_records(self) -> pd.DataFrame:
        """
        Retorna una copia de todo el contenido del CSV como DataFrame.

        Returns:
            pd.DataFrame: DataFrame con todas las filas y columnas.
        """
        return self.df.copy()

    def get_record_by_index(self, index: int) -> pd.Series:
        """
        Obtiene un registro específico por su índice (fila) en el DataFrame.

        Args:
            index (int): Índice de la fila.

        Returns:
            pd.Series: Serie con los valores de la fila, o None si el índice no existe.
        """
        try:
            return self.df.iloc[index]
        except IndexError:
            return None

    def find_records_by_exact_match(self, column: str, value) -> pd.DataFrame:
        """
        Busca registros donde el valor de una columna sea exactamente igual al parámetro dado.

        Args:
            column (str): Nombre de la columna a buscar.
            value: Valor exacto a comparar.

        Returns:
            pd.DataFrame: Subconjunto del DataFrame filtrado.
        """
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        return self.df[self.df[column] == value]

    def find_records_by_partial_match(self, column: str, substring: str) -> pd.DataFrame:
        """
        Busca registros donde el valor de una columna contenga una subcadena (case-insensitive).

        Args:
            column (str): Nombre de la columna a buscar.
            substring (str): Subcadena a buscar dentro del texto de la columna.

        Returns:
            pd.DataFrame: Subconjunto del DataFrame filtrado.
        """
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        mask = self.df[column].astype(str).str.contains(substring, case=False, na=False)
        return self.df[mask]

    def find_records_in_multiple_columns(self, columns: list, substring: str) -> pd.DataFrame:
        """
        Busca registros donde una subcadena aparezca en cualquiera de las columnas especificadas.

        Args:
            columns (list): Lista de nombres de columnas a recorrer.
            substring (str): Subcadena a buscar.

        Returns:
            pd.DataFrame: Subconjunto del DataFrame filtrado.
        """
        for col in columns:
            if col not in self.df.columns:
                raise ValueError(f"La columna '{col}' no existe en el CSV.")
        mask = False
        for col in columns:
            mask |= self.df[col].astype(str).str.contains(substring, case=False, na=False)
        return self.df[mask]

    def get_unique_values(self, column: str) -> list:
        """
        Obtiene los valores únicos de una columna.

        Args:
            column (str): Nombre de la columna.

        Returns:
            list: Lista de valores únicos.
        """
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        return self.df[column].dropna().unique().tolist()

    def count_records(self) -> int:
        """
        Cuenta el número total de registros (filas) en el CSV.

        Returns:
            int: Número de filas.
        """
        return len(self.df)

    def filter_records_by_condition(self, column: str, operator: str, value) -> pd.DataFrame:
        """
        Filtra registros según una condición simple: columna op valor.

        Args:
            column (str): Nombre de la columna.
            operator (str): Operador de comparación ('==', '>', '<', '>=', '<=').
            value: Valor para comparar.

        Returns:
            pd.DataFrame: Subconjunto del DataFrame filtrado.
        """
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        if operator not in ['==', '>', '<', '>=', '<=']:
            raise ValueError("Operador no válido. Use uno de: '==', '>', '<', '>=', '<='.")
        try:
            if operator == '==':
                return self.df[self.df[column] == value]
            elif operator == '>':
                return self.df[self.df[column] > float(value)]
            elif operator == '<':
                return self.df[self.df[column] < float(value)]
            elif operator == '>=':
                return self.df[self.df[column] >= float(value)]
            elif operator == '<=':
                return self.df[self.df[column] <= float(value)]
        except Exception as e:
            raise ValueError(f"Error al filtrar: {e}")


def print_menu():
    print("\n===== Menú de Opciones =====")
    print("1. Listar columnas disponibles")
    print("2. Mostrar número total de registros")
    print("3. Mostrar todos los registros (puede ser extenso)")
    print("4. Obtener registro por índice")
    print("5. Buscar registros (coincidencia exacta)")
    print("6. Buscar registros (coincidencia parcial)")
    print("7. Buscar registros en múltiples columnas")
    print("8. Obtener valores únicos de una columna")
    print("9. Filtrar registros por condición simple (columna op valor)")
    print("0. Salir")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Middleware en Python para acceder a un CSV en modo solo lectura con menú interactivo.')
    parser.add_argument('csv_path', help='Ruta al archivo CSV, por ejemplo: ./pacientes-diciembre-test-final.csv')
    args = parser.parse_args()

    try:
        db = CSVMiddleware(args.csv_path)
    except Exception as e:
        print(f"Error al inicializar el middleware: {e}")
        exit(1)

    while True:
        print_menu()
        choice = input("Seleccione una opción: ").strip()

        if choice == '1':
            cols = db.get_columns()
            print("Columnas disponibles:", cols)

        elif choice == '2':
            total = db.count_records()
            print(f"Número total de registros: {total}")

        elif choice == '3':
            df_all = db.get_all_records()
            print(df_all)

        elif choice == '4':
            idx = input("Ingrese el índice de la fila: ").strip()
            if idx.isdigit():
                record = db.get_record_by_index(int(idx))
                if record is not None:
                    print(record)
                else:
                    print("Índice fuera de rango.")
            else:
                print("Índice inválido. Debe ser un número entero.")

        elif choice == '5':
            col = input("Ingrese el nombre de la columna para búsqueda exacta: ").strip()
            val = input("Ingrese el valor exacto a buscar: ").strip()
            try:
                # Intentamos convertir a numérico si corresponde
                try:
                    val_num = float(val)
                    results = db.find_records_by_exact_match(col, val_num)
                except ValueError:
                    results = db.find_records_by_exact_match(col, val)
                print(results)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '6':
            col = input("Ingrese el nombre de la columna para búsqueda parcial: ").strip()
            substr = input("Ingrese la subcadena a buscar: ").strip()
            try:
                results = db.find_records_by_partial_match(col, substr)
                print(results)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '7':
            cols_input = input("Ingrese los nombres de columnas separados por comas: ").strip()
            cols_list = [c.strip() for c in cols_input.split(',') if c.strip()]
            substr = input("Ingrese la subcadena a buscar en las columnas: ").strip()
            try:
                results = db.find_records_in_multiple_columns(cols_list, substr)
                print(results)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '8':
            col = input("Ingrese el nombre de la columna para valores únicos: ").strip()
            try:
                unique_vals = db.get_unique_values(col)
                print(f"Valores únicos en '{col}': {unique_vals}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '9':
            col = input("Ingrese el nombre de la columna para filtrar: ").strip()
            operator = input("Ingrese operador (==, >, <, >=, <=): ").strip()
            val = input("Ingrese el valor para comparar: ").strip()
            try:
                # Intentamos convertir val a float si es posible
                try:
                    val_num = float(val)
                    results = db.filter_records_by_condition(col, operator, val_num)
                except ValueError:
                    results = db.filter_records_by_condition(col, operator, val)
                print(results)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '0':
            print("Saliendo. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente nuevamente.")
