import pygame
from .interface_utils import draw_inventory_interface
def draw_input_box(surface, input_text, input_rect, font, active, couleur_texte, couleur_fond, couleur_bordure):
    """
    Dessine une boîte de saisie avec le texte actuel.
    """
    pygame.draw.rect(surface, couleur_fond, input_rect, border_radius=5)
    pygame.draw.rect(surface, couleur_bordure, input_rect, 2 if active else 1, border_radius=5)
    texte_surface = font.render(input_text, True, couleur_texte)
    texte_rect = texte_surface.get_rect(center=input_rect.center)
    surface.blit(texte_surface, texte_rect)

def cheats_code(fenetre_inventaire, inventaire_joueur, tous_les_objets, font_texte, couleur_texte, images_objets, font_titre, couleur_bouton, gris_fonce, fond_section, slot_base_color, slot_hover_color, fond_transparent, misc_rect, stats_rect, slot_size, slot_margin, personnage=None):
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
            misc_rect, stats_rect, slot_size, slot_margin, personnage
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