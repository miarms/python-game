import pygame

class perso(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, vitesse):
        super().__init__()
        self.full_image = pygame.image.load(image_path).convert_alpha()
        self.frame_width = 64
        self.frame_height = 64
        self.vitesse = vitesse
        self.stats = {
            "vie": 100,
            "energie": 100,
            "combat": 50,
            "magie": 20,
            "vitesse": vitesse,
            "charisme": 50,
            "chance": 25
        }

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

    def load_animation(self):
        self.animations = {
            # 🧍 Idle / Attente
            #"idle_face": self.get_frame(9, 9, 9),   # Row 9
            #"idle_left": self.get_frame(10, 9, 9),  # Row 10
            #"idle_right": self.get_frame(11, 9, 9), # Row 11
            #"idle_back": self.get_frame(12, 9, 9),  # Row 12

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
        # Touche Z pour avancer vers le haut avec "walk_face"
        if touches[pygame.K_z]:
            dy -= self.vitesse
            self.animation = "walk_face"
            is_moving = True
        # Touches fléchées existantes
        if touches[pygame.K_LEFT]:
            dx -= self.vitesse
            self.animation = "walk_left"
            is_moving = True
        if touches[pygame.K_RIGHT]:
            dx += self.vitesse
            self.animation = "walk_right"
            is_moving = True
        if touches[pygame.K_UP]:
            dy -= self.vitesse
            self.animation = "walk_back"
            is_moving = True
        if touches[pygame.K_DOWN]:
            dy += self.vitesse
            self.animation = "walk_face"
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
    
    def get_stats(self):
        return self.stats