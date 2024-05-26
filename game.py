import pygame
import random

pygame.init()

WIDTH = 945
HEIGHT = 600
display_surface = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Clown")

#colors
YELLOW = (255 , 255 , 0)
BLUE = (0 , 0, 255)
BLACK = (0 , 0, 0)


#set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#game variables
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCERLATION = .5

score = 0
player_lives = PLAYER_STARTING_LIVES

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1 , 1])
clown_dy = random.choice([-1 , 1])

#set fonts
font = pygame.font.Font('custom.ttf' , 32)
#set text
title_text = font.render('Catch the Clown' , 1 ,BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50 , 10)

score_text = font.render("Score: " + str(score) , 1, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WIDTH - 50 , 10)

lives_text = font.render("Lives: " + str(player_lives) , 1 ,YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright= (WIDTH - 50 , 50)

game_over_text = font.render("GAMEOVER" , 1, BLUE , YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WIDTH //2 , HEIGHT // 2)

continue_text = font.render("Press any key to play again" , 1, BLUE , YELLOW)
continue_rect = continue_text.get_rect()
continue_rect.center = (WIDTH //2 , HEIGHT //2 + 64)

#set sound and music
clicked_sound = pygame.mixer.Sound('clicked.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
pygame.mixer.music.load('bg.wav')


yellow_rect = pygame.Rect(0 , 0 , WIDTH // 2, HEIGHT)
blue_rect = pygame.Rect(WIDTH // 2 , 0  , WIDTH , HEIGHT)

#set image 
clown_img = pygame.image.load('clown.png')
clown_rect = clown_img.get_rect()
clown_rect.center = (WIDTH //2 , HEIGHT //2)

pygame.mixer.music.play(-1 , 0.0)
#game loop
running = True
while running:
    display_surface.fill(YELLOW , yellow_rect)
    display_surface.fill(BLUE , blue_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            if clown_rect.collidepoint(mouse_x , mouse_y):
                score += 1
                clicked_sound.play()
                clown_velocity += CLOWN_ACCERLATION
                previous_dx = clown_dx
                previous_dy = clown_dy
                while(previous_dx == clown_dx and previous_dy == clown_dy):
                    clown_dx = random.choice([-1 , 1])
                    clown_dy = random.choice([-1, 1])
            else:
                player_lives -= 1
                miss_sound.play()
    clown_rect.x += clown_dx*clown_velocity
    clown_rect.y += clown_dy*clown_velocity

    if clown_rect.left <= 0  or clown_rect.right >= WIDTH  :
        clown_dx *= -1
    if clown_rect.top <= 0  or clown_rect.bottom >= HEIGHT:
        clown_dy *= -1 

    if player_lives == 0:
        display_surface.blit(game_over_text ,game_over_rect)
        display_surface.blit(continue_text , continue_rect)
        pygame.display.update()

        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    clown_rect.center = (WIDTH // 2, HEIGHT //2)
                    clown_velocity = CLOWN_STARTING_VELOCITY
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1 , 1])
                    pygame.mixer.music.play(-1 , 0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
    score_text = font.render("Score: " + str(score) , 1, YELLOW)
    lives_text = font.render("Lives: " + str(player_lives) , 1, YELLOW)
    display_surface.blit(title_text , title_rect)
    display_surface.blit(score_text , score_rect)
    display_surface.blit(lives_text , lives_rect)
    
    display_surface.blit(clown_img , clown_rect)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()