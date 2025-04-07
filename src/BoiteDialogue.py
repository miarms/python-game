import pygame
import json

class BoiteDialogue:
    def __init__(self, fichier_json, position, taille_min, couleur_fond, couleur_texte, couleur_bordure):  # Ajout de couleur_bordure
        self.position = position
        self.taille_min = taille_min  # Taille minimale de la boîte
        self.taille = taille_min  # Initialiser la taille avec la taille minimale
        self.couleur_fond = couleur_fond
        self.couleur_texte = couleur_texte
        self.couleur_bordure = couleur_bordure  # Attribut pour la couleur de la bordure
        self.font = pygame.font.Font('ressources/fonts/PixelOperator.ttf', 30)
        self.actif = False
        self.input_rect = pygame.Rect(position[0] + 10, position[1] + 50, taille_min[0] - 20, 30)  # Ajuster la position si nécessaire
        self.couleur_active = pygame.Color(255, 222, 89)
        self.couleur_inactive = pygame.Color('gray15')
        self.couleur_actuelle = self.couleur_inactive
        self.survol = False

        # Charger les dialogues depuis le fichier JSON
        with open(fichier_json, "r") as f:
            self.donnees_dialogues = json.load(f)

        # Initialiser l'état du dialogue
        self.map_actuelle = "map"  # Ou la map de départ
        self.dialogue_actuel = "dialogue1"  # Ou le dialogue de départ
        self.texte = self.obtenir_texte_dialogue()

    def obtenir_texte_dialogue(self):
        """Récupère le texte du dialogue actuel."""
        dialogue = self.donnees_dialogues[self.map_actuelle][self.dialogue_actuel]
        return dialogue["texte"]

    def calculer_taille(self, texte_dialogue, choix):
        """Calcule la taille de la boîte en fonction du texte et des choix."""
        largeur_max = self.taille_min[0]  # Largeur minimale
        hauteur = 0  # Hauteur initiale

        # Calculer la hauteur du texte du dialogue
        texte_surface = self.font.render(texte_dialogue, True, self.couleur_texte)
        largeur_max = max(largeur_max, texte_surface.get_width() + 20)  # Mettre à jour la largeur maximale
        hauteur += texte_surface.get_height() + 20  # Ajouter la hauteur du texte

        # Calculer la hauteur des choix
        if choix:
            hauteur += 10  # Espacement avant les choix
            for choix in choix:
                texte_choix = self.font.render(choix["texte"], True, self.couleur_texte)
                largeur_max = max(largeur_max, texte_choix.get_width() + 20)  # Mettre à jour la largeur maximale
                hauteur += texte_choix.get_height() + 5  # Ajouter la hauteur du choix et l'espacement

        return (largeur_max, hauteur)  # Retourner la taille calculée

    def afficher(self, surface):
        """Affiche la boîte de dialogue et les choix sur la surface."""
        if self.actif and self.map_actuelle and self.dialogue_actuel:  # Check for None
            # Calculer la taille de la boîte
            dialogue = self.donnees_dialogues[self.map_actuelle][self.dialogue_actuel]
            self.taille = self.calculer_taille(self.texte, dialogue.get("choix"))

            # Dessiner la bordure rose
            bordure_rect = pygame.Rect(self.position[0] - 5, self.position[1] - 5, self.taille[0] + 10, self.taille[1] + 10)
            pygame.draw.rect(surface, self.couleur_bordure, bordure_rect, border_radius=15)  # Utiliser self.couleur_bordure

            # Dessiner le rectangle avec les coins arrondis
            pygame.draw.rect(surface, self.couleur_fond, (self.position, self.taille), border_radius=10)

            # Afficher le texte du dialogue
            texte_surface = self.font.render(self.texte, True, self.couleur_texte)
            surface.blit(texte_surface, (self.position[0] + 10, self.position[1] + 10))

            # Afficher les choix
            if "choix" in dialogue:
                y = self.position[1] + texte_surface.get_height() + 20  # Position verticale des choix
                for i, choix in enumerate(dialogue["choix"]):
                    texte_choix = self.font.render(f"{i+1}. {choix['texte']}", True, self.couleur_texte)
                    surface.blit(texte_choix, (self.position[0] + 10, y))
                    y += texte_choix.get_height() + 5  # Espacement entre les choix

            # Effet de survol
            if self.survol:
                pygame.draw.rect(surface, (200, 200, 200), (self.position, self.taille), 2, border_radius=10)

    def gerer_evenement(self, event):
        """Gère les événements Pygame, y compris les choix."""
        if event.type == pygame.MOUSEMOTION:
            self.survol = self.input_rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.actif = True
            else:
                self.actif = False
            self.couleur_actuelle = self.couleur_active if self.actif else self.couleur_inactive
        if event.type == pygame.KEYDOWN:
            if self.actif:
                dialogue = self.donnees_dialogues[self.map_actuelle].get(self.dialogue_actuel)  # Utiliser get() pour éviter KeyError
                if dialogue:  # Vérifier si le dialogue existe
                    if "choix" in dialogue:  # Vérifier si le dialogue a des choix
                        if event.key in (pygame.K_1, pygame.K_2):  # Gérer les choix avec les touches 1 et 2
                            choix_index = int(event.key) - 49  # Convertir la touche en index (0 ou 1)
                            if 0 <= choix_index < len(dialogue["choix"]):
                                self.dialogue_actuel = dialogue["choix"][choix_index]["suivant"]
                                if self.dialogue_actuel:  # Vérifier si le dialogue suivant existe
                                    self.texte = self.obtenir_texte_dialogue()
                                else:
                                    self.actif = False
                    else:  # Si pas de choix, passer au suivant avec Entrée
                        if event.key == pygame.K_RETURN:
                            if "suivant" in dialogue and dialogue["suivant"]:
                                self.dialogue_actuel = dialogue["suivant"]
                                if self.dialogue_actuel:  # Vérifier si le dialogue suivant existe
                                    self.texte = self.obtenir_texte_dialogue()
                                else:
                                    self.actif = False
                            else:
                                self.actif = False

if __name__ == "__main__":
    BoiteDialogue()