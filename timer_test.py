import pygame

# 初始化 Pygame
pygame.init()

# 建立視窗
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("定時器示範")

# 定義一個自訂事件
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # 每1000毫秒觸發一次

# 主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == TIMER_EVENT:
            print("⏰ Timer triggered!")

    screen.fill((0, 0, 0))  # 清空畫面為黑色
    pygame.display.flip()   # 更新畫面

# 離開 Pygame
pygame.quit()

