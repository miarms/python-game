import pygame
from src.menu import menu
from src.cinematique import cinematique
from src.jeu import jeu

def open_our_window():
    pygame.init()
    BLANC = (255, 255, 255)
    largeur_ecran = 1540
    hauteur_ecran = 800
    fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))

    etat = "menu"  # L'état initial est le menu
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if etat == "menu":
            action = menu()
            if action == "play":
                etat = "cinematique"
            elif action == "quit":
                etat = "quitter"
                running = False
        elif etat == "cinematique":
            action = cinematique()
            if action == "jeu":
                etat = "jeu"
        elif etat == "jeu":
            # Placeholder for game logic
            jeu()
        elif etat == "quitter":
            running = False

        pygame.display.flip()

    pygame.quit()