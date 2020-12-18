import pygame, sys, random

def draw():
    pygame.draw.rect(screen, gen_color, player)
    pygame.draw.rect(screen, gen_color, opponent)
    pygame.draw.ellipse(screen, gen_color, ball)
    pygame.draw.aaline(screen, gen_color, (screen_width//2, 0), (screen_width//2,screen_height))

# The score
def draw_score(player_score, opponent_score):
    player_score_text = game_font.render(str(player_score), True, gen_color)
    opponent_score_text = game_font.render(str(opponent_score), True, gen_color)
    player_score_rect = player_score_text.get_rect(center = (screen_width - (screen_width//4), 20))
    opponent_score_rect = opponent_score_text.get_rect(center = (screen_width//4, 20))
    screen.blit(player_score_text, player_score_rect)
    screen.blit(opponent_score_text, opponent_score_rect)

# The ball movement
def ball_movement():
    global ball_x_change, ball_y_change, opponent_score, player_score, score_time
    ball.x += ball_x_change
    ball.y += ball_y_change

    if ball.left <= 0:
        player_score += 1
        score_sound.play()
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        opponent_score += 1
        score_sound.play()
        score_time = pygame.time.get_ticks()


    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_y_change = - ball_y_change
        collide_sound.play()

# Player movement
def player_movement():

    player.y += player_y_change
    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height

# Collision between the paddles and the ball
def paddle_ball_collision():
    global ball_x_change
    if player.colliderect(ball):
        ball_x_change = - ball_x_change
        collide_sound.play()

    if opponent.colliderect(ball):
        ball_x_change = - ball_x_change
        collide_sound.play()

# Moving the opponent
def opponent_movement():
    if ball.y < opponent.y - paddle_height // 8:
        opponent.y -= opponent_y_change

    if ball.y > opponent.y + paddle_height - paddle_height // 8:
        opponent.y += opponent_y_change

    if opponent.top <= 0:
        opponent.top = 0

    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

# Resetting the ball and the time counter
def reset_ball():
    global ball_x_change, ball_y_change, score_time
    ball.x = (screen_width//2) - (20//2)
    ball.y = (screen_height//2) - (20//2)

    current_time = pygame.time.get_ticks()

    if current_time - score_time < 1000:
        number_three_text = timer_font.render("3", True, gen_color)
        number_three_rect = number_three_text.get_rect(center = (screen_width // 2 , screen_height //2 -40))
        screen.blit(number_three_text, number_three_rect)

    if 1000 < current_time - score_time < 2000:
        number_two_text = timer_font.render("2", True, gen_color)
        number_two_rect = number_two_text.get_rect(center = (screen_width // 2, screen_height //2 -40))
        screen.blit(number_two_text, number_two_rect)

    if 2000 < current_time - score_time < 3000:
       number_one_text = timer_font.render("1", True, gen_color)
       number_one_rect = number_one_text.get_rect(center = (screen_width // 2, screen_height //2 -40))
       screen.blit(number_one_text, number_one_rect)

    if current_time - score_time < 3000:
        ball_x_change, ball_y_change = 0, 0
        player.y = (screen_height//2) - (paddle_height//2)
        opponent.y = (screen_height//2) - (paddle_height//2)
    else:
        ball_x_change, ball_y_change = 5 * random.choice((1,-1)), 5 * random.choice((1,-1))
        score_time = False

pygame.init()

# Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Clock
clock = pygame.time.Clock()

# Colors
bg_color = pygame.Color("#2b2b2b")
gen_color = pygame.Color(pygame.Color("#ff7259"))

# Fonts
game_font = pygame.font.SysFont("monospace", 30)
timer_font = pygame.font.SysFont("monospace", 70)

# Score
player_score = 0
opponent_score = 0

# Paddle variables
paddle_width = 15
paddle_height = 150

# Player variables
player_x = screen_width - 17
player_y = (screen_height//2) - (paddle_height//2)
player_y_change = 0

#Opponent variables
opponent_x = 2
opponent_y = (screen_height//2) - (paddle_height//2)
opponent_y_change = 5

#Ball variables
ball_width = 20
ball_height = 20
ball_x = (screen_width//2) - (20//2)
ball_y = (screen_height//2) - (20//2)
ball_x_change = 5
ball_y_change = 5

#Rects
player = pygame.Rect(player_x, player_y, paddle_width, paddle_height)
opponent = pygame.Rect(opponent_x, opponent_y, paddle_width, paddle_height)
ball = pygame.Rect(ball_x, ball_y, ball_width, ball_height)

# Sounds
collide_sound = pygame.mixer.Sound("sound/pong.ogg")
score_sound = pygame.mixer.Sound("sound/score.ogg")

# Timer
score_time = None


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y_change = -5

            if event.key == pygame.K_DOWN:
                player_y_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    screen.fill(bg_color)

    if score_time:
        reset_ball()

    player_movement()
    opponent_movement()
    paddle_ball_collision()
    ball_movement()
    draw_score(player_score, opponent_score)
    draw()

    pygame.display.update()
    clock.tick(100)
