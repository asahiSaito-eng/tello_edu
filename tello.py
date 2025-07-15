from djitellopy import Tello
import pygame
import time

# 初期化
tello = Tello()
tello.connect()
print("Battery:", tello.get_battery(), "%")

tello.streamoff()  # 念のためOFFに
tello.streamon()   # カメラストリームON（必要な場合）

# Pygame設定
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Tello Real-Time Controller")
clock = pygame.time.Clock()

# 離陸状態管理
flying = False

# メインループ
running = True
while running:
    # 入力初期化
    lr = 0  # 左右 (A/D)
    fb = 0  # 前後 (W/S)
    ud = 0  # 上下 (↑/↓)
    yaw = 0 # 回転 (←/→)

    # イベントチェック
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ESCで終了
    if keys[pygame.K_ESCAPE]:
        running = False

    # 離陸/着陸切り替え（Enterキー）
    if keys[pygame.K_RETURN]:
        if not flying:
            tello.takeoff()
            flying = True
        else:
            tello.land()
            flying = False
        time.sleep(1)  # 連続入力防止

    # 移動制御
    if keys[pygame.K_w]:
        fb = 50
    elif keys[pygame.K_s]:
        fb = -50

    if keys[pygame.K_a]:
        lr = -50
    elif keys[pygame.K_d]:
        lr = 50

    if keys[pygame.K_UP]:
        ud = 50
    elif keys[pygame.K_DOWN]:
        ud = -50

    if keys[pygame.K_LEFT]:
        yaw = -50
    elif keys[pygame.K_RIGHT]:
        yaw = 50

    # RC送信（毎フレーム）
    if flying:
        tello.send_rc_control(lr, fb, ud, yaw)

    clock.tick(30)  # 30FPS制限（高速すぎないように）

# 終了処理
if flying:
    tello.land()
pygame.quit()

