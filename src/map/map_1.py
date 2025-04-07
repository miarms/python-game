# tuile.py
import pygame
import os
from src.map.map_2 import map_2
from src.BoiteDialogue import BoiteDialogue
def map_1():
    # Initialisation de Pygame (sera déjà fait dans main.py, mais on le laisse ici pour compatibilité)
    pygame.init()

    # Taille de la fenêtre
    LARGEUR, HAUTEUR = 1540, 800
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Carte de la maison")

    # Obtenir le chemin du dossier contenant le script
    chemin_script = os.path.dirname(os.path.abspath(__file__))
    chemin_tileset = os.path.join(chemin_script, "TilesetHouse.png")

    # Charger le tileset
    tileset = pygame.image.load(chemin_tileset).convert_alpha()

    # Dictionnaire pour stocker les tuiles découpées
    tuiles = {}

    # Fonction pour extraire une tuile à une position donnée
    def extraire_tuile(x, y, largeur, hauteur):
        return tileset.subsurface((x, y, largeur, hauteur))

    # Découpage manuel des tuiles
    tuiles["mur"] = extraire_tuile(360, 64, 32, 32)  # Mur
    tuiles["sol"] = extraire_tuile(310, 80, 32, 32)  # Sol
    tuiles["porte"] = extraire_tuile(360, 105, 32, 32)  # Porte torii
    tuiles["table"] = extraire_tuile(200, 200, 32, 32)  # Table

    # Représentation de la carte (0 = mur, 1 = sol, 2 = porte, 3 = table, 4 = vide)
    TAILLE_TUILE = 32
    carte = [
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]

    # Position initiale du joueur
    joueur_x, joueur_y = 760, 400
    VITESSE = 5
    num_map = 1
    # Gestion du dialogue
    boite_dialogue = BoiteDialogue("data/dialogue_map_1.json", (100, 650),
                                 (1050, 700), (0,0,0), (255, 255, 255),
                                 (255, 222, 89))
    dialogue_en_cours = False
    # Boucle principale
    en_cours = True
    clock = pygame.time.Clock()

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            boite_dialogue.gerer_evenement(event)
        # Déplacement du joueur
        if not boite_dialogue.actif:
            touches = pygame.key.get_pressed()
            nouveau_x, nouveau_y = joueur_x, joueur_y
            if touches[pygame.K_LEFT]:
                nouveau_x -= VITESSE
            if touches[pygame.K_RIGHT]:
                nouveau_x += VITESSE
            if touches[pygame.K_UP]:
                nouveau_y -= VITESSE
            if touches[pygame.K_DOWN]:
                nouveau_y += VITESSE

        # Vérifier les collisions avec les murs
        joueur_rect = pygame.Rect(nouveau_x - 10, nouveau_y - 10, 20, 20)
        collision = False
        for y, ligne in enumerate(carte):
            for x, tuile in enumerate(ligne):
                if tuile == 0:  # Mur
                    mur_rect = pygame.Rect(x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE)
                    if joueur_rect.colliderect(mur_rect):
                        collision = True
                        break
                elif tuile == 3:  # Table (obstacle)
                    table_rect = pygame.Rect(x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE)
                    if joueur_rect.colliderect(table_rect):
                        collision = True
                        break
                elif tuile == 4:  # Vide (obstacle)
                    vide = pygame.Rect(x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE)
                    if joueur_rect.colliderect(vide):
                        collision = True
                        break
                elif tuile == 2: #Porte
                    porte_rect = pygame.Rect(x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE)
                    if joueur_rect.colliderect(porte_rect):
                        num_map == 2
                        map_2()
            if collision:
                break

        if not collision:
            joueur_x, joueur_y = nouveau_x, nouveau_y

        # Limiter le joueur à la fenêtre
        joueur_x = max(0, min(joueur_x, LARGEUR - 20))
        joueur_y = max(0, min(joueur_y, HAUTEUR - 20))

        
        if num_map == 1 and not dialogue_en_cours:
            boite_dialogue.actif = True
            dialogue_en_cours = True

        # Dessiner la carte
        fenetre.fill((0, 0, 0))  # Fond noir

        # Dessiner les tuiles
        for y, ligne in enumerate(carte):
            for x, tuile in enumerate(ligne):
                if tuile == 0:  # Mur
                    fenetre.blit(tuiles["mur"], (x * TAILLE_TUILE, y * TAILLE_TUILE))
                elif tuile == 1:  # Sol
                    fenetre.blit(tuiles["sol"], (x * TAILLE_TUILE, y * TAILLE_TUILE))
                elif tuile == 2:  # Porte
                    fenetre.blit(tuiles["porte"], (x * TAILLE_TUILE, y * TAILLE_TUILE))
                elif tuile == 3:  # Table
                    fenetre.blit(tuiles["table"], (x * TAILLE_TUILE, y * TAILLE_TUILE))

        # Dessiner le joueur
        pygame.draw.circle(fenetre, (255, 0, 0), (joueur_x, joueur_y), 10)
        boite_dialogue.afficher(fenetre)
        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(60)

    # Quitter Pygame
    pygame.quit()
    return False  # Retourne False si la boucle se termine (pour indiquer que l'état doit changer)

# Ne pas exécuter directement ce script si importé
if __name__ == "__main__":
    map_1()
