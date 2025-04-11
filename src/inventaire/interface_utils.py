import pygame

def draw_tooltip(surface, objet, tous_les_objets, font_texte, couleur_texte, couleur_fond, couleur_bordure, mouse_pos, screen_width, screen_height):
    """
    Dessine un encart avec la description et les stats de l'objet près de la position de la souris.
    """
    if not objet or objet not in tous_les_objets:
        return
    
    # Récupérer les informations de l'objet
    info = tous_les_objets[objet]
    nom = info["nom"]
    description = info["description"]
    type_objet = info["type"]
    
    # Créer la liste des lignes à afficher
    lignes = [nom, description]
    
    # Ajouter les stats selon le type d'objet
    if type_objet == "arme":
        lignes.append(f"Attaque: {info.get('attaque', 0)}")
    elif type_objet == "consommable":
        lignes.append(f"Soin: {info.get('soin', 0)}")
    elif type_objet == "armure":
        lignes.append(f"Défense: {info.get('defense', 0)}")
    lignes.append(f"Valeur: {info.get('valeur', 0)}")
    
    # Calculer la taille du tooltip
    max_width = 0
    texte_surfaces = []
    for ligne in lignes:
        texte_surface = font_texte.render(ligne, True, couleur_texte)
        texte_surfaces.append(texte_surface)
        max_width = max(max_width, texte_surface.get_width())
    
    padding = 10
    tooltip_width = max_width + 2 * padding
    tooltip_height = len(lignes) * (font_texte.get_height() + 5) + 2 * padding
    
    # Positionner le tooltip près de la souris
    tooltip_x = mouse_pos[0] + 15
    tooltip_y = mouse_pos[1] - tooltip_height // 2
    
    # Ajuster pour ne pas sortir de l'écran
    if tooltip_x + tooltip_width > screen_width:
        tooltip_x = mouse_pos[0] - tooltip_width - 15
    if tooltip_y + tooltip_height > screen_height:
        tooltip_y = screen_height - tooltip_height - 10
    if tooltip_y < 0:
        tooltip_y = 10
    
    # Dessiner le fond et la bordure
    tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
    pygame.draw.rect(surface, couleur_fond, tooltip_rect, border_radius=5)
    pygame.draw.rect(surface, couleur_bordure, tooltip_rect, 2, border_radius=5)
    
    # Afficher chaque ligne
    for i, texte_surface in enumerate(texte_surfaces):
        texte_rect = texte_surface.get_rect(topleft=(tooltip_x + padding, tooltip_y + padding + i * (font_texte.get_height() + 5)))
        surface.blit(texte_surface, texte_rect)

def draw_slot(surface, slot_rect, mouse_pos, slot_color, slot_hover_color, hover_effect_color):
    is_hovered = slot_rect.collidepoint(mouse_pos)
    current_color = slot_hover_color if is_hovered else slot_color
    pygame.draw.rect(surface, current_color, slot_rect, border_radius=5)
    if is_hovered:
        pygame.draw.rect(surface, hover_effect_color, slot_rect, border_radius=5)

menu_contextuel_actif = None  # Variable globale pour gérer l'état du menu contextuel

