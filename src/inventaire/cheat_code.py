import pygame
from .interface_utils import draw_inventory_interface, draw_input_box

def cheats_code(fenetre, inventaire_joueur, tous_les_objets, font_texte, couleur_texte, images_objets, font_titre, couleur_bouton, gris_fonce, fond_section, slot_base_color, slot_hover_color, fond_transparent, misc_rect, stats_rect, slot_size, slot_margin, input_text, mouse_pos, personnage=None, message=None, message_timer=0):
    """
    Dessine la barre de saisie pour les cheats et met à jour l'inventaire si nécessaire.
    Retourne l'état mis à jour : input_text, message, message_timer.
    """
    if not tous_les_objets:
        print("Erreur : tous_les_objets est vide. Vérifiez le chargement de data/items.json.")
        return input_text, message, message_timer, True

    input_rect = pygame.Rect(
        fenetre.get_width() // 2 - 150,
        fenetre.get_height() // 2 - 20,
        300,
        40
    )
    couleur_fond = (50, 60, 70)
    couleur_bordure = (255, 222, 89)
    
    # Liste des IDs valides pour l'affichage
    valid_ids = ["1", "2", "3"]  # Basé sur le JSON
    
    # Redessiner l'interface de l'inventaire en arrière-plan
    draw_inventory_interface(
        fenetre, inventaire_joueur, tous_les_objets, images_objets,
        font_titre, font_texte, couleur_bouton, gris_fonce, fond_section,
        slot_base_color, slot_hover_color, fond_transparent, mouse_pos,
        misc_rect, stats_rect, slot_size, slot_margin, personnage
    )
    
    # Afficher l'instruction
    instruction = "Entrez l'ID de l'objet (ex: 1, 2, 3)"
    texte_instruction = font_texte.render(instruction, True, couleur_texte)
    texte_rect_instruction = texte_instruction.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 2 - 100))
    fenetre.blit(texte_instruction, texte_rect_instruction)
    
    # Afficher la liste des IDs valides
    valid_ids_text = f"IDs valides : {', '.join(valid_ids)}"
    texte_valid_ids = font_texte.render(valid_ids_text, True, couleur_texte)
    texte_valid_ids_rect = texte_valid_ids.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 2 - 60))
    fenetre.blit(texte_valid_ids, texte_valid_ids_rect)
    
    # Dessiner la boîte de saisie
    draw_input_box(fenetre, input_text, input_rect, font_texte, True, couleur_texte, couleur_fond, couleur_bordure)
    
    # Afficher le message temporaire
    if message and pygame.time.get_ticks() < message_timer:
        texte = font_texte.render(message, True, couleur_texte)
        texte_rect = texte.get_rect(center=(fenetre.get_width() // 2, fenetre.get_height() // 2 + 50))
        fenetre.blit(texte, texte_rect)
    
    return input_text, message, message_timer, True