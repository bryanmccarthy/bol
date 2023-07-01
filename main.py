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
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 8
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -16
            self.jump_sound.play()

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
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)

# Player 
player = pygame.sprite.GroupSingle()
player.add(Player())

# Enemies
enemy_group = pygame.sprite.Group()
enemies = []

# Game inactive screen player
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    bg_music.play(loops = -1)
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
        player.sprite.rect.x = 80
        enemies.clear()
        player_gravity = 0
        bg_music.stop()
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
