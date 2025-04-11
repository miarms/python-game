import pygame

def draw_tooltip(surface, objet, tous_les_objets, font_texte, couleur_texte, couleur_fond, couleur_bordure, mouse_pos, screen_width, screen_height):
    if not objet or objet not in tous_les_objets:
        return
    
    info = tous_les_objets[objet]
    nom = info["nom"]
    description = info["description"]
    type_objet = info["type"]
    
    lignes = [nom, description]
    
    if type_objet == "arme":
        lignes.append(f"Combat: {info.get('combat', 0)}")
    elif type_objet == "consommable":
        if "vie" in info:
            lignes.append(f"Vie: {info['vie']}")
        if "sante" in info:
            lignes.append(f"Santé: {info['sante']}")
    elif type_objet == "armure":
        lignes.append(f"Défense: {info.get('defense', 0)}")
    lignes.append(f"Valeur: {info.get('valeur', 0)}")
    
    max_width = 0
    texte_surfaces = []
    for ligne in lignes:
        texte_surface = font_texte.render(ligne, True, couleur_texte)
        texte_surfaces.append(texte_surface)
        max_width = max(max_width, texte_surface.get_width())
    
    padding = 10
    tooltip_width = max_width + 2 * padding
    tooltip_height = len(lignes) * (font_texte.get_height() + 5) + 2 * padding
    
    tooltip_x = mouse_pos[0] + 15
    tooltip_y = mouse_pos[1] - tooltip_height // 2
    
    if tooltip_x + tooltip_width > screen_width:
        tooltip_x = mouse_pos[0] - tooltip_width - 15
    if tooltip_y + tooltip_height > screen_height:
        tooltip_y = screen_height - tooltip_height - 10
    if tooltip_y < 0:
        tooltip_y = 10
    
    tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
    pygame.draw.rect(surface, couleur_fond, tooltip_rect, border_radius=5)
    pygame.draw.rect(surface, couleur_bordure, tooltip_rect, 2, border_radius=5)
    
    for i, texte_surface in enumerate(texte_surfaces):
        texte_rect = texte_surface.get_rect(topleft=(tooltip_x + padding, tooltip_y + padding + i * (font_texte.get_height() + 5)))
        surface.blit(texte_surface, texte_rect)

def draw_slot(surface, slot_rect, mouse_pos, slot_color, slot_hover_color, hover_effect_color):
    is_hovered = slot_rect.collidepoint(mouse_pos)
    current_color = slot_hover_color if is_hovered else slot_color
    pygame.draw.rect(surface, current_color, slot_rect, border_radius=5)
    if is_hovered:
        pygame.draw.rect(surface, hover_effect_color, slot_rect, border_radius=5)

menu_contextuel_actif = None
message_actif = None
message_timer = 0

