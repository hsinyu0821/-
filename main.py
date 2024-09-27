import pygame
import random

pygame.init()

# 設置畫布
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("跑酷遊戲")

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 設置帧率
FPS = 60
clock = pygame.time.Clock()

# 定義字體
font_name = pygame.font.match_font('arial')

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_start_screen():
    win.fill(WHITE)
    draw_text(win, "跑酷遊戲", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(win, "按任意鍵開始", 22, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(score):
    win.fill(WHITE)
    draw_text(win, "遊戲結束", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(win, f"得分: {score}", 44, WIDTH // 2, HEIGHT // 2 - 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.gravity = 1
        self.jump_force = -15
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        if self.velocity > 10:
            self.velocity = 10  # 控制最大下降速度
        
        # 移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= HEIGHT:
            self.velocity = self.jump_force
        
        self.rect.y += self.velocity

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0  # 重設垂直速度

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

def add_obstacle(obstacles, speed):
    obstacle = Obstacle(speed)
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

def reset_game():
    global player, all_sprites, obstacles, start_ticks, game_over, score
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    obstacles = pygame.sprite.Group()
    
    start_ticks = pygame.time.get_ticks()
    pygame.time.set_timer(obstacle_spawn_event, obstacle_spawn_time)
    game_over = False
    score = 0

obstacle_spawn_time = 2000
obstacle_spawn_event = pygame.USEREVENT + 1

reset_game()
show_start_screen()

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == obstacle_spawn_event and not game_over:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
            obstacle_speed = 5 + elapsed_time // 10
            add_obstacle(obstacles, obstacle_speed)
            if elapsed_time < 60:
                new_spawn_time = int(2000 * (1 - elapsed_time / 60))
                pygame.time.set_timer(obstacle_spawn_event, new_spawn_time)

    if not game_over:
        all_sprites.update()

        score = (pygame.time.get_ticks() - start_ticks) // 1000

        if pygame.sprite.spritecollideany(player, obstacles):
            game_over = True
    
    win.fill(WHITE)
    all_sprites.draw(win)
    draw_text(win, f"得分: {score}", 22, WIDTH // 2, 10)
    
    pygame.display.flip()

    if game_over:
        show_game_over_screen(score)
        reset_game()

pygame.quit()
