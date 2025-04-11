import pygame
import random

def draw_input_box(surface, input_text, input_rect, font, active, couleur_texte, couleur_fond, couleur_bordure):
    """
    Dessine une boîte de saisie avec le texte actuel.
    """
    pygame.draw.rect(surface, couleur_fond, input_rect, border_radius=5)
    pygame.draw.rect(surface, couleur_bordure, input_rect, 2 if active else 1, border_radius=5)
    texte_surface = font.render(input_text, True, couleur_texte)
    texte_rect = texte_surface.get_rect(center=input_rect.center)
    surface.blit(texte_surface, texte_rect)

def draw_inventory_interface(fenetre_inventaire, inventaire_joueur, tous_les_objets, images_objets, font_titre, font_texte, couleur_bouton, gris_fonce, fond_section, slot_base_color, slot_hover_color, fond_transparent, mouse_pos, clothing_rect, misc_rect, stats_rect, slot_size, slot_margin):
    """
    Dessine l'interface complète de l'inventaire.
    """
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

    for i in range(9):
        x = clothing_rect.x + slot_margin + (i % 3) * (slot_size + slot_margin)
        y = clothing_rect.y + slot_margin + (i // 3) * (slot_size + slot_margin)
        slot_rect = pygame.Rect(x, y, slot_size, slot_size)
        draw_slot(fenetre_inventaire, slot_rect, mouse_pos, slot_base_color, slot_hover_color, fond_transparent)

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

    stats = [
        "Force: 15",
        "Agilité: 12",
        "Endurance: 18",
        "Intelligence: 10",
        "Chance: 7"
    ]
    for i, stat in enumerate(stats):
        texte = font_texte.render(stat, True, couleur_bouton)
        texte_rect = texte.get_rect(topleft=(stats_rect.x + 20, stats_rect.y + 20 + i * 30))
        fenetre_inventaire.blit(texte, texte_rect)

def cheats_code(fenetre_inventaire, inventaire_joueur, tous_les_objets, font_texte, couleur_texte, images_objets, font_titre, couleur_bouton, gris_fonce, fond_section, slot_base_color, slot_hover_color, fond_transparent, clothing_rect, misc_rect, stats_rect, slot_size, slot_margin):
    """
    Affiche une barre de saisie pour entrer l'ID d'un objet (1, 2, 3) et met à jour l'inventaire immédiatement.
    """
    if not tous_les_objets:
        print("Erreur : tous_les_objets est vide. Vérifiez le chargement de data/items.json.")
        return True

    input_active = True
    input_text = ""
    input_rect = pygame.Rect(
        fenetre_inventaire.get_width() // 2 - 150,
        fenetre_inventaire.get_height() // 2 - 20,
        300,
        40
    )
    couleur_fond = (50, 60, 70)
    couleur_bordure = (255, 222, 89)
    mouse_pos = (0, 0)
    message = None
    message_timer = 0
    
    # Liste des IDs valides pour l'affichage
    valid_ids = ["1", "2", "3"]  # Basé sur le nouveau JSON
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_text = input_text.strip()
                    print(f"ID saisi : {input_text}")  # Debug
                    # Chercher l'objet correspondant à l'ID
                    objet_key = None
                    for key, objet in tous_les_objets.items():
                        if objet["id"] == input_text:
                            objet_key = key
                            break
                    if objet_key:
                        quantite = 1
                        if objet_key in inventaire_joueur:
                            inventaire_joueur[objet_key] += quantite
                        else:
                            inventaire_joueur[objet_key] = quantite
                        message = f"Objet ajouté : {tous_les_objets[objet_key]['nom']} !"
                        print(f"Objet ajouté : {objet_key} ({tous_les_objets[objet_key]['nom']})")  # Debug
                        message_timer = pygame.time.get_ticks() + 1000
                        input_text = ""
                    else:
                        message = f"ID invalide : {input_text}. Essayez : {', '.join(valid_ids)}"
                        print(f"Erreur : ID invalide : {input_text}")  # Debug
                        message_timer = pygame.time.get_ticks() + 1000
                        input_text = ""
                elif event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20:
                        input_text += event.unicode
        
        # Redessiner l'interface
        draw_inventory_interface(
            fenetre_inventaire, inventaire_joueur, tous_les_objets, images_objets,
            font_titre, font_texte, couleur_bouton, gris_fonce, fond_section,
            slot_base_color, slot_hover_color, fond_transparent, mouse_pos,
            clothing_rect, misc_rect, stats_rect, slot_size, slot_margin
        )
        
        # Afficher l'instruction
        instruction = f"Entrez l'ID de l'objet (ex: 1, 2, 3)"
        texte_instruction = font_texte.render(instruction, True, couleur_texte)
        texte_rect_instruction = texte_instruction.get_rect(center=(fenetre_inventaire.get_width() // 2, fenetre_inventaire.get_height() // 2 - 100))
        fenetre_inventaire.blit(texte_instruction, texte_rect_instruction)
        
        # Afficher la liste des IDs valides
        valid_ids_text = f"IDs valides : {', '.join(valid_ids)}"
        texte_valid_ids = font_texte.render(valid_ids_text, True, couleur_texte)
        texte_valid_ids_rect = texte_valid_ids.get_rect(center=(fenetre_inventaire.get_width() // 2, fenetre_inventaire.get_height() // 2 - 60))
        fenetre_inventaire.blit(texte_valid_ids, texte_valid_ids_rect)
        
        # Dessiner la boîte de saisie
        draw_input_box(fenetre_inventaire, input_text, input_rect, font_texte, input_active, couleur_texte, couleur_fond, couleur_bordure)
        
        # Afficher le message temporaire
        if message and pygame.time.get_ticks() < message_timer:
            texte = font_texte.render(message, True, couleur_texte)
            texte_rect = texte.get_rect(center=(fenetre_inventaire.get_width() // 2, fenetre_inventaire.get_height() // 2 + 50))
            fenetre_inventaire.blit(texte, texte_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return True

def inventaire(fenetre_inventaire, inventaire_joueur, tous_les_objets, font_texte, couleur_texte):
    pygame.init()
    
    largeur_inventaire = 1540
    hauteur_inventaire = 800
    pygame.display.set_caption("Inventaire")

    gris_fonce = (64, 78, 92)
    couleur_bouton = (255, 222, 89)
    fond_transparent = (255, 255, 255, 128)
    fond_section = (40, 48, 56)
    slot_base_color = (50, 60, 70)
    slot_hover_color = (70, 85, 100)

    font_titre = pygame.font.Font(None, 40)
    font_texte = pygame.font.Font(None, 24)

    slot_size = 64
    slot_margin = 8
    
    clothing_width = 3 * (slot_size + slot_margin) + slot_margin
    clothing_height = 3 * (slot_size + slot_margin) + slot_margin
    clothing_rect = pygame.Rect(
        50,
        hauteur_inventaire - clothing_height - 50,
        clothing_width,
        clothing_height
    )
    
    misc_width = 10 * (slot_size + slot_margin) + slot_margin
    misc_height = slot_size + 2 * slot_margin
    misc_rect = pygame.Rect(
        clothing_rect.right + 20,
        hauteur_inventaire - misc_height - 50,
        misc_width,
        misc_height
    )
    
    stats_width = 300
    stats_height = 200
    stats_rect = pygame.Rect(
        largeur_inventaire - stats_width - 50,
        hauteur_inventaire - stats_height - 50,
        stats_width,
        stats_height
    )
    
    running = True
    mouse_pos = (0, 0)
    
    images_objets = {}
    print("Chargement des images des objets...")
    for id_objet, objet in tous_les_objets.items():
        try:
            image_path = objet["image"]
            print(f"Tentative de chargement de l'image : {image_path}")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (slot_size, slot_size))
            images_objets[id_objet] = image
        except FileNotFoundError:
            print(f"Erreur : Image non trouvée pour l'objet {objet['nom']} ({image_path})")
            images_objets[id_objet] = None
        except pygame.error as e:
            print(f"Erreur Pygame lors du chargement de {image_path} : {e}")
            images_objets[id_objet] = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    print("Touche 'h' pressée, lancement de cheats_code")
                    if not cheats_code(
                        fenetre_inventaire, inventaire_joueur, tous_les_objets, font_texte, couleur_bouton,
                        images_objets, font_titre, couleur_bouton, gris_fonce, fond_section,
                        slot_base_color, slot_hover_color, fond_transparent, clothing_rect,
                        misc_rect, stats_rect, slot_size, slot_margin
                    ):
                        running = False

        draw_inventory_interface(
            fenetre_inventaire, inventaire_joueur, tous_les_objets, images_objets,
            font_titre, font_texte, couleur_bouton, gris_fonce, fond_section,
            slot_base_color, slot_hover_color, fond_transparent, mouse_pos,
            clothing_rect, misc_rect, stats_rect, slot_size, slot_margin
        )
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()

def draw_slot(surface, slot_rect, mouse_pos, slot_color, slot_hover_color, hover_effect_color):
    is_hovered = slot_rect.collidepoint(mouse_pos)
    current_color = slot_hover_color if is_hovered else slot_color
    pygame.draw.rect(surface, current_color, slot_rect, border_radius=5)
    if is_hovered:
        pygame.draw.rect(surface, hover_effect_color, slot_rect, border_radius=5)