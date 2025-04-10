import pygame

def inventaire(fenetre_inventaire, inventaire_joueur, tous_les_objets, font_texte, couleur_texte):
    pygame.init()
    
    # Paramètres de la fenêtre
    largeur_inventaire = 1540
    hauteur_inventaire = 800
    #fenetre_inventaire = pygame.display.set_mode((largeur_inventaire, hauteur_inventaire)) # La fenêtre est créée en dehors, on la reçoit en paramètre
    pygame.display.set_caption("Inventaire")

    # Couleurs personnalisées (sombre et classe)
    gris_fonce = (64, 78, 92)  # Fond principal
    couleur_bouton = (255, 222, 89)  # Titres et accents
    fond_transparent = (255, 255, 255, 128)  # Effet de survol
    fond_section = (40, 48, 56)  # Fond des sections
    slot_base_color = (50, 60, 70)  # Slots au repos
    slot_hover_color = (70, 85, 100)  # Slots au survol

    # Polices
    font_titre = pygame.font.Font(None, 40)
    font_texte = pygame.font.Font(None, 24)

    # Paramètres des slots
    slot_size = 64 # Augmenter la taille des slots pour les images
    slot_margin = 8
    
    # Section vêtements (3x3 en bas à gauche)
    clothing_width = 3 * (slot_size + slot_margin) + slot_margin  # 224
    clothing_height = 3 * (slot_size + slot_margin) + slot_margin  # 224
    clothing_rect = pygame.Rect(
        50,  # Marge gauche
        hauteur_inventaire - clothing_height - 50,  # En bas avec marge
        clothing_width,
        clothing_height
    )
    
    # Section objets divers (1x10 en bas, à droite des vêtements)
    misc_width = 10 * (slot_size + slot_margin) + slot_margin  # 712
    misc_height = slot_size + 2 * slot_margin  # 80
    misc_rect = pygame.Rect(
        clothing_rect.right + 20,  # À droite des vêtements avec une petite marge
        hauteur_inventaire - misc_height - 50,  # Aligné avec vêtements
        misc_width,
        misc_height
    )
    
    # Section statistiques (en bas à droite)
    stats_width = 300
    stats_height = 200  # Réduit pour s'aligner avec la hauteur des sections
    stats_rect = pygame.Rect(
        largeur_inventaire - stats_width - 50,  # Marge droite
        hauteur_inventaire - stats_height - 50,  # Aligné avec vêtements et objets
        stats_width,
        stats_height
    )
    
    running = True
    mouse_pos = (0, 0)
    
    # Charger les images des objets
    images_objets = {}
    for id_objet, objet in tous_les_objets.items():
        try:
            image_path = objet["image"]
            image = pygame.image.load(image_path).convert_alpha()
            # Redimensionner l'image si nécessaire (à la taille du slot)
            image = pygame.transform.scale(image, (slot_size, slot_size))
            images_objets[id_objet] = image
        except FileNotFoundError:
            print(f"Image non trouvée pour l'objet : {objet['nom']}")
            images_objets[id_objet] = None  # Ou une image par défaut, ou laisser None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

        # Fond principal sombre
        fenetre_inventaire.fill(gris_fonce)
        
        # Dessin des fonds des sections (sans ombre)
        for rect in [clothing_rect, misc_rect, stats_rect]:
            pygame.draw.rect(fenetre_inventaire, fond_section, rect, border_radius=5)

        # Titres (au-dessus des sections)
        titres = [
            ("Vêtements", clothing_rect.top - 40),
            ("Objets", misc_rect.top - 40),
            ("Statistiques", stats_rect.top - 40)
        ]
        for texte, y_pos in titres:
            titre = font_titre.render(texte, True, couleur_bouton)
            titre_rect = titre.get_rect(center=(
                clothing_rect.centerx if texte == "Vêtements" else 
                misc_rect.centerx if texte == "Objets" else 
                stats_rect.centerx, 
                y_pos
            ))
            fenetre_inventaire.blit(titre, titre_rect)

        # Slots vêtements (3x3)
        for i in range(9):
            x = clothing_rect.x + slot_margin + (i % 3) * (slot_size + slot_margin)
            y = clothing_rect.y + slot_margin + (i // 3) * (slot_size + slot_margin)
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)
            draw_slot(fenetre_inventaire, slot_rect, mouse_pos, slot_base_color, slot_hover_color, fond_transparent)
            # Afficher l'image de l'objet s'il y en a un dans ce slot
            # (Ici, il faudrait une logique pour savoir quel objet est équipé dans quel slot)
            # Pour l'instant, on n'affiche rien

        # Slots objets divers (1x10)
        for i in range(10):
            x = misc_rect.x + slot_margin + i * (slot_size + slot_margin)
            y = misc_rect.y + slot_margin
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)
            draw_slot(fenetre_inventaire, slot_rect, mouse_pos, slot_base_color, slot_hover_color, fond_transparent)
            # Afficher l'image de l'objet s'il y en a un dans ce slot
            # (Parcourir l'inventaire et vérifier si l'objet correspond à ce slot)
            index_objet = list(inventaire_joueur.keys())  # Convertir les clés en liste
            if i < len(index_objet):
                id_objet = index_objet[i]
                if id_objet in images_objets and images_objets[id_objet]:
                    image_objet = images_objets[id_objet]
                    image_rect = image_objet.get_rect(center=slot_rect.center)
                    fenetre_inventaire.blit(image_objet, image_rect)

        # Statistiques
        stats = [
            "Force: 15",
            "Agilité: 12",
            "Endurance: 18",
            "Intelligence: 10",
            "Chance: 7"
        ]
        for i, stat in enumerate(stats):
            texte = font_texte.render(stat, True, couleur_bouton)
            texte_rect = texte.get_rect(topleft=(stats_rect.x + 20, stats_rect.y + 20 + i * 30))  # Espacement réduit
            fenetre_inventaire.blit(texte, texte_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()

def draw_slot(surface, slot_rect, mouse_pos, slot_color, slot_hover_color, hover_effect_color):
    is_hovered = slot_rect.collidepoint(mouse_pos)
    current_color = slot_hover_color if is_hovered else slot_color
    pygame.draw.rect(surface, current_color, slot_rect, border_radius=5)
    if is_hovered:
        pygame.draw.rect(surface, hover_effect_color, slot_rect, border_radius=5)

if __name__ == "__main__":
    inventaire()