import pygame
import sys
from PIL import Image
from .jeu import jeu

def cinematique():
    pygame.init()
    largeur_fenetre = 1540
    hauteur_fenetre = 800
    screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

    # Charger le GIF
    try:
        background_menu = Image.open("ressources/gif/cinematique.gif")
    except FileNotFoundError:
        print("Erreur : Fichier 'cinematique.gif' introuvable.")
        pygame.quit()
        sys.exit()

    # Convertir le GIF en une liste de frames Pygame
    frames = []
    for frame in range(background_menu.n_frames):
        background_menu.seek(frame)
        frame_image = pygame.image.fromstring(background_menu.tobytes(), background_menu.size, background_menu.mode)
        frame_image = pygame.transform.scale(frame_image, (largeur_fenetre, hauteur_fenetre))
        frames.append(frame_image)

    frame_idx = 0
    gif_playing = True  # Add a flag to control GIF playing

    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gif_playing = False  # Stop playing the GIF
                screen.fill((255, 255, 255))
                jeu()
                en_cours = False
                return  # Importantly, exit the cinematique function

        # Remplir l'écran avec la couleur blanche
        screen.fill((255, 255, 255))

        # Afficher le GIF only if gif_playing is True
        if gif_playing:
            screen.blit(frames[frame_idx], (0, 0))
            pygame.display.flip()  # update l'affichage
            frame_idx = (frame_idx + 1) % len(frames)  # Anime gif
            pygame.time.delay(50)  # Controle vitesse du gif

    pygame.quit()
    return None