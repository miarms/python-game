import pygame
from src.utils.open_our_window import open_our_window
def move():
    pygame.init()
    ROUGE = (255, 0, 0)
    x = 100
    y = 100
    taille = 50
    vitesse = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            x -= vitesse
        if touches[pygame.K_RIGHT]:
            x += vitesse
        if touches[pygame.K_UP]:
            y -= vitesse
        if touches[pygame.K_DOWN]:
            y += vitesse
        pygame.draw.rect(open_our_window(), ROUGE, (x, y, taille, taille))
        pygame.display.update()
move()