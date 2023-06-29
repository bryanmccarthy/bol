import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

score_surface = text_font.render('bol', False, 'black')
score_rect = score_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load('graphics/snail/Snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            if player_rect.collidepoint(event.pos): print("collision")
            
    # test movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_rect.x -= 5
    if keys[pygame.K_d]:
        player_rect.x += 5
    
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(score_surface, score_rect)

    snail_rect.x -= 4 
    if snail_rect.right <= 0: snail_rect.left = 800

    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    if player_rect.colliderect(snail_rect):
        print("collision")   

    #if player_rect.collidepoint(pygame.mouse.get_pos()):
    #    print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)
