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
            self.rect.x += dx / dist * 1.1
            self.rect.y += dy / dist * 1.1

angle_offset = 0

class OrbitBall(pygame.sprite.Sprite):
    def __init__(self, player_pos, radius, angle_offset):
        super().__init__()
        self.image = pygame.image.load("assets/orbit.png").convert_alpha()
        self.image= pygame.transform.scale(self.image, (35,35))
        self.rect = self.image.get_rect()
        self.radius = radius
        self.angle = angle_offset
        self.player_pos = player_pos

    def update(self):
        # 更新繞圓的角度與位置
        self.angle += 0.05
        cx = self.player_pos[0] + player_size // 2
        cy = self.player_pos[1] + player_size // 2
        self.rect.centerx = int(cx + math.cos(self.angle) * self.radius)
        self.rect.centery = int(cy + math.sin(self.angle) * self.radius)
        # 不需要自己移除，由外部判斷移除

class HomingRocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.Surface((20, 10), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 200, 0), [(0, 0), (20, 5), (0, 10)])
        self.rect = self.image.get_rect(center=(x, y))
        self.target = target
        self.speed = 5

    def update(self):
        if not self.target.alive():
            self.kill()
            return
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist < 5:
            self.kill()
            self.target.kill()
        else:
            self.rect.x += int(dx / dist * self.speed)
            self.rect.y += int(dy / dist * self.speed)


# 玩家設定
player_pos = [275, 300]
player_size = 50

# Sprite 群組
arrow_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
orbit_group = pygame.sprite.Group()
rocket_group = pygame.sprite.Group()

SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 400)
SPAWN_ARROW = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_ARROW, 300)
SPAWN_ORBIT = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWN_ORBIT, 1000)
SPAWN_ROCKET = pygame.USEREVENT + 4
pygame.time.set_timer(SPAWN_ROCKET, 1000)

# 玩家圖片
player_img = pygame.image.load("assets/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_size, player_size))  # 可根據需要縮放


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
        if event.type == SPAWN_ENEMY:
            #加入敵人（每幾秒生成一個）：
            enemy_x = random.randint(-300, 300)
            enemy_y = random.randint(-200, 200)
            enemy_dx = player_pos[0]+ enemy_x
            enemy_dy = player_pos[1]+ enemy_y
            #敵人生成在一定距離外
            if math.hypot(player_pos[0] - enemy_dx, player_pos[1] - enemy_dy) > 100:
                enemy_group.add(Enemy(enemy_dx, enemy_dy))
        if event.type == SPAWN_ARROW:
            # 生成弓箭
            cx = player_pos[0] + player_size // 2
            cy = player_pos[1] + player_size // 2
            arrow_group.add(Arrow(cx, cy, 0, -10))  # 上
            arrow_group.add(Arrow(cx, cy, 10, 0))   # 右
            arrow_group.add(Arrow(cx, cy, 0, 10))   # 下
            arrow_group.add(Arrow(cx, cy, -10, 0))  # 左
        if event.type == SPAWN_ORBIT:
            if len(orbit_group) < 3:
                orbit_group.add(OrbitBall(player_pos, 50, angle_offset))
                angle_offset += math.pi * 2 / 3  # 不同起始角度


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


    # 畫敵人
    arrow_group.update()
    enemy_group.update(player_pos)
    orbit_group.update()
    orbit_group.draw(screen)
    arrow_group.draw(screen)
    enemy_group.draw(screen)

    # 檢測2組碰撞
    pygame.sprite.groupcollide(enemy_group, arrow_group, True, True)
    pygame.sprite.groupcollide(enemy_group, orbit_group, True, False)


    # 更新畫面
    pygame.display.update()

pygame.quit()

