import pygame

def map_2():
    pygame.init()
    LARGEUR, HAUTEUR = 1540, 800
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Map 2")

    # Couleur de fond
    couleur_fond = (0, 0, 255)  # Bleu

    # Boucle principale
    en_cours = True
    clock = pygame.time.Clock()
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

        # Dessiner le fond
        fenetre.fill(couleur_fond)

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Ne pas exécuter directement ce script si importé
if __name__ == "__main__":
    map_2()