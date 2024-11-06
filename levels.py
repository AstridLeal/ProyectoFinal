import pygame
from entities import Player, Enemy, PowerUp, Bullet
from random import randint # Importar función randint para generar números aleatorios
from utils import load_image, load_sound

class Level: # Clase para representar un nivel del juego
    def __init__(self, screen_width, screen_height, background_image, level_number): # Constructor de la clase
        self.screen_width = screen_width # Ancho de la pantalla
        self.screen_height = screen_height # Alto de la pantalla
        self.background = pygame.transform.scale(pygame.image.load(background_image), (screen_width, screen_height)) # Cargar imagen de fondo
        self.player = Player(screen_width // 2, screen_height - 50) # Crear instancia del jugador
        self.enemies = pygame.sprite.Group() # Grupo de enemigos
        self.powerups = pygame.sprite.Group() # Grupo de potenciadores
        self.bullets = pygame.sprite.Group() # Grupo de balas
        self.all_sprites = pygame.sprite.Group() # Grupo de todos los sprites
        self.all_sprites.add(self.player) # Añadir jugador al grupo de sprites
        self.level_number = level_number # Número de nivel
        
        # Cargar efectos de sonido
        self.shoot_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/bala.mp3') # Cargar sonido de disparo
        self.enemy_death_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/enemigo.mp3') # Cargar sonido de muerte de enemigo
        self.powerup_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/escudo.mp3') # Cargar sonido de potenciador
        self.level_up_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/nivel.mp3') # Cargar sonido de subida de nivel
        self.game_over_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/game over.mp3') # Cargar sonido de fin de juego
        self.victory_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/victory.mp3') # Cargar sonido de victoria
        self.player_damage_sound = load_sound('E:/Code/ProyectoFinal/assets/sounds/muerte.mp3') # Cargar sonido de daño al jugador

    def spawn_enemies(self): # Método para generar enemigos
        x = randint(0, self.screen_width - 50) # Posición aleatoria en el eje X
        enemy_type = randint(1, 3) # Tipo de enemigo aleatorio
        if enemy_type == 1: # Crear enemigo de tipo 1
            enemy = Enemy(x, 0, 'E:/Code/ProyectoFinal/assets/images/enemigo.png', damage=40) # Crear instancia de enemigo
        elif enemy_type == 2: # Crear enemigo de tipo 2
            enemy = Enemy(x, 0, 'E:/Code/ProyectoFinal/assets/images/fuego.png', damage=20)
        else: # Crear enemigo de tipo 3
            enemy = Enemy(x, 0, 'E:/Code/ProyectoFinal/assets/images/bomba.png', damage=30)
        self.enemies.add(enemy) # Añadir enemigo al grupo de enemigos
        self.all_sprites.add(enemy) # Añadir enemigo al grupo de todos los sprites

    def spawn_powerups(self): # Método para generar potenciadores
        x = randint(0, self.screen_width - 50) # Posición aleatoria en el eje X
        powerup_type = randint(1, 3) # Tipo de potenciador aleatorio
        if powerup_type == 1: # Crear potenciador de tipo 1
            powerup = PowerUp(x, 0, 'E:/Code/ProyectoFinal/assets/images/estrella.png', effect='points') # Crear instancia de potenciador
        elif powerup_type == 2: # Crear potenciador de tipo 2
            powerup = PowerUp(x, 0, 'E:/Code/ProyectoFinal/assets/images/escudo.png', effect='shield')
        else: # Crear potenciador de tipo 3
            powerup = PowerUp(x, 0, 'E:/Code/ProyectoFinal/assets/images/espada.png', effect='damage')
        self.powerups.add(powerup) # Añadir potenciador al grupo de potenciadores
        self.all_sprites.add(powerup) # Añadir potenciador al grupo de todos los sprites

    def update(self): # Método para actualizar el estado del nivel
        self.all_sprites.update() # Actualizar todos los sprites
        self.check_collisions() # Verificar colisiones entre los sprites
        if randint(1, 50) == 1:  # Spawnear enemigo con una probabilidad
            self.spawn_enemies() # Generar enemigo
        if randint(1, 100) == 1:  # Spawnear potenciador con una probabilidad
            self.spawn_powerups() # Generar potenciador

    def check_collisions(self): # Método para verificar colisiones entre los sprites
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True) # Colisiones entre jugador y enemigos
        for hit in hits: # Iterar sobre las colisiones
            self.player.health -= hit.damage # Restar vida al jugador
            self.player_damage_sound.play()  # Reproducir sonido de daño al jugador
            if self.player.health <= 0: # Verificar si el jugador ha muerto
                self.player.kill() # Eliminar al jugador
                pygame.mixer.music.stop()  # Detener música de fondo al morir
                self.game_over_sound.play()  # Sonido de game over
                pygame.time.delay(2000)  # Esperar 2 segundos para que el sonido termine de reproducirse
                pygame.quit()  # Salir del juego
                return  # Asegurarse de que no se ejecute más código

        pickups = pygame.sprite.spritecollide(self.player, self.powerups, True) # Colisiones entre jugador y potenciadores
        for pickup in pickups: # Iterar sobre los potenciadores recogidos
            if pickup.effect == 'points': # Verificar el efecto del potenciador
                self.player.score += 100 # Añadir puntos al jugador
            elif pickup.effect == 'shield': # Verificar el efecto del potenciador
                self.player.health += 50 # Añadir vida al jugador
            elif pickup.effect == 'damage': # Verificar el efecto del potenciador
                self.player.powered_up = True # Activar potenciador
            self.powerup_sound.play()  # Reproducir sonido de potenciador

        enemy_hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True) # Colisiones entre enemigos y balas
        for hit in enemy_hits: # Iterar sobre las colisiones
            self.player.score += 50 # Añadir puntos al jugador
            self.enemy_death_sound.play()  # Reproducir sonido de muerte de enemigo

    def render(self, screen): # Método para renderizar el nivel en pantalla
        screen.blit(self.background, (0, 0)) # Mostrar imagen de fondo
        self.all_sprites.draw(screen) # Dibujar todos los sprites en pantalla