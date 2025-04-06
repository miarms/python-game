import pygame
from src.map.map_1 import map_1
def jeu():
    pygame.init()
    largeur_ecran = 1540  # Or get these values from elsewhere if needed
    hauteur_ecran = 800
    fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    fenetre.fill((0, 0, 0))  # Fill with black color (RGB)
    pygame.display.flip()    # Update the display to show the black screen

    print("en jeu")

if __name__ == '__main__':
    jeu()
    