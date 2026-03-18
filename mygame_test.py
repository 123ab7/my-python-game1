import pygame
import sys
import random

pygame.init()

# 画面設定
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# プレイヤー
player = pygame.Rect(275, 700, 50, 50)
player_speed = 6

# 弾
bullets = []

# 敵
enemies = []
enemy_timer = 0

# スコア
score = 0
font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()

# メインループ
while True:
    clock.tick(60)
    screen.fill(BLACK)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 弾発射
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.x + 20, player.y, 10, 20))

    # キー入力
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # 画面外に行かないように
    player.x = max(0, min(WIDTH - player.width, player.x))

    # 弾の移動
    for bullet in bullets:
        bullet.y -= 10

    bullets = [b for b in bullets if b.y > 0]

    # 敵の生成
    enemy_timer += 1
    if enemy_timer > 30:
        enemy_x = random.randint(0, WIDTH - 40)
        enemies.append(pygame.Rect(enemy_x, 0, 40, 40))
        enemy_timer = 0

    # 敵の移動
    for enemy in enemies:
        enemy.y += 4

    # 当たり判定
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # ゲームオーバー判定
    for enemy in enemies:
        if enemy.y > HEIGHT:
            print("GAME OVER")
            pygame.quit()
            sys.exit()

    # 描画
    pygame.draw.rect(screen, WHITE, player)

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # スコア表示
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()