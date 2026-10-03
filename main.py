# CREATED BY: KOI JOHNSON
# START: 10/2/26
# LAST UPDATED: 5/5/26

## VENV -  commands
# python3 -m venv venv
# source venv/bin/activate
# ./path/to/venv/bin/python main.py



# IMPORTS
import pygame
import sys
import random
import textwrap
import os

# For WebAssembly
import asyncio

async def main ():

# CONFIGURATIONS

    # Screen configurations
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    GROUND = 400

    # Physics & Mechanics
    GRAVITY = 1
    PLAYER_SPEED = 5
    JUMP_FORCE = -80
    LEVEL_WIDTH = 5000  

    # Colors 
    BG_COLOR = (128, 128, 128) # Grey
    PLAYER_COLOR = (82, 14, 125) # Purple
    FLOOR_COLOR = (0, 0, 0) # Black




# INITIALIZATION

    x = 300
    y = 350
    velocity = 0
    grounded = True


# UPLOADS

    # Art


    # Audio


    # Font

# SET UP

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EOL")
    clock = pygame.time.Clock()


# BACKGROUND
    def background():
    # Ground
        pygame.draw.rect(screen, FLOOR_COLOR, (0, GROUND, SCREEN_WIDTH, 200))


# PLAYER
    def player():
    # Sprite Rendering
            pygame.draw.rect(screen, PLAYER_COLOR, (x, y, 50, 50))


# MOVEMENT
    def player_move(x_loc, y_loc, grounded, keys):
        if keys[pygame.K_LEFT]:
            x_loc -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            x_loc += PLAYER_SPEED
        if keys[pygame.K_UP] and grounded == True:
            y_loc += JUMP_FORCE
            grounded = False
        return grounded, x_loc, y_loc
        
        
    
# PHYSICS
    def physics(velocity, x_loc, y_loc, grounded):
        # Gravity

        velocity += GRAVITY
        y_loc += velocity
        velocity = 0  

        # Ground
        if y_loc > GROUND - 50:
            y_loc = GROUND - 50
            grounded = True
                   

        # Boundaries
        if x_loc < 0: 
            x_loc = SCREEN_WIDTH - 50 # Scene Shifting... 50 is just for my square
            # SCENE -= 1
        elif x_loc > SCREEN_WIDTH:
            x_loc = 0
            # SCENE += 1
        return grounded, x_loc, y_loc


# COLLECTION

    # Coins

    # Tool 



# LEVEL / SCENES

    # 0 - Phone Call / Home 

    # 1 - Maneuver  

    # 2 - Enemy

    # 3 - Maze

    # 4 - Final


# PHONE BOOTH CUT-SCENES

    # Intro 
    
    # 1 - “Have you had thoughts about how you might do this?” 

    # 2 - “Are you safe?”

    # 3 - “When did you realize you couldn't stay afloat anymore?”

    # 4 - You’ve reached the end of the line…

    # Ending 1 

    # Ending 2




# MAIN GAME LOOP
    while True:
        screen.fill(BG_COLOR)
        background()
        player()


        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)


    # Check Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit() 


    # MOVE
        keys = pygame.key.get_pressed()
        grounded, x, y = player_move(x, y, grounded, keys)
        grounded, x, y = physics(velocity, x, y, grounded)
        player()

                    




asyncio.run(main())  