import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

game_title = text_font.render('Bol', False, 'White')
game_title_rect = game_title.get_rect(center = (400, 50))

play_surface = text_font.render('SPACE to play', False, 'White')
play_rect = play_surface.get_rect(center = (400, 350))

snail_surface = pygame.image.load('graphics/snail/Snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (800, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# Game inactive screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale_by(player_stand, 2.5)
player_stand_rect = player_stand.get_rect(center = (400, 200))

start_time = 0

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render(f"{current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -16
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800 
                    player_rect.left = 50
                    start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= 8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += 8
                    
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Snail
        snail_rect.x -= 4 
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        if player_rect.colliderect(snail_rect):
            game_active = False

        #if player_rect.collidepoint(pygame.mouse.get_pos()):
        #    print(pygame.mouse.get_pressed())
    else:
        screen.fill((92, 129, 162))
        screen.blit(play_surface, play_rect)
        screen.blit(player_stand, player_stand_rect)
        score_message = text_font.render(f"Your score: {score}", False, "White")
        score_message_rect = score_message.get_rect(center = (400, 50))
        if score == 0:
            screen.blit(game_title, game_title_rect)
        else:
            screen.blit(score_message, score_message_rect)
        

    pygame.display.update()
    clock.tick(60)
