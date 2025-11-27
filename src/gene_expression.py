import pandas as pd
import argparse
import sys
import os
from typing import Optional

def cargar_datos(ruta_archivo: str) -> pd.DataFrame:
    """
    Carga los datos de expresión génica desde un archivo TSV.

    Valida que el archivo exista y que no esté vacío.

    Args:
        ruta_archivo (str): La ruta del archivo TSV a cargar.

    Returns:
        pd.DataFrame: Un DataFrame de pandas con los datos cargados.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta especificada.
        pd.errors.EmptyDataError: Si el archivo está vacío.
        Exception: Para otros errores de lectura (permisos, formato corrupto).
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo '{ruta_archivo}' no fue encontrado.")

    try:
        # Se usa sep='\t' para TSV. Si tus archivos tienen cabecera, header=0 es default.
        df = pd.read_csv(ruta_archivo, sep="\t")
        return df
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"El archivo '{ruta_archivo}' está vacío.")
    except Exception as e:
        raise Exception(f"Error al leer el archivo: {e}")

def filtrar_genes_por_expresion(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Filtra los genes cuyo valor de expresión es mayor o igual al umbral dado.

    Realiza validación de columnas y limpieza de datos no numéricos.

    Args:
        df (pd.DataFrame): DataFrame con al menos las columnas 'gene' y 'expression'.
        threshold (float): Valor mínimo de expresión requerido.

    Returns:
        pd.DataFrame: DataFrame filtrado y ordenado por nombre del gen.

    Raises:
        ValueError: Si faltan las columnas requeridas en el DataFrame.
    """
    # 1. Validación de columnas requeridas
    columnas_requeridas = {'gene', 'expression'}
    if not columnas_requeridas.issubset(df.columns):
        columnas_faltantes = columnas_requeridas - set(df.columns)
        raise ValueError(f"El archivo no contiene las columnas requeridas: {columnas_faltantes}")

    # 2. Conversión segura a numérico
    # 'coerce' convierte valores no válidos (como texto "NA" o errores) en NaN
    df['expression'] = pd.to_numeric(df['expression'], errors='coerce')

    # 3. Limpieza de datos: Eliminar filas donde 'expression' sea NaN
    filas_iniciales = len(df)
    df_limpio = df.dropna(subset=['expression'])
    
    # Opcional: Advertencia si se eliminaron datos corruptos
    filas_eliminadas = filas_iniciales - len(df_limpio)
    if filas_eliminadas > 0:
        print(f"Advertencia: Se ignoraron {filas_eliminadas} filas con valores de expresión no numéricos.", file=sys.stderr)

    # 4. Filtrado
    df_filtrado = df_limpio[df_limpio['expression'] >= threshold].copy()
    
    return df_filtrado.sort_values(by='gene')

def main():
    parser = argparse.ArgumentParser(description="Filtra genes por nivel de expresión desde un archivo TSV.")
    parser.add_argument("archivo", type=str, help="Ruta al archivo TSV con columnas 'gene' y 'expression'.")
    parser.add_argument("-t", "--threshold", type=float, required=True, help="Umbral (float) de expresión mínima.")
    
    args = parser.parse_args()

    try:
        print(f"--- Procesando archivo: {args.archivo} con threshold: {args.threshold} ---")
        
        df = cargar_datos(args.archivo)
        df_filtrado = filtrar_genes_por_expresion(df, args.threshold)

        if df_filtrado.empty:
            print("Ningún gen cumple con el criterio de filtrado.")
        else:
            # Imprimir encabezado para claridad
            print("gene\texpression")
            for _, row in df_filtrado.iterrows():
                print(f"{row['gene']}\t{row['expression']}")
                
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error de Datos: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()