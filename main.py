import pygame
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 8
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -16

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/Snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/Snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 8
        if self.rect.x <= -50: self.destroy()

    def destroy(self):
        self.kill()

# Game Setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
score = 0
start_time = 0
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()
game_title = text_font.render('Bol', False, 'White')
game_title_rect = game_title.get_rect(center = (400, 50))
play_surface = text_font.render('SPACE to play', False, 'White')
play_rect = play_surface.get_rect(center = (400, 350))

# Player 
player = pygame.sprite.GroupSingle()
player.add(Player())

# Enemy
enemy_group = pygame.sprite.Group()

# Enemies
enemies = []

# Load Sprites
snail_frame_1 = pygame.image.load('graphics/snail/Snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/Snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale_by(player_stand, 2.5)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# Timers
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 250)

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render(f"{current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def enemy_movement(enemies):
    if enemies:
        for enemy_rect in enemies:
            enemy_rect.x -= 5
            if enemy_rect.bottom == 300:
                screen.blit(snail_surface, enemy_rect)
            else:
                screen.blit(fly_surface, enemy_rect)
        enemies = [enemy for enemy in enemies if enemy.x > -50]
        return enemies
    return []

def collisions(player, enemies):
    if enemies:
        for enemy in enemies:
            if player.colliderect(enemy):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
        enemy_group.empty()
        return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= 2: player_index  = 0
        player_surface = player_walk[int(player_index)]
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['fly', 'snail', 'snail'])))
            if event.type == snail_animation_timer:
                snail_frame_index = 1 if snail_frame_index == 0 else 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                fly_frame_index = 1 if fly_frame_index == 0 else 0
                fly_surface = fly_frames[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    player_rect.left = 50
                    start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Screen & Score
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Enemies
        enemy_group.draw(screen)
        enemy_group.update()

        # Collisions
        game_active = collision_sprite()
    else:
        # Game inactive state
        enemies.clear()
        player_gravity = 0
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
