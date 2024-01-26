# Simple pygame program

# Import and initialize the pygame library
import pygame
from enum import IntEnum
import random

from pygame.locals import ( K_LEFT, K_RIGHT, K_RETURN, K_ESCAPE, KEYDOWN, QUIT )

class Move(IntEnum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

def determine_winner(p1, p2):
    if p1 == p2:
        return 0
    elif p1 == "Rock":
        if p2 == "Paper":
            return -1
        elif p2 == "Scissors":
            return 1
    elif p1 == "Paper":
        if p2 == "Scissors":
            return -1
        elif p2 == "Rock":
            return 1
    elif p1 == "Scissors":
        if p2 == "Rock":
            return -1
        elif p2 == "Paper":
            return 1

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0,0,0)
GREEN = (0, 255, 0)
# Create the screen object
# The size is determined by the constants SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Run until the user asks to quit
running = True
played = False
selected = Move.PAPER
comp_choice = None
while running:
    if played:
        m = "Rock" if selected == Move.ROCK else ("Paper" if selected == Move.PAPER else "Scissors")
        your_move = "You played " + m
        comp_move = "Computer played " + comp_choice
        result = determine_winner(m, comp_choice)
        game_status = "Tie!"
        if result == 1:
            game_status = "You Won!"
        if result == -1:
            game_status = "You Lost!"
        tag = "Hit return to play again"
        screen.fill((255, 255, 255))
        screen.blit(pygame.font.SysFont("Arial", 25).render(your_move, True, (0, 0, 0)), (50, 50))
        screen.blit(pygame.font.SysFont("Arial", 25).render(comp_move, True, (0, 0, 0)), (50, 80))
        screen.blit(pygame.font.SysFont("Arial", 25).render(game_status, True, (0, 0, 0)), (50, 110))
        screen.blit(pygame.font.SysFont("Arial", 25).render(tag, True, (0, 0, 0)), (50, 140))
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    played = False
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        continue


    # Did the user click the window close button?
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape Key?
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_LEFT:
                selected = (selected - 1) % 3
            if event.key == K_RIGHT:
                selected = (selected + 1) % 3
            if event.key == K_RETURN:
                played = True
                comp_choices = ["Rock", "Paper", "Scissors"]
                rand_idx = random.randint(0, len(comp_choices) - 1)
                comp_choice = comp_choices[rand_idx]
        # Did the user click the window close button?
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the background with white
    screen.fill((255, 255, 255))

    title1 = "Welcome to Rock Paper Scissors. Move Arrow Keys Left to Right"
    title2 = "to choose your move. Hit Enter to confirm your move"
    screen.blit(pygame.font.SysFont("Arial", 25).render(title1, True, (0, 0, 0)), (50, 50))
    screen.blit(pygame.font.SysFont("Arial", 25).render(title2, True, (0, 0, 0)), (100, 80))
    # Draw a solid black square in the left
    rock = pygame.Rect((50, 200, 100, 100))
    paper = pygame.Rect((350, 200, 100, 100))
    scissors = pygame.Rect((650, 200, 100, 100))

    pygame.draw.rect(screen, BLACK, rock)
    pygame.draw.rect(screen, BLACK, paper)
    pygame.draw.rect(screen, BLACK, scissors)
    screen.blit(pygame.font.SysFont("Arial", 25).render("Rock", True, (0, 0, 0)), (50, 310))
    screen.blit(pygame.font.SysFont("Arial", 25).render("Paper", True, (0, 0, 0)), (350, 310))
    screen.blit(pygame.font.SysFont("Arial", 25).render("Scissors", True, (0, 0, 0)), (650, 310))

    if selected == Move.PAPER:
        pygame.draw.rect(screen, GREEN, paper)
    if selected == Move.ROCK:
        pygame.draw.rect(screen, GREEN, rock)
    if selected == Move.SCISSORS:
        pygame.draw.rect(screen, GREEN, scissors)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
