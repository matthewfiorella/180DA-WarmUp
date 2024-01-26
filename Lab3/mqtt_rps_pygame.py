# Simple pygame program

# Import and initialize the pygame library
import pygame
from enum import IntEnum
import random
import paho.mqtt.client as mqtt
import numpy as np

from pygame.locals import ( K_LEFT, K_RIGHT, K_RETURN, K_ESCAPE, KEYDOWN, QUIT )

game_state = {"me": None, "nick": None}
# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/rps/nn")

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
        
# The default message callback.
# (won’t be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    opponent_choice = str(message.payload.decode())
    oc_decode = "Rock" if opponent_choice == "r" else ("Paper" if opponent_choice == "p" else "Scissors")
    game_state["nick"] = oc_decode
    
# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

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
waiting = False
selected = Move.PAPER
comp_choice = None
while running:

    if waiting: # Waiting for opponent move
        wait_msg = "Waiting for Opponent to Play Move..."
        replay_msg = "Press enter if you want to change your move"
        your_move = "You played " + game_state["me"]
        screen.fill((255, 255, 255))
        screen.blit(pygame.font.SysFont("Arial", 25).render(wait_msg, True, (0, 0, 0)), (50, 50))
        screen.blit(pygame.font.SysFont("Arial", 25).render(replay_msg, True, (0, 0, 0)), (50, 80))
        screen.blit(pygame.font.SysFont("Arial", 25).render(your_move, True, (0, 0, 0)), (50, 110))

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False
                    game_state["me"] = None
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False
        
        if game_state["nick"]:
            waiting = False
            played = True

        pygame.display.flip()
        continue

    elif played: # Opponent Played
        your_move = "You played " + game_state["me"]
        comp_move = "Nick played " + game_state["nick"]
        result = determine_winner(game_state["me"], game_state["nick"])
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
                    waiting = False
                    game_state["me"] = None
                    game_state["nick"] = None
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
                if game_state["nick"]:
                    played = True
                else:
                    waiting = True
                m = "Rock" if selected == Move.ROCK else ("Paper" if selected == Move.PAPER else "Scissors")
                game_state["me"] = m
                client.publish("ece180d/rps/mf", m, qos=1)

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