def draw_inventory_interface(fenetre_inventaire, inventaire_joueur, tous_les_objets, images_objets, font_titre, font_texte, couleur_bouton, gris_fonce, fond_section, slot_base_color, slot_hover_color, fond_transparent, mouse_pos, clothing_rect, misc_rect, stats_rect, slot_size, slot_margin):
    """
    Dessine l'interface complète de l'inventaire avec tooltip au survol et menu contextuel persistant.
    """
    global menu_contextuel_actif  # Utiliser la variable globale pour gérer le menu contextuel

    fenetre_inventaire.fill(gris_fonce)
    
    for rect in [clothing_rect, misc_rect, stats_rect]:
        pygame.draw.rect(fenetre_inventaire, fond_section, rect, border_radius=5)

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

    # Variable pour stocker l'objet survolé
    objet_survole = None

    # Slots pour les objets divers
    for i in range(10):
        x = misc_rect.x + slot_margin + i * (slot_size + slot_margin)
        y = misc_rect.y + slot_margin
        slot_rect = pygame.Rect(x, y, slot_size, slot_size)
        draw_slot(fenetre_inventaire, slot_rect, mouse_pos, slot_base_color, slot_hover_color, fond_transparent)
        index_objet = list(inventaire_joueur.keys())
        if i < len(index_objet):
            id_objet = index_objet[i]
            if id_objet in images_objets and images_objets[id_objet]:
                image_objet = images_objets[id_objet]
                image_rect = image_objet.get_rect(center=slot_rect.center)
                fenetre_inventaire.blit(image_objet, image_rect)
                # Afficher la quantité pour les consommables
                if tous_les_objets[id_objet]["type"] == "consommable" and inventaire_joueur[id_objet] > 1:
                    quantite_texte = font_texte.render(str(inventaire_joueur[id_objet]), True, couleur_bouton)
                    quantite_rect = quantite_texte.get_rect(bottomright=slot_rect.bottomright)
                    fenetre_inventaire.blit(quantite_texte, quantite_rect)
                # Vérifier si le slot est survolé
                if slot_rect.collidepoint(mouse_pos):
                    objet_survole = id_objet
                # Activer le menu contextuel au clic
                if pygame.mouse.get_pressed()[0] and slot_rect.collidepoint(mouse_pos):
                    menu_contextuel_actif = (mouse_pos, id_objet)

    # Afficher le menu contextuel si actif
    if menu_contextuel_actif:
        menu_pos, id_objet = menu_contextuel_actif
        menu_width, menu_height = 150, 80
        menu_rect = pygame.Rect(menu_pos[0], menu_pos[1], menu_width, menu_height)
        pygame.draw.rect(fenetre_inventaire, (50, 50, 50), menu_rect, border_radius=5)
        pygame.draw.rect(fenetre_inventaire, (255, 255, 255), menu_rect, 2, border_radius=5)

        # Ajouter les options "Utiliser" et "Jeter"
        utiliser_rect = pygame.Rect(menu_pos[0] + 10, menu_pos[1] + 10, menu_width - 20, 30)
        jeter_rect = pygame.Rect(menu_pos[0] + 10, menu_pos[1] + 40, menu_width - 20, 30)

        pygame.draw.rect(fenetre_inventaire, (100, 100, 100), utiliser_rect, border_radius=5)
        pygame.draw.rect(fenetre_inventaire, (100, 100, 100), jeter_rect, border_radius=5)

        utiliser_texte = font_texte.render("Utiliser", True, (255, 255, 255))
        jeter_texte = font_texte.render("Jeter", True, (255, 255, 255))

        fenetre_inventaire.blit(utiliser_texte, utiliser_texte.get_rect(center=utiliser_rect.center))
        fenetre_inventaire.blit(jeter_texte, jeter_texte.get_rect(center=jeter_rect.center))

        # Gérer les clics sur les options
        if pygame.mouse.get_pressed()[0]:
            if utiliser_rect.collidepoint(mouse_pos):
                print(f"Utiliser l'objet : {tous_les_objets[id_objet]['nom']}")
                menu_contextuel_actif = None  # Fermer le menu contextuel après action
            elif jeter_rect.collidepoint(mouse_pos):
                print(f"Jeter l'objet : {tous_les_objets[id_objet]['nom']}")
                if inventaire_joueur[id_objet] > 1:
                    inventaire_joueur[id_objet] -= 1
                else :
                    inventaire_joueur.pop(id_objet, None)
                menu_contextuel_actif = None  # Fermer le menu contextuel après action

    # Fermer le menu contextuel si clic en dehors
    if menu_contextuel_actif and not menu_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        menu_contextuel_actif = None

    # Afficher le tooltip si un objet est survolé
    if objet_survole:
        draw_tooltip(
            fenetre_inventaire, 
            objet_survole, 
            tous_les_objets, 
            font_texte, 
            couleur_bouton, 
            (50, 60, 70, 200),  # Fond semi-transparent
            (255, 222, 89),      # Bordure
            mouse_pos, 
            fenetre_inventaire.get_width(), 
            fenetre_inventaire.get_height()
        )