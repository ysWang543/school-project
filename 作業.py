import pygame,random

from itertools import cycle


# 初始化 Pygame
pygame.init()

# 設定遊戲視窗大小
window = pygame.display.set_mode((288, 512))

# 設定遊戲標題
pygame.display.set_caption("Flappy Bird")

# 載入遊戲圖片
background = pygame.image.load("D:\期中報告/background.png").convert()
bird = pygame.image.load("D:\期中報告/bird.png").convert_alpha()
pipe = pygame.image.load("D:\期中報告/pipe.png")

# 設定遊戲字體
font = pygame.font.Font(None, 36)

# 初始化視窗和遊戲物件等等

clock = pygame.time.Clock()

# 宣告常數或變數
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 設定鳥的初始位置和速度
bird_x = 50
bird_y = 200
bird_speed = 0
gravity = 0.25

# 設定水管的初始位置和間隔
pipe_gap = 100
pipe_height = [200, 250, 300, 350]
pipe_positions = [(288, h) for h in pipe_height]
pipe_scored = [False, False, False, False]

# 設定遊戲分數和遊戲是否結束的狀態
score = 0
game_over = False

# 定義函式：更新遊戲物件位置
def update_objects():
    global bird_y, bird_speed, pipe_x, pipe_positions, score, game_over, pipe_scored
    # 更新鳥的位置
    bird_y += bird_speed
    bird_speed += gravity
    # 更新水管的位置
    for i, (x, y) in enumerate(pipe_positions):
        x -= 2
        pipe_positions[i] = (x, y)
        # 碰撞檢測
        if bird_x + bird.get_width() > x and bird_x < x + pipe.get_width() and \
           (bird_y < y + pipe.get_height() or bird_y + bird.get_height() > y + pipe.get_height() + pipe_gap):
            game_over = True
        # 加分檢測
        if x + pipe.get_width() < bird_x and not pipe_scored[i]:
            pipe_scored[i] = True
            score += 1
        
    # 移除已經超出螢幕的水管，並且新增新的水管
    if pipe_positions[0][0] < -pipe.get_width():
        pipe_positions.pop(0)
        pipe_heights = cycle(pipe_height)
        random_height = next(pipe_heights)
        pipe_positions.append((pipe_positions[-1][0] + 200, random_height))
        pipe_scored.pop(0)
        pipe_scored.append(False)

# 宣告常數或變數
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 定義函式：更新遊戲分數
def update_score():
    score_text = font.render("Score: {}".format(score), True, WHITE)
    window.blit(score_text, (10, 10))

# 定義函式：遊戲結束
def game_over_screen():
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
    window.blit(game_over_text, game_over_rect)

    score_text = font.render("Score: {}".format(score), True, WHITE)
    score_rect = score_text.get_rect(center=(window.get_width() // 2, window.get_height() // 2 + 50))
    window.blit(score_text, score_rect)

    restart_text = font.render("Press space to restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(window.get_width() // 2, window.get_height() // 2 + 100))
    window.blit(restart_text, restart_rect)


# 初始遊戲狀態為等待玩家開始遊戲
game_started = False


while True:
    # 事件迴圈
    for event in pygame.event.get():
        # 按下關閉視窗按鈕
        if event.type == pygame.QUIT:
            game_over = True
        # 按下空白鍵
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -8
                
    # 更新遊戲物件位置
    update_objects()

    # 繪製遊戲畫面
    window.blit(background, (0, 0))
    for x, y in pipe_positions:
        window.blit(pipe, (x, y))
    window.blit(bird, (bird_x, bird_y))

    # 更新遊戲分數
    update_score()

    # 遊戲結束畫面
    if game_over:
        game_over_screen()

    # 更新畫面
    pygame.display.update()

    # 控制遊戲速度
    clock.tick(60)


