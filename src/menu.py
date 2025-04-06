import pygame
import sys
from PIL import Image

# Fonction pour afficher le menu
def menu():
    pygame.init()
    largeur_fenetre = 1540
    hauteur_fenetre = 800
    screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("Menu Principal")

    # Couleurs
    gris_fonce = (64, 78, 92)
    gris = (169, 169, 169)
    couleur_bouton = (255, 222, 89)
    fond_transparent = (255, 255, 255, 128)  # gris_fonce avec transparence (alpha 128)

    # Charger le GIF
    try:
        background_menu = Image.open("ressources/menu/bg_menu.gif")
    except FileNotFoundError:
        print("Erreur : Fichier 'bg_menu.gif' introuvable.")
        pygame.quit()
        sys.exit()

    # Convertir le GIF en une liste de frames Pygame
    frames = []
    for frame in range(background_menu.n_frames):
        background_menu.seek(frame)
        frame_image = pygame.image.fromstring(background_menu.tobytes(), background_menu.size, background_menu.mode)
        frame_image = pygame.transform.scale(frame_image, (largeur_fenetre, hauteur_fenetre))
        frames.append(frame_image)

    # Initialiser l'index de la frame
    frame_idx = 0

    # Police pour le texte
    font = pygame.font.Font("ressources/fonts/RetroFunk.otf", 30)

    # Définir les positions des boutons (horizontal)
    bouton_width = 300
    bouton_height = 60
    espace_entre_boutons = 20  # Espacement entre les boutons
    total_bouton_width = (bouton_width * 2) + espace_entre_boutons
    start_x = (largeur_fenetre // 2) - (total_bouton_width // 2)  # Centre les boutons horizontalement
    bouton_y = hauteur_fenetre // 1.5 - 30  # Position verticale commune

    bouton_play_rect = pygame.Rect(start_x, bouton_y, bouton_width, bouton_height)
    bouton_quit_rect = pygame.Rect(start_x + bouton_width + espace_entre_boutons, bouton_y, bouton_width, bouton_height)

    # Paramètre emplacement bouton Settings
    settings_x = largeur_fenetre - bouton_width - 10
    settings_y = 15
    bouton_settings_rect = pygame.Rect(settings_x, settings_y, bouton_width, bouton_height)

    # Taille du fond semi-transparent (plus grand pour englober les boutons)
    fond_boutons_rect = pygame.Rect(
        start_x - 20, bouton_y - 20, total_bouton_width + 40, bouton_height + 40)  # Adjusted size

    # Boucle du menu
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Vérifie si l'utilisateur a cliqué
                    if bouton_play_rect.collidepoint(event.pos):
                        return "play"  # Retourne "play" si le bouton "Play" est cliqué
                    elif bouton_quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()  # Quitter le jeu

        # Remplir l'écran avec la couleur grise
        screen.fill(gris)

        # Afficher le GIF
        screen.blit(frames[frame_idx], (0, 0))

        # Créer une surface transparente
        surface_transparente = pygame.Surface((fond_boutons_rect.width, fond_boutons_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface_transparente, fond_transparent, surface_transparente.get_rect(), border_radius=30)
        screen.blit(surface_transparente, fond_boutons_rect.topleft)

        # Dessiner les boutons avec des coins arrondis
        pygame.draw.rect(screen, couleur_bouton, bouton_play_rect, border_radius=15)  # Bouton "Play"
        pygame.draw.rect(screen, couleur_bouton, bouton_quit_rect, border_radius=15)  # Bouton "Quit"
        pygame.draw.rect(screen, couleur_bouton, bouton_settings_rect, border_radius=15)  # Bouton "Settings"

        # Ajouter du texte aux boutons
        texte_play = font.render("Play", True, gris_fonce)
        texte_quit = font.render("Quit", True, gris_fonce)
        texte_settings = font.render("Settings", True, gris_fonce)
        screen.blit(texte_play, (bouton_play_rect.centerx - texte_play.get_width() // 2, bouton_play_rect.centery - texte_play.get_height() // 2))
        screen.blit(texte_quit, (bouton_quit_rect.centerx - texte_quit.get_width() // 2, bouton_quit_rect.centery - texte_quit.get_height() // 2))
        screen.blit(texte_settings, (bouton_settings_rect.centerx - texte_settings.get_width() // 2, bouton_settings_rect.centery - texte_settings.get_height() // 2))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Passer à la prochaine image du GIF
        frame_idx = (frame_idx + 1) % len(frames)  # Revenir à la première frame après la dernière

        # Contrôler la vitesse de l'animation
        pygame.time.Clock().tick(15)  # 15 images par seconde pour une animation fluide

    pygame.quit()
    return None  # Si l'utilisateur ferme la fenêtre