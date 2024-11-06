import pygame

def load_image(filename): # Función para cargar imágenes
    return pygame.image.load(filename) # Cargar imagen desde el archivo especificado

def load_sound(filename): # Función para cargar sonidos
    return pygame.mixer.Sound(filename) # Cargar sonido desde el archivo especificado
