import argparse
import sys
import os
from collections import Counter
from typing import Dict, Tuple

def obtener_argumentos() -> argparse.Namespace:
    """Configura y obtiene los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Calcula la frecuencia de bases (A, T, C, G) en un archivo FASTA."
    )
    parser.add_argument(
        "archivo", 
        type=str, 
        help="Ruta al archivo FASTA de entrada."
    )
    return parser.parse_args()

def leer_fasta(ruta_archivo: str) -> str:
    """
    Lee un archivo FASTA y concatena las líneas de secuencia.
    Ignora las líneas de encabezado que comienzan con '>'.

    Args:
        ruta_archivo (str): Ruta del archivo.

    Returns:
        str: Cadena con la secuencia cruda (puede contener saltos de línea).
    
    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo '{ruta_archivo}' no fue encontrado.")

    secuencia_fragmentos = []
    
    try:
        with open(ruta_archivo, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith(">"):
                    continue
                secuencia_fragmentos.append(linea)
    except Exception as e:
        raise IOError(f"Error leyendo el archivo: {e}")

    return "".join(secuencia_fragmentos)

def limpiar_y_validar(secuencia: str) -> str:
    """
    Convierte a mayúsculas y valida que solo existan bases ATCG.
    
    Args:
        secuencia (str): Secuencia cruda.
        
    Returns:
        str: Secuencia limpia.
        
    Raises:
        ValueError: Si encuentra caracteres no válidos.
    """
    secuencia_upper = secuencia.upper()
    bases_validas = set("ATCG")
    
    # Verificación rápida de caracteres extraños
    bases_presentes = set(secuencia_upper)
    if not bases_presentes.issubset(bases_validas):
        invalidas = bases_presentes - bases_validas
        raise ValueError(f"La secuencia contiene caracteres inválidos: {invalidas}")
        
    return secuencia_upper

def calcular_frecuencias(secuencia: str) -> Tuple[int, Dict[str, float]]:
    """
    Calcula el porcentaje de aparición de cada base.

    Returns:
        Tuple[int, Dict[str, float]]: Longitud total y diccionario con porcentajes.
    """
    total = len(secuencia)
    if total == 0:
        return 0, {}
    
    conteo = Counter(secuencia)
    frecuencias = {base: (count / total) * 100 for base, count in conteo.items()}
    
    return total, frecuencias

def main():
    args = obtener_argumentos()

    try:
        # 1. Lectura
        secuencia_raw = leer_fasta(args.archivo)
        
        # 2. Limpieza y Validación
        secuencia_clean = limpiar_y_validar(secuencia_raw)
        
        # 3. Cálculo
        total_bases, frecuencias = calcular_frecuencias(secuencia_clean)
        
        # 4. Salida
        print(f"--- Resultados para: {args.archivo} ---")
        print(f"Longitud de secuencia: {total_bases} bp")
        print("Frecuencias:")
        for base in sorted(frecuencias.keys()):
            print(f"  {base}: {frecuencias[base]:.2f}%")

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