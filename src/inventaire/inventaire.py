import pygame
from .cheat_code import cheats_code
from .interface_utils import draw_inventory_interface, draw_close_button

def inventaire(fenetre, inventaire_joueur, tous_les_objets, font_texte, couleur_texte, personnage, mouse_pos=(0, 0)):
    # Pas besoin de pygame.init() ici, déjà fait dans map_1.py
    
    largeur_inventaire = 1540
    hauteur_inventaire = 800
    # Pas besoin de set_caption ici, on utilise la même fenêtre

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
    
    # Ajuster misc_rect pour 3 lignes
    misc_width = 10 * (slot_size + slot_margin) + slot_margin  # 10 slots par ligne
    misc_height = 3 * (slot_size + slot_margin) + slot_margin  # 3 lignes
    misc_rect = pygame.Rect(
        50,  # x position
        hauteur_inventaire - misc_height - 50,  # y position
        misc_width,  # width
        misc_height  # height
    )
    
    stats_width = 300
    stats_height = 200
    stats_rect = pygame.Rect(
        largeur_inventaire - stats_width - 50,
        hauteur_inventaire - stats_height - 50,
        stats_width,
        stats_height
    )

    close_button_rect = pygame.Rect(largeur_inventaire - 50, 10, 40, 40)
    
    # Cache pour les images (charger une seule fois)
    if not hasattr(inventaire, "images_objets"):
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
        inventaire.images_objets = images_objets
    else:
        images_objets = inventaire.images_objets

    # Dessiner l'interface
    draw_inventory_interface(
        fenetre, inventaire_joueur, tous_les_objets, images_objets,
        font_titre, font_texte, couleur_bouton, gris_fonce, fond_section,
        slot_base_color, slot_hover_color, fond_transparent, mouse_pos,
        misc_rect, stats_rect, slot_size, slot_margin, personnage
    )

    draw_close_button(fenetre, close_button_rect, couleur_bouton)
    
    return True  # Indique que l'inventaire est affiché