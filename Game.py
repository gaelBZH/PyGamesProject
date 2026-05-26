import pygame
import random
import sys

# Variables
GAME_NAME = "King of the Ocean"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PLAYER_WIDTH = 250
PLAYER_HEIGHT = 70
PLAYER_SPEED = 2
ENEMY_WIDTH = 135
ENEMY_HEIGHT = 44

ENNEMY_SHOOTRATE = 40 # 40%
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 2
ENEMY_SPAWN_RATE = 105
MAX_ENEMIES = 6

BULLET_WIDTH = 8   
BULLET_HEIGHT = 40
BULLET_SPEED = 1
ENEMY_BULLET_SPEED = 2
MAX_BULLETS = 3

LEVEL_1 = 0
LEVEL_2 = 20
LEVEL_3 = 50

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

font_style = pygame.font.SysFont("monospace", 35)
game_over_font = pygame.font.SysFont("monospace", 75)
clock = pygame.time.Clock()

# Load Images
background_image_1 = None
background_image_2 = None
background_image_3 = None
try:
    raw_image = pygame.image.load('./Sea1.jpg')
    background_image_1 = pygame.transform.scale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    raw_image = pygame.image.load('./Sea2.png')
    background_image_2 = pygame.transform.scale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    raw_image = pygame.image.load('./Sea3.png')
    background_image_3 = pygame.transform.scale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Unable to load Sea background image: {e}\nDefaulting to black background.")

# Load Game Over Image
gameover_image = None
try:
    raw_gameover_img = pygame.image.load('./gameover.png')
    gameover_image = pygame.transform.scale(raw_gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Unable to load gameover.png image: {e}\nDefaulting to text.")

player_image = None
try:
    raw_player_img = pygame.image.load('./Ship2.png')
    player_image = pygame.transform.scale(raw_player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
except pygame.error as e:
    print(f"Unable to load player image Ship.png: {e}\nDefaulting to blue rectangle.")

torpilla_image = None
enemy_torpilla_image = None
try:
    raw_torpilla_img = pygame.image.load('./Torpilla.png')
    torpilla_image = pygame.transform.scale(raw_torpilla_img, (BULLET_WIDTH, BULLET_HEIGHT))
    enemy_torpilla_image = pygame.transform.flip(torpilla_image, False, True)
except pygame.error as e:
    print(f"Unable to load torpedo image Torpilla.png: {e}\nDefaulting to green rectangle.")

enemy_image_right = None
enemy_image_left = None
try:
    raw_enemy_img = pygame.image.load('./SubmarineA.png')
    enemy_image_right = pygame.transform.scale(raw_enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
    enemy_image_left = pygame.transform.flip(enemy_image_right, True, False)
except pygame.error as e:
    print(f"Unable to load enemy image SubmarineA.png: {e}\nDefaulting to red rectangle.")


# Load Audio
try:
    pygame.mixer.music.load('./music.mp3')
    fire_sound = pygame.mixer.Sound('./sonar.mp3')
    fire_sound.set_volume(1)
except pygame.error as e:
    print(f"Audio error: {e}")
    fire_sound = None

if pygame.mixer.music.get_busy() == False:
    try:
        pygame.mixer.music.play(loops=-1)
    except:
        pass


# Functions
def draw_player(player_rect):
    if player_image:
        screen.blit(player_image, (player_rect.x, player_rect.y))
    else:
        pygame.draw.rect(screen, BLUE, player_rect)

def display_score(score):
    score_text = font_style.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

def display_level(level):
    level_text = font_style.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, [10, 40])

def message(msg, color, y_displace=0, font=font_style):
    mesg = font.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_displace))
    screen.blit(mesg, mesg_rect)


