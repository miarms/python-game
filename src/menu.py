import pygame
import sys
import os
from PIL import Image

def afficher_gif_avec_pillow(chemin_gif, largeur_fenetre=1280, hauteur_fenetre=800):
    """
    Affiche un GIF animé en utilisant Pillow et Pygame.
    """
    pygame.init()
    screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("GIF avec Pillow")

    try:
        gif = Image.open(chemin_gif)
    except FileNotFoundError:
        print(f"Erreur : Fichier GIF non trouvé à {chemin_gif}")
        pygame.quit()
        sys.exit()

    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
        frame_image = pygame.transform.scale(frame_image, (largeur_fenetre, hauteur_fenetre))
        frames.append(frame_image)

    frame_idx = 0
    en_cours = True
    clock = pygame.time.Clock()

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
        screen.blit(frames[frame_idx], (0, 0))
        pygame.display.flip()
        frame_idx = (frame_idx + 1) % len(frames)
        clock.tick(15)
    pygame.quit()

if __name__ == "__main__":
    # Utilisation du chemin absolu direct
    chemin_gif = "C:\\Users\\pater\\Documents\\GitHub\\python-game\\ressources\\menu\\bg_menu.gif"

    afficher_gif_avec_pillow(chemin_gif)