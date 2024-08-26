import pygame
import random

pygame.init()

# Kích thước màn hình
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)

# Thông số trò chơi
paddle_width, paddle_height = 10, 100
ball_radius = 7
paddle_speed = 10
ball_speed_x, ball_speed_y = 7, 7

# Tọa độ ban đầu
player_x, player_y = 10, height // 2 - paddle_height // 2
opponent_x, opponent_y = width - 20, height // 2 - paddle_height // 2
ball_x, ball_y = width // 2, height // 2

# Điểm số
player_score = 0
opponent_score = 0
font = pygame.font.SysFont("comicsansms", 35)

def draw():
    win.fill(black)
    player = pygame.Rect(player_x, player_y, paddle_width, paddle_height)
    opponent = pygame.Rect(opponent_x, opponent_y, paddle_width, paddle_height)
    ball = pygame.Rect(ball_x, ball_y, ball_radius * 2, ball_radius * 2)  # Sửa kích thước bóng
    pygame.draw.rect(win, white, player)
    pygame.draw.rect(win, white, opponent)
    pygame.draw.ellipse(win, white, ball)
    pygame.draw.aaline(win, white, (width // 2, 0), (width // 2, height))

    player_text = font.render(f"{player_score}", True, white)
    win.blit(player_text, (width // 4, 20))

    opponent_text = font.render(f"{opponent_score}", True, white)
    win.blit(opponent_text, (3 * width // 4, 20))

    pygame.display.update()

def ball_movement():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, player_score, opponent_score

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
        ball_speed_y *= -1

    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
    player_rect = pygame.Rect(player_x, player_y, paddle_width, paddle_height)
    opponent_rect = pygame.Rect(opponent_x, opponent_y, paddle_width, paddle_height)

    if ball_rect.colliderect(player_rect) or ball_rect.colliderect(opponent_rect):
        ball_speed_x *= -1

    if ball_x - ball_radius <= 0:
        opponent_score += 1
        reset_ball()

    if ball_x + ball_radius >= width:
        player_score += 1
        reset_ball()

def player_movement(keys):
    global player_y
    if keys[pygame.K_w] and player_y - paddle_speed > 0:
        player_y -= paddle_speed
    if keys[pygame.K_s] and player_y + paddle_speed < height - paddle_height:
        player_y += paddle_speed

def opponent_movement():
    global opponent_y
    if opponent_y + paddle_height / 2 < ball_y:
        opponent_y += paddle_speed
    if opponent_y + paddle_height / 2 > ball_y:
        opponent_y -= paddle_speed

    # Đảm bảo đối thủ không ra ngoài màn hình
    if opponent_y < 0:
        opponent_y = 0
    if opponent_y + paddle_height > height:
        opponent_y = height - paddle_height

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x, ball_y = width // 2, height // 2
    ball_speed_x *= random.choice((-1, 1))
    ball_speed_y *= random.choice((-1, 1))

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player_movement(keys)
        opponent_movement()
        ball_movement()
        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
