import random

def jugar_rps():
    """
    Ejecuta una ronda de Piedra, Papel o Tijera.
    """
    print("\n--- 🗿 Piedra, 📄 Papel o ✂️ Tijera ---")
    opciones = ["piedra", "papel", "tijera"]

    # 1. Entrada del usuario
    usuario = input("👉 Elige una opción (piedra, papel, tijera): ").lower().strip()

    # Validación básica
    if usuario not in opciones:
        print(f"❌ Error: '{usuario}' no es válido. Por favor escribe piedra, papel o tijera.")
        return

    # 2. Elección de la computadora
    computadora = random.choice(opciones)
    print(f"🤖 Computadora eligió: {computadora}")

    # 3. Lógica del juego (IMPLEMENTADA)
    
    # Caso 1: Empate
    if usuario == computadora:
        print("⚖️ ¡Es un empate!")
    
    # Caso 2: Usuario gana (Todas las combinaciones ganadoras)
    # Piedra gana a Tijera  O  Papel gana a Piedra  O  Tijera gana a Papel
    elif (usuario == "piedra" and computadora == "tijera") or \
         (usuario == "papel" and computadora == "piedra") or \
         (usuario == "tijera" and computadora == "papel"):
        print("🏆 ¡Felicidades! Tú ganas.")
    
    # Caso 3: Si no es empate y no ganaste, entonces perdiste
    else:
        print("💻 La computadora gana. ¡Suerte para la próxima!")

def main():
    # Bucle principal para jugar varias veces
    while True:
        jugar_rps()
        
        # Preguntar si quiere jugar otra vez
        seguir = input("\n¿Quieres jugar otra vez? (s/n): ").lower()
        if seguir != 's':
            print("¡Gracias por jugar! 👋")
            break

if __name__ == "__main__":
    main()