def draw_inventory_interface(fenetre_inventaire, inventaire_joueur, tous_les_objets, images_objets, font_titre, font_texte, couleur_bouton, gris_fonce, fond_section, slot_base_color, slot_hover_color, fond_transparent, mouse_pos, clothing_rect, misc_rect, stats_rect, slot_size, slot_margin, personnage=None):
    global menu_contextuel_actif, message_actif, message_timer
    
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
    
    if personnage:
        stats = personnage.get_stats()
        y_offset = stats_rect.top + 10
        for stat, valeur in stats.items():
            texte_stat = font_texte.render(f"{stat.capitalize()}: {valeur}", True, couleur_bouton)
            texte_rect = texte_stat.get_rect(topleft=(stats_rect.left + 10, y_offset))
            fenetre_inventaire.blit(texte_stat, texte_rect)
            y_offset += font_texte.get_height() + 5
    
    objet_survole = None
    last_click_time = 0
    click_delay = 200
    
    sous_types_slots = {
        "plastron": pygame.Rect(clothing_rect.x + slot_margin, clothing_rect.y + slot_margin, slot_size, slot_size),
        "bottes": pygame.Rect(clothing_rect.x + slot_margin, clothing_rect.y + slot_margin + slot_size + slot_margin, slot_size, slot_size)
    }
    for sous_type, slot_rect in sous_types_slots.items():
        draw_slot(fenetre_inventaire, slot_rect, mouse_pos, slot_base_color, slot_hover_color, fond_transparent)
        if personnage and personnage.equipement.get(sous_type):
            id_objet = personnage.equipement[sous_type]
            if id_objet in images_objets and images_objets[id_objet]:
                image_objet = images_objets[id_objet]
                image_rect = image_objet.get_rect(center=slot_rect.center)
                fenetre_inventaire.blit(image_objet, image_rect)
            if slot_rect.collidepoint(mouse_pos):
                objet_survole = id_objet
    
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
                if tous_les_objets[id_objet]["type"] == "consommable" and inventaire_joueur[id_objet] > 1:
                    quantite_texte = font_texte.render(str(inventaire_joueur[id_objet]), True, couleur_bouton)
                    quantite_rect = quantite_texte.get_rect(bottomright=slot_rect.bottomright)
                    fenetre_inventaire.blit(quantite_texte, quantite_rect)
                if slot_rect.collidepoint(mouse_pos):
                    objet_survole = id_objet
                current_time = pygame.time.get_ticks()
                if pygame.mouse.get_pressed()[0] and slot_rect.collidepoint(mouse_pos) and current_time - last_click_time > click_delay:
                    last_click_time = current_time
                    menu_contextuel_actif = (mouse_pos, id_objet)
    
    if menu_contextuel_actif:
        menu_pos, id_objet = menu_contextuel_actif
        menu_width, menu_height = 150, 80
        menu_rect = pygame.Rect(menu_pos[0], menu_pos[1], menu_width, menu_height)
        pygame.draw.rect(fenetre_inventaire, (50, 50, 50), menu_rect, border_radius=5)
        pygame.draw.rect(fenetre_inventaire, (255, 255, 255), menu_rect, 2, border_radius=5)
        
        utiliser_rect = pygame.Rect(menu_pos[0] + 10, menu_pos[1] + 10, menu_width - 20, 30)
        jeter_rect = pygame.Rect(menu_pos[0] + 10, menu_pos[1] + 40, menu_width - 20, 30)
        
        pygame.draw.rect(fenetre_inventaire, (100, 100, 100), utiliser_rect, border_radius=5)
        pygame.draw.rect(fenetre_inventaire, (100, 100, 100), jeter_rect, border_radius=5)
        
        utiliser_texte = font_texte.render("Utiliser", True, (255, 255, 255))
        jeter_texte = font_texte.render("Jeter", True, (255, 255, 255))
        
        fenetre_inventaire.blit(utiliser_texte, utiliser_texte.get_rect(center=utiliser_rect.center))
        fenetre_inventaire.blit(jeter_texte, jeter_texte.get_rect(center=jeter_rect.center))
        
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and current_time - last_click_time > click_delay:
            last_click_time = current_time
            if utiliser_rect.collidepoint(mouse_pos):
                print(f"Utiliser l'objet : {tous_les_objets[id_objet]['nom']}")
                if personnage:
                    message = personnage.utiliser_objet(id_objet)
                    if message:
                        message_actif = message
                        message_timer = pygame.time.get_ticks() + 2000
                menu_contextuel_actif = None
            elif jeter_rect.collidepoint(mouse_pos):
                print(f"Jeter l'objet : {tous_les_objets[id_objet]['nom']}")
                if id_objet in inventaire_joueur:
                    if inventaire_joueur[id_objet] > 1:
                        inventaire_joueur[id_objet] -= 1
                    else:
                        inventaire_joueur.pop(id_objet)
                menu_contextuel_actif = None
    
    if menu_contextuel_actif and not menu_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and current_time - last_click_time > click_delay:
        last_click_time = current_time
        menu_contextuel_actif = None
    
    # Afficher le message temporaire en haut à droite de l'écran
    if message_actif and pygame.time.get_ticks() < message_timer:
        texte_message = font_texte.render(message_actif, True, couleur_bouton)
        message_rect = texte_message.get_rect(topright=(fenetre_inventaire.get_width() - 10, 10))  # Position en haut à droite
        pygame.draw.rect(fenetre_inventaire, (50, 60, 70), message_rect.inflate(10, 10), border_radius=5)  # Fond avec marge
        fenetre_inventaire.blit(texte_message, message_rect)
    
    if objet_survole:
        draw_tooltip(
            fenetre_inventaire, 
            objet_survole, 
            tous_les_objets, 
            font_texte, 
            couleur_bouton, 
            (50, 60, 70, 200),
            (255, 222, 89),
            mouse_pos, 
            fenetre_inventaire.get_width(), 
            fenetre_inventaire.get_height()
        )