import pygame
from .cheat_code import cheats_code
from .interface_utils import draw_inventory_interface

def inventaire(fenetre_inventaire, inventaire_joueur, tous_les_objets, font_texte, couleur_texte, personnage):
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
            clothing_rect, misc_rect, stats_rect, slot_size, slot_margin, personnage
        )
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()
