import random
import pygame
import sys

from pygame.locals import *

class Enemy:
    enemy_posX = 0
    enemy_posY = 0
    enemy_height = 150
    def __init__(self, enemy_posX, enemy_posY, enemy_height):
        self.enemy_posX = enemy_posX
        self.enemy_posY = enemy_posY
        self.enemy_height = enemy_height

def main(gamestate, character):
    pygame.init()

    width = 800
    height = 450

    DISPLAY = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy Bird")

    bright = 35
    gray = (bright, bright, bright)


    bird = pygame.image.load("media/bird.png").convert_alpha()
    wing = pygame.image.load("media/wing.png").convert_alpha()
    characters = [bird, wing]

    enemy_distance = 200
    enemy_width = 20

    enemies = []
    for i in range(4):
        t_enemy_height = random.randint(20, 300)
        b_enemy_height = 275 - t_enemy_height
        group = [Enemy(width + (i * enemy_distance) + 20, 0, t_enemy_height),
                 Enemy(width + (i * enemy_distance) + 20, height - b_enemy_height, b_enemy_height)]
        enemies.append(group)

    posX = 50
    posY = height/2 - characters[character].get_height()/2
    speed = 0.075

    enemy_speed = 0.06

    font = pygame.font.SysFont("media/soloist.ttf", 80)
    font_small = pygame.font.SysFont("media/soloist.ttf", 45)

    score = 0
    new_enemy_height = 0
    player_speedup = True
    enemy_speedup = True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        press = pygame.key.get_pressed()

        DISPLAY.fill(gray)

        if gamestate == 0:
            welcome = font.render("Welcome to Flappy Bird", False, (255, 250, 250))
            choose = font_small.render("Choose your character (arrow keys)", False, (255, 255, 255))
            begin = font_small.render("Press Enter to start", False, (255, 255, 255))
            DISPLAY.blit(welcome, (width/2 - welcome.get_width()/2, 50))
            DISPLAY.blit(choose, (width/2 - choose.get_width()/2, 150))
            DISPLAY.blit(begin, (width/2 - begin.get_width()/2, 350))
            if press[pygame.K_LEFT] and character > 0:
                character -= 1
            if press[pygame.K_RIGHT] and character < 1:
                character += 1
            DISPLAY.blit(characters[character], (width/2 - characters[character].get_width()/2, 250 + characters[character].get_height()/4))

            if press[pygame.K_RETURN]:
                main(1, character)

        if gamestate == 1:
            # Move character
            if press[pygame.K_UP] and posY > 0:
                posY -= speed
            if press[pygame.K_DOWN] and posY < height - 35:
                posY += speed

            # Displaying and moving Enemies
            for group in enemies:
                for enemy in group:
                    # Displaying Enemies
                    pygame.draw.rect(DISPLAY, (160, 160, 160), (enemy.enemy_posX, enemy.enemy_posY, enemy_width, enemy.enemy_height))
                    # Moving Enemies
                    enemy.enemy_posX -= enemy_speed
                    # Enemy Respawns
                    if enemy.enemy_posX < -20:
                        new_posY = 0
                        if group.index(enemy) == 0:
                            new_enemy_height = random.randint(20, 300)
                        if group.index(enemy) == 1:
                            new_enemy_height = 310 - new_enemy_height
                            new_posY = height - new_enemy_height
                        enemy.enemy_posX = width
                        enemy.enemy_posY = new_posY
                        enemy.enemy_height = new_enemy_height
                    # Checking if you die
                    if enemy.enemy_posX < posX + characters[character].get_width() < enemy.enemy_posX + enemy_width:
                        if group.index(enemy) == 0 and enemy.enemy_height > posY:
                            gamestate = 2
                        if group.index(enemy) == 1 and enemy.enemy_posY < posY + characters[character].get_height():
                            gamestate = 2
                if 50 > group[0].enemy_posX > 50 - enemy_speed:
                    score += 1
                    player_speedup = True
                    enemy_speedup = True

            if score % 10 == 0 and score != 0 and player_speedup:
                speed += 0.015
                round(speed)
                player_speedup = False
            if score % 5 == 0 and score != 0 and enemy_speedup:
                enemy_speed += 0.01
                round(enemy_speed)
                enemy_speedup = False

            # Displaying character
            DISPLAY.blit(characters[character], (posX, posY))

            # Displaying score
            text = font.render(str(score), False, (255, 250, 250))
            DISPLAY.blit(text, (10, 10))
        if gamestate == 2:
            text = font.render("GAME OVER", False, (255, 250, 250))
            text2 = font.render("You got a Score of: " + str(score), False, (255, 250, 250))
            text3 = font_small.render("Press Enter to restart", False, (255, 250, 250))
            DISPLAY.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2 - 70))
            DISPLAY.blit(text2, (width/2 - text2.get_width()/2, height/2 - text2.get_height()/2))
            DISPLAY.blit(text3, (width/2 - text3.get_width()/2, height/2 - text3.get_height()/2 + 70))

            if press[pygame.K_RETURN]:
                main(1, character)
            if press[pygame.K_ESCAPE]:
                main(0, character)
        pygame.display.update()

main(0, 0)
