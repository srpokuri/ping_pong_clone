from curses.textpad import rectangle

import pygame
import sys

from pygame import Vector2
#Start game
pygame.init()
hit_sound = pygame.mixer.Sound("Pong_bounce.wav")
wall_hit_sound = pygame.mixer.Sound("Pong_wall.wav")
score_sound = pygame.mixer.Sound("score.mp3")
#Screen setup
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pong")
#Initial Values
ball = Vector2(640,360)
player_pos = Vector2(340,360)
opponent = Vector2(940,360)
keys = 0
up = True
left = True
ball_speed = Vector2(5,0)
player_speed = 10
# Game Loop
clock = pygame.time.Clock()
running = True
player_score = 0
opponent_score = 0
#reset method to reset after a scoring
countdown = 0
def reset():
    global player_pos
    global opponent
    global ball
    global player_speed
    global opponent_speed
    global ball_speed
    global countdown
    ball = Vector2(640, 360)
    player_pos = Vector2(340, 360)
    opponent = Vector2(940, 360)
    ball_speed = Vector2(0, 0)
    player_speed = 0
    score_sound.play()
    countdown = 4
#Collision check method
def CheckCollision(val: Vector2, val1: Vector2):
    global ball_speed
    bo = (val.x > val1.x + 35) or (val.x + 25 < val1.x) or (val.y > val1.y + 110) or (val.y + 25 < val1.y)
    return not bo
#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Drawing everything
    screen.fill("white")
    pygame.draw.circle(screen, "blue", ball, 25)
    pygame.draw.rect(screen,"red",pygame.Rect(player_pos.x,player_pos.y,10,100))
    pygame.draw.rect(screen,"black",pygame.Rect(opponent.x,opponent.y,10,100))
    #Score board
    my_score = pygame.font.Font(None, 70).render(str(player_score), False, "blue")
    not_my_score = pygame.font.Font(None, 70).render(str(opponent_score), False, "blue")
    screen.blit(my_score,(0,0))
    screen.blit(not_my_score,(1250,0))
    if countdown>0:
        screen.blit(pygame.font.Font(None,70).render(str(countdown-1),False,"Red"),(640,360))
        pygame.time.delay(500)
        countdown-=1
    if player_speed==0 and countdown==0:
        player_speed=10
        ball_speed.x=5
    #Collision checks and speed boosts
    if CheckCollision(ball,opponent):
        left = True
        ball_speed.x+=1
        ball_speed.y+=1
        hit_sound.play()
    if CheckCollision(ball,player_pos):
        left = False
        ball_speed.x += 1
        ball_speed.y += 1
        hit_sound.play()

    #horizontal ball movement and score checks
    if left:
        ball.x-=ball_speed.x
        if ball.x<200:
            opponent_score+=1
            reset()
    else:
        ball.x+=ball_speed.x
        if ball.x>1100:
            player_score+=1
            reset()
    #ball vertical movement and opponent movement(since opponemt plays according to ball)
    if up:
        ball.y-=ball_speed.y
        opponent.y-=ball_speed.y*0.9
        if ball.y<15:
            up = False
            wall_hit_sound.play()
    else:
        ball.y += ball_speed.y
        opponent.y += ball_speed.y*0.9
        if ball.y > 695:
            up = True
            wall_hit_sound.play()
    #player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y-=player_speed
        if player_pos.y<1:
            player_pos.y+=player_speed
    if keys[pygame.K_s]:
        player_pos.y+=player_speed
        if player_pos.y>620:
            player_pos.y-=player_speed
    pygame.display.flip()
    clock.tick(60)/1000
pygame.quit()
sys.exit()