# Main Function
def game_loop():
    global MAX_BULLETS, ENEMY_SPEED_MIN, ENEMY_SPEED_MAX, MAX_ENEMIES, PLAYER_SPEED

    game_over = False
    game_close = False
    level = 1

    player_rect = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) / 2, 70, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_x_change = 0

    enemy_list = []
    bullet_list = []
    enemy_bullet_list = []
    score = 0
    enemy_timer = 0

    while not game_close:
        while game_over:
            # If the Game Over image exists, display it, otherwise display the old black background with text
            if gameover_image:
                screen.blit(gameover_image, (0, 0))
            else:
                screen.fill(BLACK)
                message("Game Over!", RED, y_displace=-50, font=game_over_font)
            
            # Keep displaying score and controls on top
            message(f"Final Score: {score}", WHITE, y_displace=-260)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over, game_close = False, True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over, game_close = False, True
                    if event.key == pygame.K_p:
                        game_loop()

        # Events
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                game_close = True
                
            # Move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    player_x_change = PLAYER_SPEED
                    
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT and player_x_change < 0) or (event.key == pygame.K_RIGHT and player_x_change > 0):
                    player_x_change = 0

            # Shoot
            if event.type == pygame.MOUSEBUTTONDOWN and len(bullet_list) < MAX_BULLETS:
                bullet_y = player_rect.bottom
                
                if event.button == 1:   # Left
                    bullet_x = player_rect.left + 50
                    bullet_list.append(pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))
                    if fire_sound: fire_sound.play()
                    
                elif event.button == 3: # Right
                    bullet_x = player_rect.right - 50
                    bullet_list.append(pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))
                    if fire_sound: fire_sound.play()

        # Update Position
        player_rect.x += player_x_change
        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(SCREEN_WIDTH, player_rect.right)

        # Player Torpedoes
        for bullet in bullet_list[:]:
            bullet.y += BULLET_SPEED
            if bullet.top > SCREEN_HEIGHT:
                bullet_list.remove(bullet)

        # Spawn Enemies
        enemy_timer += 1
        if enemy_timer >= ENEMY_SPAWN_RATE and len(enemy_list) < MAX_ENEMIES:
            enemy_timer = 0
            side = random.choice([0, 1])
            enemy_speed = random.randrange(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX + 1)
            
            if side == 0:  # Left
                enemy_x, actual_speed = -ENEMY_WIDTH, enemy_speed
            else:          # Right
                enemy_x, actual_speed = SCREEN_WIDTH, -enemy_speed
                
            enemy_y = random.randrange(175, SCREEN_HEIGHT - 50)
            enemy_list.append({
                'rect': pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT), 
                'speed': actual_speed,
                'will_fire': random.random() <= ENNEMY_SHOOTRATE/100, 
                'fire_x': random.randrange(100, SCREEN_WIDTH - 100),
                'has_fired': False
            })

        # Enemies Move and Fire
        for enemy_data in enemy_list[:]:
            enemy_rect = enemy_data['rect']
            enemy_rect.x += enemy_data['speed']

            # Enemy Fire
            if enemy_data['will_fire'] and not enemy_data['has_fired']:
                if (enemy_data['speed'] > 0 and enemy_rect.centerx >= enemy_data['fire_x']) or \
                   (enemy_data['speed'] < 0 and enemy_rect.centerx <= enemy_data['fire_x']):
                    enemy_data['has_fired'] = True
                    enemy_bullet_list.append(pygame.Rect(
                        enemy_rect.centerx - BULLET_WIDTH // 2, 
                        enemy_rect.top, 
                        BULLET_WIDTH, 
                        BULLET_HEIGHT
                    ))

            # Delete Enemies outside
            if (enemy_data['speed'] > 0 and enemy_rect.left > SCREEN_WIDTH) or (enemy_data['speed'] < 0 and enemy_rect.right < 0):
                enemy_list.remove(enemy_data)

        # Enemy Torpedoes / Player Collisions
        for e_bullet in enemy_bullet_list[:]:
            e_bullet.y -= ENEMY_BULLET_SPEED
            if e_bullet.bottom < 170:
                enemy_bullet_list.remove(e_bullet)
            elif e_bullet.colliderect(player_rect):
                game_over = True

        # Player Torpedoes / Enemies Collisions
        for bullet in bullet_list[:]:
            for enemy_data in enemy_list[:]:
                if bullet.colliderect(enemy_data['rect']):
                    if bullet in bullet_list:
                        bullet_list.remove(bullet)
                    if enemy_data in enemy_list:
                        enemy_list.remove(enemy_data)
                    score += 2
                    if score >= LEVEL_3:
                        level = 3
                    elif score >= LEVEL_2:
                        level = 2
                    else:
                        level = 1
                    break

        # ======================= Drawing =======================

        # Draw Background and Update Levels
        if level == 1:
            screen.blit(background_image_1, (0, 0)) if background_image_1 else screen.fill(BLACK)
            MAX_BULLETS = 2
            ENEMY_SPEED_MIN = 1
            ENEMY_SPEED_MAX = 1
            MAX_ENEMIES = 3
            PLAYER_SPEED = 2
            ENNEMY_SHOOTRATE = 40
        elif level == 2:
            screen.blit(background_image_2, (0, 0)) if background_image_2 else screen.fill(BLACK)
            MAX_BULLETS = 5
            ENEMY_SPEED_MIN = 1
            ENEMY_SPEED_MAX = 2
            MAX_ENEMIES = 6
            PLAYER_SPEED = 3
            ENNEMY_SHOOTRATE = 60
        else:
            screen.blit(background_image_3, (0, 0)) if background_image_3 else screen.fill(BLACK)
            MAX_BULLETS = 8
            ENEMY_SPEED_MIN = 2
            ENEMY_SPEED_MAX = 3
            MAX_ENEMIES = 8
            PLAYER_SPEED = 4
            ENNEMY_SHOOTRATE = 80

        # Draw UI
        for i in range(MAX_BULLETS - len(bullet_list)):
            x = SCREEN_WIDTH - 10 - (i + 1) * (BULLET_WIDTH + 15)
            y = 10
            if torpilla_image:
                screen.blit(torpilla_image, (x, y))
            else:
                pygame.draw.rect(screen, GREEN, (x, y, BULLET_WIDTH, BULLET_HEIGHT))
        
        # Draw Player and Enemies
        draw_player(player_rect)
        for enemy in enemy_list:
            if enemy_image_right and enemy_image_left:
                if enemy['speed'] > 0:
                    screen.blit(enemy_image_right, (enemy['rect'].x, enemy['rect'].y))
                else:
                    screen.blit(enemy_image_left, (enemy['rect'].x, enemy['rect'].y))
            else:
                pygame.draw.rect(screen, RED, enemy['rect'])
                
        # Draw Player Torpedoes
        for bullet in bullet_list:
            if torpilla_image:
                screen.blit(torpilla_image, (bullet.x, bullet.y))
            else:
                pygame.draw.rect(screen, GREEN, bullet)

        # Draw Enemy Torpedoes
        for e_bullet in enemy_bullet_list:
            if enemy_torpilla_image:
                screen.blit(enemy_torpilla_image, (e_bullet.x, e_bullet.y))
            else:
                pygame.draw.rect(screen, RED, e_bullet)

        # Draw Score and Level
        display_score(score)
        display_level(level)

        pygame.display.flip()
        clock.tick(80)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    game_loop()