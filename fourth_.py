import pygame
import random
import math

pygame.init()

# 建立視窗
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
pygame.display.set_caption("我的第一個遊戲")

# 顏色
white = (255, 255, 255)
purple = (204, 204, 255)
blue = (0, 51, 102)
green = (0, 200, 0)
black = (0,0,0)

# Sprite 類別
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.image.load("assets/arrow.png").convert_alpha()
        self.image= pygame.transform.scale(self.image, (30,30))  
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.right < 0 or self.rect.left > 600 or self.rect.bottom < 0 or self.rect.top > 400:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.image= pygame.transform.scale(self.image, (35,35))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player_pos):
        dx = player_pos[0] + 25 - self.rect.centerx
        dy = player_pos[1] + 25 - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += int(dx / dist * 1.5)
            self.rect.y += int(dy / dist * 1.5)

# 玩家設定
player_pos = [275, 300]
player_size = 50

# Sprite 群組
arrow_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

arrow_timer = 0
enemy_timer = 0

# 玩家圖片
player_img = pygame.image.load("assets/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_size, player_size))  # 可根據需要縮放

# 弓箭清單
arrows = []  # 每支箭為 [x, y, dx, dy] (x,y)代表位置 (dx,dy)代表移動量

# 步驟 1：敵人清單
enemies = []

running = True
while running:
    clock.tick(60)  # 控制 FPS
    screen.fill(purple)

    # 畫角色
    screen.blit(player_img, player_pos)

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制角色移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 2
    if keys[pygame.K_RIGHT] and player_pos[0] < (600 - player_size):
        player_pos[0] += 2
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= 2
    if keys[pygame.K_DOWN] and player_pos[1] < (400 - player_size):
        player_pos[1] += 2

    # 自動發射弓箭
    arrow_timer += 1
    if arrow_timer > 30:
        cx = player_pos[0] + player_size // 2
        cy = player_pos[1] + player_size // 2
        arrow_group.add(Arrow(cx, cy, 0, -10))  # 上
        arrow_group.add(Arrow(cx, cy, 10, 0))   # 右
        arrow_group.add(Arrow(cx, cy, 0, 10))   # 下
        arrow_group.add(Arrow(cx, cy, -10, 0))  # 左
        arrow_timer = 0

    #加入敵人（每幾秒生成一個）：
    enemy_timer += 1
    if enemy_timer > 20:  # 每秒生成三隻（假設 FPS=60）
        enemy_spawned = False
        while enemy_spawned == False:
            enemy_x = random.randint(-300, 300)
            enemy_y = random.randint(-200, 200)
            enemy_dx = player_pos[0]+ enemy_x
            enemy_dy = player_pos[1]+ enemy_y
            #敵人生成在一定距離外
            if math.hypot(player_pos[0] - enemy_dx, player_pos[1] - enemy_dy) > 100:
                enemy_group.add(Enemy(enemy_dx, enemy_dy))
                enemy_spawned = True

        enemies.append([enemy_dx,enemy_dy])
        enemy_timer = 0

    # 畫敵人
    arrow_group.update()
    enemy_group.update(player_pos)
    arrow_group.draw(screen)
    enemy_group.draw(screen)

    # 更新畫面
    pygame.display.update()

pygame.quit()

