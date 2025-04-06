import pygame
import sys
from PIL import Image

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

    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                en_cours = False
         # Remplir l'écran avec la couleur grise
        screen.fill(255, 255, 255)

        # Afficher le GIF
        screen.blit(frames[frame_idx], (0, 0))
def main():
    cinematique()
main()