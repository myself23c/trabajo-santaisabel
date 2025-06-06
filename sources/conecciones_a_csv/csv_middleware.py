import pandas as pd
import re

class CSVMiddleware:
    """Middleware en Python para acceder a un archivo CSV en modo solo lectura.
    Permite múltiples funciones/métodos para buscar, filtrar y obtener información del CSV,
    incluyendo consultas con condiciones lógicas avanzadas, todo insensible a mayúsculas/minúsculas."""

    def __init__(self, csv_path: str):
        """Inicializa el middleware cargando el CSV en un DataFrame de pandas.
        Args:
            csv_path (str): Ruta al archivo CSV. Se asume codificación UTF-8."""
        try:
            self.df = pd.read_csv(csv_path, encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta: {csv_path}")
        except Exception as e:
            raise Exception(f"Error al leer el CSV: {e}")

    def get_columns(self) -> list:
        """Devuelve la lista de nombres de columnas del CSV."""
        return list(self.df.columns)

    def get_all_records(self) -> pd.DataFrame:
        """Retorna una copia de todo el contenido del CSV como DataFrame."""
        return self.df.copy()

    def get_record_by_index(self, index: int) -> pd.Series:
        """Obtiene un registro específico por su índice (fila) en el DataFrame."""
        try:
            return self.df.iloc[index]
        except IndexError:
            return None

    def find_records_by_exact_match(self, column: str, value) -> pd.DataFrame:
        """
        Busca registros donde el valor de una columna coincida exactamente con 'value',
        sin importar mayúsculas/minúsculas.
        """
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        # Convertimos todo a string, pasamos a minúsculas y comparamos
        mask = self.df[column].astype(str).str.lower() == str(value).lower()
        return self.df[mask]

    def find_records_by_partial_match(self, column: str, substring: str) -> pd.DataFrame:
        """Busca registros donde el valor de una columna contenga una subcadena, ignorando mayúsculas."""
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        mask = self.df[column].astype(str).str.contains(substring, case=False, na=False)
        return self.df[mask]

    def find_records_in_multiple_columns(self, columns: list, substring: str) -> pd.DataFrame:
        """Busca registros donde una subcadena aparezca en cualquiera de las columnas especificadas, ignorando mayúsculas."""
        for col in columns:
            if col not in self.df.columns:
                raise ValueError(f"La columna '{col}' no existe en el CSV.")
        mask = False
        for col in columns:
            mask |= self.df[col].astype(str).str.contains(substring, case=False, na=False)
        return self.df[mask]

    def get_unique_values(self, column: str) -> list:
        """Obtiene los valores únicos de una columna."""
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        return self.df[column].dropna().unique().tolist()

    def count_records(self) -> int:
        """Cuenta el número total de registros (filas) en el CSV."""
        return len(self.df)

    def filter_records_by_condition(self, column: str, operator: str, value) -> pd.DataFrame:
        """
        Filtra registros según una condición simple: columna op valor,
        insensible a mayúsculas/minúsculas cuando se comparan cadenas.
        Operadores válidos: '==', '!=', '>', '<', '>=', '<='.
        """
        if column not in self.df.columns:
            raise ValueError(f"La columna '{column}' no existe en el CSV.")
        if operator not in ['==', '!=', '>', '<', '>=', '<=']:
            raise ValueError("Operador no válido. Use uno de: '==', '!=', '>', '<', '>=', '<='.")

        try:
            # Determinamos si la columna es numérica o de texto
            dtype_col = self.df[column].dtype
            is_numeric = pd.api.types.is_numeric_dtype(dtype_col)

            if operator == '==':
                if is_numeric:
                    return self.df[self.df[column] == float(value)]
                else:
                    return self.df[self.df[column].astype(str).str.lower() == str(value).lower()]

            elif operator == '!=':
                if is_numeric:
                    return self.df[self.df[column] != float(value)]
                else:
                    return self.df[self.df[column].astype(str).str.lower() != str(value).lower()]

            elif operator in ['>', '<', '>=', '<=']:
                # Para comparaciones numéricas, convertimos a float.
                # Si la columna no es numérica, intentamos convertir a float.
                try:
                    series_num = self.df[column].astype(float)
                    valor_num = float(value)
                except Exception:
                    raise ValueError(f"No se puede comparar '{column}' con '{value}' usando '{operator}' (no numérico).")
                if operator == '>':
                    return self.df[series_num > valor_num]
                elif operator == '<':
                    return self.df[series_num < valor_num]
                elif operator == '>=':
                    return self.df[series_num >= valor_num]
                elif operator == '<=':
                    return self.df[series_num <= valor_num]

        except Exception as e:
            raise ValueError(f"Error al filtrar: {e}")

    def filter_by_logical_query(self, expression: str, return_columns: list = None) -> pd.DataFrame:
        """
        Filtra registros según una expresión lógica tipo JavaScript, insensible a mayúsculas/minúsculas.

        - Se soportan operadores: ==, !=, >, <, >=, <=
        - Operadores lógicos JS: && (AND), || (OR)
        - Nombres de columnas entre comillas dobles: "columna"
        - Los literales de texto entre comillas se convierten a minúsculas antes de comparar.
        Ejemplo de expresión válida:
            '"Nombre" == "juan" && "Edad" > 25'
        """
        # 1) Reemplazamos && → and y || → or
        expr_py = expression.replace('&&', 'and').replace('||', 'or')

        # 2) Encontramos todos los tokens entre comillas dobles
        tokens = re.findall(r'"([^"]+)"', expr_py)
        columnas_en_expr = set()
        literales_en_expr = set()

        for token in tokens:
            if token in self.df.columns:
                columnas_en_expr.add(token)
            else:
                literales_en_expr.add(token)

        # 3) Creamos un DataFrame temporal para agregar columnas en minúscula
        df_temp = self.df.copy()
        for col in columnas_en_expr:
            col_lower = f"{col}_lower"
            df_temp[col_lower] = df_temp[col].astype(str).str.lower()

        # 4) Reemplazamos cada "columna" con la referencia a su versión en minúscula
        def reemplazar_token(match):
            token = match.group(1)
            if token in columnas_en_expr:
                # Reemplazamos por `col_lower`
                return f'`{token}_lower`'
            else:
                # Literal de texto: convertimos a minúsculas y lo ponemos como cadena
                return f"'{token.lower()}'"

        expr_py = re.sub(r'"([^"]+)"', reemplazar_token, expr_py)

        try:
            # Ejecutamos la consulta sobre df_temp. Query usará las columnas *_lower para comparar.
            df_filtrado_temp = df_temp.query(expr_py)
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión lógica: {e}")

        # 5) Obtenemos el índice de los registros que cumplen la condición
        idx_validos = df_filtrado_temp.index

        # 6) Si se especifican columnas de retorno, las validamos y seleccionamos
        if return_columns:
            for col in return_columns:
                if col not in self.df.columns:
                    raise ValueError(f"La columna '{col}' no existe en el CSV.")
            return self.df.loc[idx_validos, return_columns]

        # Devolvemos todas las columnas de los registros filtrados
        return self.df.loc[idx_validos]

