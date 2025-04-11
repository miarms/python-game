import pygame
import json 

class perso(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, vitesse):
        super().__init__()
        self.full_image = pygame.image.load(image_path).convert_alpha()
        self.frame_width = 64
        self.frame_height = 64
        self.vitesse = vitesse
        self.stats = {
            "vie": 80,
            "sante": 100,
            "defense": 0,
            "combat": 50,
            "magie": 20,
            "vitesse": vitesse,
            "charisme": 50,
            "chance": 25,
            "piece": 0
        }
        self.inventaire = {}
        self.charger_objets("data/items.json")
        self.animation = "walk_face"
        self.frame_index = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, self.frame_width, self.frame_height)
        self.rect.x = x
        self.rect.y = y
        self.animations = {}
        self.load_animation()
        self.image = self.animations[self.animation][self.frame_index]
        self.equipement = {
        "arme": None,
        "armure": None,
        "bottes": None
        }
    def load_animation(self):
        self.animations = {
            # 🧍 Idle / Attente
            "idle_face": self.get_frame(11, 1, 1),   # Row 9
            "idle_left": self.get_frame(10, 11, 11),  # Row 10
            "idle_right": self.get_frame(12, 11, 11), # Row 11
            "idle_back": self.get_frame(9, 11, 11),  # Row 12

            # 🚶 Marche
            "walk_face": self.get_frame(11, 11, 11),   # Row 11
            "walk_left": self.get_frame(10, 11, 11),   # Row 6
            "walk_right": self.get_frame(12, 11, 11),  # Row 7
            "walk_back": self.get_frame(9, 11, 11),   # Row 8

            # 🗡️ Attaque
            #"attack_face": self.get_frame(1, 6, 6), # Row 1
            #"attack_back": self.get_frame(2, 6, 6), # Row 2
            #"attack_left": self.get_frame(3, 6, 6), # Row 3
            #"attack_right": self.get_frame(4, 6, 6),# Row 4

            # ✨ Magie
            #"magic_face": self.get_frame(13, 6, 6), # Row 13
            #"magic_left": self.get_frame(14, 6, 6), # Row 14
            #"magic_right": self.get_frame(15, 6, 6),# Row 15
            #"magic_back": self.get_frame(16, 6, 6), # Row 16

            # 😵 Touché / Mort
            #"hurt_face": self.get_frame(17, 6, 6),  # Row 17
            #"hurt_back": self.get_frame(18, 6, 6),  # Row 18
            #"death": self.get_frame(19, 1, 1),      # Row 19
        }
        
    def get_frame(self, row_start, num_frames, frames_per_row):
        frames = []
        for i in range(num_frames):
            frame_x = (i % frames_per_row) * self.frame_width
            frame_y = (row_start - 1) * self.frame_height
            rect = pygame.Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            # Debug: Print rect to verify coordinates
            print(f"Extracting frame: row={row_start}, index={i}, rect={rect}")
            frames.append(self.full_image.subsurface(rect))
        return frames
    
    def deplacement(self, touches, obstacles):
        dx = 0
        dy = 0
        is_moving = False
        # Touche pour bouger + animation
        if touches[pygame.K_s]:
            dy += self.vitesse
            self.animation = "walk_face"
            is_moving = True
        # Touches fléchées existantes
        if touches[pygame.K_q]:
            dx -= self.vitesse
            self.animation = "walk_left"
            is_moving = True
        if touches[pygame.K_d]:
            dx += self.vitesse
            self.animation = "walk_right"
            is_moving = True
        if touches[pygame.K_z]:
            dy -= self.vitesse
            self.animation = "walk_back"
            is_moving = True

        self.rect.x += dx
        self.rect.y += dy
        # Revenir à l'animation idle si aucun mouvement
        if not is_moving:
            if self.animation == "walk_face":
                self.animation = "idle_face"
            elif self.animation == "walk_left":
                self.animation = "idle_left"
            elif self.animation == "walk_right":
                self.animation = "idle_right"
            elif self.animation == "walk_back":
                self.animation = "idle_back"

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if dx > 0:
                    self.rect.right = obstacle.left
                if dx < 0:
                    self.rect.left = obstacle.right
                if dy > 0:
                    self.rect.bottom = obstacle.top
                if dy < 0:
                    self.rect.top = obstacle.bottom

    def update(self, touches, obstacles):
        self.deplacement(touches, obstacles)
        is_moving = any(touches[key] for key in (pygame.K_z, pygame.K_q, pygame.K_d, pygame.K_s)) # Vérifie si une touche de mouvement est pressée
        if is_moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations[self.animation]):
                self.frame_index = 0
        else:
            self.frame_index = 0  # Réinitialise l'index si pas de mouvement
        self.image = self.animations[self.animation][int(self.frame_index)]

    def get_stats(self):
        return self.stats
    
    
    def charger_objets(self, chemin_fichier):
       with open(chemin_fichier, "r") as f:
           self.tous_les_objets = json.load(f)

    def ajouter_objet(self, id_objet, quantite=1):
       if id_objet in self.tous_les_objets:
           if id_objet in self.inventaire:
               self.inventaire[id_objet] += quantite
           else:
               self.inventaire[id_objet] = quantite
       else:
           print(f"Objet avec l'ID {id_objet} non trouvé !")
   
    def retirer_objet(self, id_objet, quantite=1):
       if id_objet in self.inventaire:
           self.inventaire[id_objet] -= quantite
           if self.inventaire[id_objet] <= 0:
               del self.inventaire[id_objet]
       else:
           print(f"Objet avec l'ID {id_objet} non présent dans l'inventaire !")    
    def utiliser_objet(self, id_objet):
        if id_objet not in self.inventaire or id_objet not in self.tous_les_objets:
            print(f"Objet {id_objet} non disponible !")
            return

        objet = self.tous_les_objets[id_objet]
        type_objet = objet["type"]

        if type_objet == "consommable":
            if "soin" in objet:
                self.stats["vie"] = min(self.stats["vie"] + objet["soin"], 100)  # Limite à 100
                print(f"Vie restaurée : {self.stats['vie']}")
            self.retirer_objet(id_objet, 1)  # Consomme l'objet

        elif type_objet == "arme":
            self.stats["combat"] += objet.get("combat", 0)
            print(f"Équipé : {objet['nom']}, Combat: {self.stats['combat']}")
            # Logique pour équiper (ex. : stocker l'arme équipée)

        elif type_objet == "armure":
            self.stats["defense"] = self.stats.get("defense", 0) + objet.get("defense", 0)
            if "vitesse" in objet:
                self.stats["vitesse"] += objet["vitesse"]
            print(f"Équipé : {objet['nom']}, Défense: {self.stats.get('defense', 0)}, Vitesse: {self.stats['vitesse']}")
            # Logique pour équiper (ex. : stocker l'armure équipée)
    def equiper_objet(self, id_objet):
        objet = self.tous_les_objets[id_objet]
        type_objet = objet["type"]
        sous_type = objet.get("sous-type", type_objet)

        if type_objet == "arme":
            # Unequip previous weapon if any
            if self.equipement["arme"]:
                self.desequiper_objet(self.equipement["arme"])
            self.equipement["arme"] = id_objet
            self.stats["combat"] += objet.get("combat", 0)
            print(f"Équipé arme : {objet['nom']}, Combat: {self.stats['combat']}")

        elif type_objet == "armure":
            if sous_type in ["armure", "bottes"]:
                # Unequip previous item in the same slot
                if self.equipement[sous_type]:
                    self.desequiper_objet(self.equipement[sous_type])
                self.equipement[sous_type] = id_objet
                self.stats["defense"] += objet.get("defense", 0)
                if "vitesse" in objet:
                    self.stats["vitesse"] += objet.get("vitesse", 0)
                print(f"Équipé {sous_type} : {objet['nom']}, Défense: {self.stats['defense']}, Vitesse: {self.stats['vitesse']}")
            else:
                print(f"Erreur : Sous-type d'armure inconnu : {sous_type}")
                return False
        return True

    def desequiper_objet(self, id_objet):
        for slot, equipped_id in list(self.equipement.items()):
            if equipped_id == id_objet:
                objet = self.tous_les_objets[id_objet]
                type_objet = objet["type"]
                if type_objet == "arme":
                    self.stats["combat"] -= objet.get("combat", 0)
                    print(f"Déséquipé arme : {objet['nom']}, Combat: {self.stats['combat']}")
                elif type_objet == "armure":
                    self.stats["defense"] -= objet.get("defense", 0)
                    if "vitesse" in objet:
                        self.stats["vitesse"] -= objet.get("vitesse", 0)
                    print(f"Déséquipé {slot} : {objet['nom']}, Défense: {self.stats['defense']}, Vitesse: {self.stats['vitesse']}")
                self.equipement[slot] = None
                return True
        return False

    def utiliser_objet(self, id_objet):
        if id_objet not in self.inventaire or id_objet not in self.tous_les_objets:
            print(f"Objet {id_objet} non disponible !")
            return None
    
        objet = self.tous_les_objets[id_objet]
        type_objet = objet["type"]
        message = None
    
        if type_objet == "consommable":
            if "vie" in objet:
                if self.stats["vie"] >= 100:
                    message = "Vos points de vie sont déjà pleins"
                else:
                    self.stats["vie"] = min(self.stats["vie"] + objet["vie"], 100)
                    self.retirer_objet(id_objet, 1)
                    message = f"Vie restaurée : {self.stats['vie']}"
                    print(message)
            if "sante" in objet:
                if self.stats["sante"] >= 100:
                    message = "Vos points de santé sont déjà pleins"
                else:
                    self.stats["sante"] = min(self.stats["sante"] + objet["sante"], 100)
                    self.retirer_objet(id_objet, 1)
                    message = f"Santé restaurée : {self.stats['sante']}"
                    print(message)
        else:
            message = f"Objet {objet['nom']} ne peut pas être utilisé directement"
    
        return message