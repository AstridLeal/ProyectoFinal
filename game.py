import pygame
from entities import Player, Enemy, PowerUp, Bullet
from levels import Level
from utils import load_image, load_sound

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Inicializar el mezclador de audio para reproducir sonidos
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) # Crear la ventana del juego
        pygame.display.set_caption("Space Adventure") # Establecer el título de la ventana
        self.clock = pygame.time.Clock() # Crear un reloj para controlar la velocidad de fotogramas
        self.running = True # Variable para controlar el bucle principal del juego
        self.levels = [ # Crear una lista de niveles
            Level(self.screen_width, self.screen_height, r'E:/Code/ProyectoFinal/assets/images/Fondo1.png', level_number=1),
            Level(self.screen_width, self.screen_height, r'E:/Code/ProyectoFinal/assets/images/fondo2.png', level_number=2),
            Level(self.screen_width, self.screen_height, r'E:/Code/ProyectoFinal/assets/images/fondo3.png', level_number=3)
        ]
        self.current_level = 0
        self.font = pygame.font.Font(None, 36)  # Fuente para mostrar el texto en pantalla

        # Cargar música de fondo
        pygame.mixer.music.load('E:/Code/ProyectoFinal/assets/sounds/musica de fondo.mp3')
        pygame.mixer.music.play(-1)  # Reproducir en bucle

        # Cargar efectos de sonido
        self.shoot_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/bala.mp3') # Cargar sonido de disparo
        self.enemy_death_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/enemigo.mp3') # Cargar sonido de muerte de enemigo
        self.powerup_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/escudo.mp3') # Cargar sonido de potenciador
        self.level_up_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/nivel.mp3')  # Cargar sonido de subida de nivel
        self.game_over_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/game over.mp3') # Cargar sonido de fin de juego
        self.victory_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/victory.mp3') # Cargar sonido de victoria
        self.player_damage_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/muerte.mp3') # Cargar sonido de daño al jugador

    def run(self): # Método principal para ejecutar el juego
        while self.running: # Bucle principal del juego
            self.handle_events() # Manejar eventos de entrada
            self.update() # Actualizar el estado del juego
            self.render() # Renderizar los gráficos en pantalla
            self.clock.tick(60) # Limitar la velocidad de fotogramas a 60 FPS

    def update(self): # Actualizar el estado del juego
        if self.current_level < len(self.levels): # Verificar si hay más niveles por jugar
            self.levels[self.current_level].update() # Actualizar el nivel actual
            self.check_level_progression() # Verificar si se ha completado el nivel actual
        else:
            self.running = False  # Termina el juego si se completan todos los niveles

    def check_level_progression(self): # Verificar si se ha completado el nivel actual
        score = self.levels[self.current_level].player.score # Obtener la puntuación del jugador
        if score >= 2000: 
            pygame.mixer.music.stop() # Detener música de fondo al ganar
            self.victory_sound.play()  # Sonido de victoria
            self.running = False  # Fin del juego
        elif score >= 1500 and self.current_level < 2:
            self.current_level = 2
            self.level_up_sound.play()  # Sonido de subida de nivel
        elif score >= 1000 and self.current_level < 1:
            self.current_level = 1
            self.level_up_sound.play()  # Sonido de subida de nivel
 
    def render(self): # Renderizar los gráficos en pantalla
        if self.current_level < len(self.levels): # Verificar si hay más niveles por jugar
            self.levels[self.current_level].render(self.screen) # Renderizar el nivel actual
            self.display_hud() # Mostrar el HUD en pantalla (interfaz de usuario en pantalla)
        pygame.display.flip() # Actualizar la pantalla

    def display_hud(self): # Mostrar el HUD en pantalla (interfaz de usuario en pantalla)
        player = self.levels[self.current_level].player # Obtener el jugador del nivel actual
        hud_text = f"Vida: {player.health}  Puntuación: {player.score}  Nivel: {self.current_level + 1}" # Texto del HUD
        hud_surface = self.font.render(hud_text, True, (255, 255, 255)) # Crear una superficie con el texto
        self.screen.blit(hud_surface, (10, 10)) # Mostrar el texto en pantalla

    def handle_events(self): # Manejar eventos de entrada del teclado
        for event in pygame.event.get(): # Obtener todos los eventos de la cola de eventos
            if event.type == pygame.QUIT: # Verificar si se ha cerrado la ventana
                self.running = False # Terminar el bucle principal
            elif event.type == pygame.KEYDOWN: # Verificar si se ha presionado una tecla
                if event.key == pygame.K_SPACE: # Verificar si se ha presionado la tecla de espacio (disparar)
                    bullet = self.levels[self.current_level].player.shoot() # Crear una bala
                    self.levels[self.current_level].bullets.add(bullet) # Agregar la bala al grupo de balas
                    self.levels[self.current_level].all_sprites.add(bullet) # Agregar la bala a todos los sprites
                    self.shoot_sound.play()  # Reproducir sonido de disparo