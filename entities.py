import pygame
from utils import load_image, load_sound

class GameObject(pygame.sprite.Sprite): # Clase base para todos los objetos del juego
    def __init__(self, x, y, image, width=None, height=None): # Constructor de la clase
        super().__init__() # Llama al constructor de la clase base
        self.image = pygame.image.load(image) # Cargar la imagen del objeto
        if width and height: # Escalar la imagen si se especifican las dimensiones
            self.image = pygame.transform.scale(self.image, (width, height)) 
        self.rect = self.image.get_rect(topleft=(x, y)) # Obtener el rectángulo de la imagen

    def update(self): # Método para actualizar el estado del objeto
        pass 

class Player(GameObject): # Clase para el jugador
    def __init__(self, x, y): # Constructor de la clase
        super().__init__(x, y, r'E:/Code/ProyectoFinal/assets/images/jugador.png', width=75, height=75)
        self.health = 100 # Vida inicial del jugador
        self.score = 0 # Puntuación inicial del jugador
        self.powered_up = False # Estado del jugador con potenciador

    def update(self): # Método para actualizar el estado del jugador
        keys = pygame.key.get_pressed() # Obtener las teclas presionadas
        if keys[pygame.K_LEFT]: # Mover el jugador a la izquierda
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]: # Mover el jugador a la derecha
            self.rect.x += 5
        if keys[pygame.K_UP]: # Mover el jugador hacia arriba
            self.rect.y -= 5 
        if keys[pygame.K_DOWN]: # Mover el jugador hacia abajo
            self.rect.y += 5

    def shoot(self): # Método para que el jugador dispare
        return Bullet(self.rect.centerx, self.rect.top) # Crear una bala en la posición del jugador

class Enemy(GameObject): # Clase para los enemigos
    def __init__(self, x, y, image, damage): # Constructor de la clase
        super().__init__(x, y, image, width=50, height=50) # Llama al constructor de la clase base
        self.damage = damage # Daño que inflige el enemigo

    def update(self): # Método para actualizar el estado del enemigo
        self.rect.y += 6  # Velocidad de caída
        if self.rect.y > 600: 
            self.kill()  # Elimina el enemigo cuando sale de la pantalla

class PowerUp(GameObject): # Clase para los potenciadores
    def __init__(self, x, y, image, effect): # Constructor de la clase
        super().__init__(x, y, image, width=30, height=30)
        self.effect = effect # Efecto del potenciador

    def update(self): # Método para actualizar el estado del potenciador
        self.rect.y += 4  # Velocidad de caída
        if self.rect.y > 600:
            self.kill()  # Elimina el potenciador cuando sale de la pantalla

class Bullet(GameObject): # Clase para las balas
    def __init__(self, x, y): # Constructor de la clase
        super().__init__(x, y, r'E:/Code/ProyectoFinal/assets/images/bala.png', width=10, height=30)
        self.speed = -10 # Velocidad de la bala

    def update(self): # Método para actualizar el estado de la bala
        self.rect.y += self.speed # Mover la bala hacia arriba
        if self.rect.bottom < 0:
            self.kill()  # Elimina la bala cuando sale de la pantalla