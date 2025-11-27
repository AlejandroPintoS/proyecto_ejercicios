import argparse
import sys
from typing import Dict
from collections import defaultdict

def validar_secuencia(secuencia: str) -> str:
    """
    Valida que la secuencia de ADN contenga únicamente caracteres permitidos (A, T, C, G).

    Utiliza operaciones de conjuntos para una verificación eficiente.

    Args:
        secuencia (str): La secuencia de ADN a validar.

    Returns:
        str: La secuencia validada en mayúsculas.

    Raises:
        ValueError: Si la secuencia contiene caracteres distintos a A, T, C, G o está vacía.
    """
    secuencia_upper = secuencia.upper()
    
    if not secuencia_upper:
        raise ValueError("La secuencia proporcionada está vacía.")

    # Optimización: Usar sets es mucho más rápido que iterar caracter por caracter
    bases_validas = set("ATCG")
    bases_encontradas = set(secuencia_upper)
    
    # Si hay bases encontradas que no están en las validas, restarlas nos da las inválidas
    bases_invalidas = bases_encontradas - bases_validas
    
    if bases_invalidas:
        raise ValueError(f"Caracteres inválidos encontrados: {', '.join(bases_invalidas)}")
    
    return secuencia_upper

def contar_kmers(secuencia: str, k: int) -> Dict[str, int]:
    """
    Cuenta la frecuencia de cada k-mer en la secuencia dada.

    Args:
        secuencia (str): Secuencia de ADN validada.
        k (int): Longitud del k-mer (substring).

    Returns:
        Dict[str, int]: Diccionario donde la clave es el k-mer y el valor es su frecuencia.

    Raises:
        ValueError: Si k es menor que 1 o mayor que la longitud de la secuencia.
    """
    if k < 1:
        raise ValueError("El tamaño del k-mer (k) debe ser un entero positivo mayor a 0.")
    
    n = len(secuencia)
    if k > n:
        raise ValueError(f"El tamaño del k-mer ({k}) no puede ser mayor que la longitud de la secuencia ({n}).")

    # defaultdict simplifica el código eliminando el 'if key in dict'
    kmers = defaultdict(int)
    
    # Rango: desde 0 hasta largo - k + 1
    for i in range(n - k + 1):
        kmer = secuencia[i : i + k]
        kmers[kmer] += 1
        
    return dict(kmers)

def main():
    parser = argparse.ArgumentParser(description="Herramienta para contar k-mers en una secuencia de ADN.")
    parser.add_argument("secuencia", type=str, help="Secuencia de ADN (texto plano, ej: ATCGGTA).")
    parser.add_argument("-k", "--kmer_size", type=int, default=3, help="Tamaño del k-mer (Entero > 0. Por defecto: 3).")
    
    args = parser.parse_args()
    
    try:
        # Validación de entrada
        secuencia_valida = validar_secuencia(args.secuencia)
        
        # Proceso principal
        kmers_contados = contar_kmers(secuencia_valida, args.kmer_size)
        
        # Salida: Ordenamos por frecuencia (descendente) y luego alfabéticamente para mejor lectura
        print(f"--- Frecuencia de {args.kmer_size}-mers (Total únicos: {len(kmers_contados)}) ---")
        print("K-mer\tCount")
        
        # Ordenar: primero por conteo (descendiente), luego por k-mer (alfabético)
        for kmer, conteo in sorted(kmers_contados.items(), key=lambda item: (-item[1], item[0])):
            print(f"{kmer}\t{conteo}")

    except ValueError as e:
        print(f"Error de Validación: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()