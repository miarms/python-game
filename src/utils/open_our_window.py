import pygame
def open_our_window():
    pygame.init()
    
    largeur_ecran = 1540
    hauteur_ecran = 800
    fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
    pygame.QUIT()
open_our_window()