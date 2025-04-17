import pygame
from .inventaire import inventaire
from .cheat_code import cheats_code

class InterfaceManager:
    def __init__(self, fenetre, joueur, font_texte, couleur_texte):
        self.fenetre = fenetre
        self.joueur = joueur
        self.font_texte = font_texte
        self.couleur_texte = couleur_texte
        self.font_titre = pygame.font.Font(None, 40)
        self.couleur_bouton = (255, 222, 89)
        self.gris_fonce = (64, 78, 92)
        self.fond_section = (40, 48, 56)
        self.slot_base_color = (50, 60, 70)
        self.slot_hover_color = (70, 85, 100)
        self.fond_transparent = (255, 255, 255, 128)
        self.slot_size = 64
        self.slot_margin = 8
        self.largeur_inventaire = 1540
        self.hauteur_inventaire = 800
        
        # Rectangles pour l'inventaire
        self.misc_width = 10 * (self.slot_size + self.slot_margin) + self.slot_margin
        self.misc_height = 3 * (self.slot_size + self.slot_margin) + self.slot_margin
        self.misc_rect = pygame.Rect(
            50,
            self.hauteur_inventaire - self.misc_height - 50,
            self.misc_width,
            self.misc_height
        )
        self.stats_width = 300
        self.stats_height = 200
        self.stats_rect = pygame.Rect(
            self.largeur_inventaire - self.stats_width - 50,
            self.hauteur_inventaire - self.stats_height - 50,
            self.stats_width,
            self.stats_height
        )
        
        # État de l'interface
        self.afficher_inventaire = False
        self.afficher_cheat_code = False
        self.cheat_input_text = ""
        self.cheat_message = None
        self.cheat_message_timer = 0
        self.mouse_pos = (0, 0)
        
    def gerer_evenements(self, event):
        """Gère les événements clavier et souris pour l'inventaire et les cheats."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print("Touche I pressée, afficher_inventaire =", not self.afficher_inventaire)
                self.afficher_inventaire = not self.afficher_inventaire
                if self.afficher_inventaire:
                    self.afficher_cheat_code = False
                    self.cheat_input_text = ""
                    self.cheat_message = None
            if event.key == pygame.K_ESCAPE:
                print("Touche Échap pressée, afficher_inventaire =", self.afficher_inventaire, "afficher_cheat_code =", self.afficher_cheat_code)
                if self.afficher_cheat_code:
                    self.afficher_cheat_code = False
                    self.cheat_input_text = ""
                    self.cheat_message = None
                    print("Mode cheat code fermé")
                elif self.afficher_inventaire:
                    self.afficher_inventaire = False
                    print("Inventaire fermé")
            if event.key == pygame.K_h and self.afficher_inventaire and not self.afficher_cheat_code:
                print("Touche H pressée, activation mode cheat code")
                self.afficher_cheat_code = True
                self.cheat_input_text = ""
                self.cheat_message = None
            if self.afficher_cheat_code and event.key == pygame.K_RETURN:
                self.cheat_input_text = self.cheat_input_text.strip()
                print(f"ID saisi : {self.cheat_input_text}")
                objet_key = None
                for key, objet in self.joueur.tous_les_objets.items():
                    if objet["id"] == self.cheat_input_text:
                        objet_key = key
                        break
                if objet_key:
                    quantite = 1
                    if objet_key in self.joueur.inventaire:
                        self.joueur.inventaire[objet_key] += quantite
                    else:
                        self.joueur.inventaire[objet_key] = quantite
                    self.cheat_message = f"Objet ajouté : {self.joueur.tous_les_objets[objet_key]['nom']} !"
                    print(f"Objet ajouté : {objet_key} ({self.joueur.tous_les_objets[objet_key]['nom']})")
                    self.cheat_message_timer = pygame.time.get_ticks() + 1000
                    self.cheat_input_text = ""
                else:
                    self.cheat_message = f"ID invalide : {self.cheat_input_text}. Essayez : 1, 2, 3"
                    print(f"Erreur : ID invalide : {self.cheat_input_text}")
                    self.cheat_message_timer = pygame.time.get_ticks() + 1000
                    self.cheat_input_text = ""
            if self.afficher_cheat_code and event.key == pygame.K_BACKSPACE:
                self.cheat_input_text = self.cheat_input_text[:-1]
            if self.afficher_cheat_code and event.unicode.isprintable() and len(self.cheat_input_text) < 20:
                self.cheat_input_text += event.unicode
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and self.afficher_inventaire:
            close_button_rect = pygame.Rect(self.largeur_inventaire - 50, 10, 40, 40)
            if close_button_rect.collidepoint(event.pos):
                self.afficher_inventaire = False
                self.afficher_cheat_code = False
                self.cheat_input_text = ""
                self.cheat_message = None
                print("Inventaire fermé via bouton")

    def dessiner(self):
        """Dessine l'inventaire ou la barre de cheat code si nécessaire."""
        if self.afficher_inventaire:
            inventaire(
                self.fenetre, self.joueur.inventaire, self.joueur.tous_les_objets,
                self.font_texte, self.couleur_texte, self.joueur, self.mouse_pos
            )
            if self.afficher_cheat_code:
                self.cheat_input_text, self.cheat_message, self.cheat_message_timer, _ = cheats_code(
                    self.fenetre, self.joueur.inventaire, self.joueur.tous_les_objets,
                    self.font_texte, self.couleur_texte, inventaire.images_objets,
                    self.font_titre, self.couleur_bouton, self.gris_fonce, self.fond_section,
                    self.slot_base_color, self.slot_hover_color, self.fond_transparent,
                    self.misc_rect, self.stats_rect, self.slot_size, self.slot_margin,
                    self.cheat_input_text, self.mouse_pos, self.joueur,
                    self.cheat_message, self.cheat_message_timer
                )

    def est_interface_active(self):
        """Retourne True si l'inventaire ou les cheats sont affichés."""
        return self.afficher_inventaire or self.afficher_cheat_code