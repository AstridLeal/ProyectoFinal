import pygame
from game import Game

def main():
    pygame.init()  # Inicializa todos los módulos de Pygame
    game = Game()  # Crea una instancia de la clase Game, que maneja el juego
    game.run()  # Llama al método run() para iniciar el juego
    pygame.quit()  # Limpia y cierra todos los módulos de Pygame cuando el juego termina

if __name__ == "__main__":
    main()  # Ejecuta la función main() si el script se ejecuta directamente