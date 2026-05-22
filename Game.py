import pygame
import random
import sys

# Variables
GAME_NAME = "PyGame Project"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PLAYER_WIDTH = 250
PLAYER_HEIGHT = 80
PLAYER_SPEED = 3
ENEMY_WIDTH = 135
ENEMY_HEIGHT = 44

ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 2
ENEMY_SPAWN_RATE = 105
MAX_ENEMIES = 6

BULLET_WIDTH = 8   
BULLET_HEIGHT = 40
BULLET_SPEED = 1
MAX_BULLETS = 5


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

font_style = pygame.font.SysFont("monospace", 35)
game_over_font = pygame.font.SysFont("monospace", 75)
clock = pygame.time.Clock()

# Load Images
background_image = None
try:
    raw_image = pygame.image.load('./Sea.jpg')
    background_image = pygame.transform.scale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Impossible de charger l'image de fond Sea.jpg : {e}\nFond noir par défaut.")

player_image = None
try:
    raw_player_img = pygame.image.load('./Ship.png')
    player_image = pygame.transform.scale(raw_player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
except pygame.error as e:
    print(f"Impossible de charger l'image du joueur Ship.png : {e}\nRectangle bleu par défaut.")

torpilla_image = None
try:
    raw_torpilla_img = pygame.image.load('./Torpilla.png')
    torpilla_image = pygame.transform.scale(raw_torpilla_img, (BULLET_WIDTH, BULLET_HEIGHT))
except pygame.error as e:
    print(f"Impossible de charger l'image de la torpille Torpilla.png : {e}\nRectangle vert par défaut.")

enemy_image_right = None
enemy_image_left = None
try:
    raw_enemy_img = pygame.image.load('./SubmarineA.png')
    enemy_image_right = pygame.transform.scale(raw_enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
    enemy_image_left = pygame.transform.flip(enemy_image_right, True, False)
except pygame.error as e:
    print(f"Impossible de charger l'image de l'ennemi SubmarineA.png : {e}\nRectangle rouge par défaut.")


# Load Audio
try:
    pygame.mixer.music.load('./background_theme.mp3')
    fire_sound = pygame.mixer.Sound('./sonar.mp3')
    fire_sound.set_volume(0.5)
except pygame.error as e:
    print(f"Erreur audio : {e}")

pygame.mixer.music.play(loops=-1)


# Functions
def draw_player(player_rect):
    if player_image:
        screen.blit(player_image, (player_rect.x, player_rect.y))
    else:
        pygame.draw.rect(screen, BLUE, player_rect)

def display_score(score):
    score_text = font_style.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

def message(msg, color, y_displace=0, font=font_style):
    mesg = font.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_displace))
    screen.blit(mesg, mesg_rect)


# Main Function
def game_loop():
    game_over = False
    game_close = False

    player_rect = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) / 2, 70, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_x_change = 0

    enemy_list = []
    bullet_list = []
    score = 0
    enemy_timer = 0

    while not game_close:
        while game_over:
            screen.fill(BLACK)
            message("Game Over!", RED, y_displace=-50, font=game_over_font)
            message(f"Final Score: {score}", WHITE, y_displace=20)
            message("Press Q-Quit or C-Play Again", WHITE, y_displace=70)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over, game_close = False, True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over, game_close = False, True
                    if event.key == pygame.K_c:
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
                    fire_sound.play()
                    
                elif event.button == 3: # Right
                    bullet_x = player_rect.right - 50
                    bullet_list.append(pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))
                    fire_sound.play()

        # Update Position
        player_rect.x += player_x_change
        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(SCREEN_WIDTH, player_rect.right)

        # Torpillas
        for bullet in bullet_list[:]:
            bullet.y += BULLET_SPEED
            if bullet.top > SCREEN_HEIGHT:
                bullet_list.remove(bullet)

        # Spawn Ennemies
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
                'speed': actual_speed
            })

        # Ennemies Move
        for enemy_data in enemy_list[:]:
            enemy_rect = enemy_data['rect']
            enemy_rect.x += enemy_data['speed']
            if (enemy_data['speed'] > 0 and enemy_rect.left > SCREEN_WIDTH) or (enemy_data['speed'] < 0 and enemy_rect.right < 0):
                enemy_list.remove(enemy_data)

        # Collisions Torpillas/Ennemies
        for bullet in bullet_list[:]:
            for enemy_data in enemy_list[:]:
                if bullet.colliderect(enemy_data['rect']):
                    if bullet in bullet_list: bullet_list.remove(bullet)
                    if enemy_data in enemy_list: enemy_list.remove(enemy_data)
                    score += 2
                    break

        # Print
        screen.blit(background_image, (0, 0)) if background_image else screen.fill(BLACK)
        
        draw_player(player_rect)
        for enemy in enemy_list:
            if enemy_image_right and enemy_image_left:
                if enemy['speed'] > 0:
                    screen.blit(enemy_image_right, (enemy['rect'].x, enemy['rect'].y))
                else:
                    screen.blit(enemy_image_left, (enemy['rect'].x, enemy['rect'].y))
            else:
                pygame.draw.rect(screen, RED, enemy['rect'])
                
        for bullet in bullet_list:
            if torpilla_image:
                screen.blit(torpilla_image, (bullet.x, bullet.y))
            else:
                pygame.draw.rect(screen, GREEN, bullet)
        display_score(score)

        pygame.display.flip()
        clock.tick(80)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    game_loop()