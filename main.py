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
    COIN_COLOR = (255, 255, 255) # White
    FONT_COLOR = (0, 143, 145) # Teal




# INITIALIZATION

    x = 300
    y = 350
    velocity = 0
    grounded = True
    coin_count = 1
    coin_collected = False
    order = 0

# SET UP

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EOL")
    clock = pygame.time.Clock()    

# UPLOADS

    # Art


    # Audio


    # Font
    # font = pygame.font.Font('nokiafc22.ttf', 24)


# BACKGROUND
    def background():
    # Ground
        pygame.draw.rect(screen, FLOOR_COLOR, (0, GROUND, SCREEN_WIDTH, 200))


# TEXT

   # def draw_text(text, x, y, color=FONT_COLOR):
         #   img = font.render(text, True, color)
         #   screen.blit(img, (x, y))

   # def wrap(surface, text, sfont, color, x, y, max_width):
                # Split text into lines that fit within max_width
        #        wrapped_lines = textwrap.wrap(text, width=max_width // (sfont.size(' ')[0] // 2))

        #        for i, line in enumerate(wrapped_lines):
        #            line_surf = sfont.render(line, True, color)
          #          surface.blit(line_surf, (x, y + i * sfont.get_height()))


# PLAYER
    def player():
    # Sprite Rendering
        player = pygame.Rect(x, y, 50, 50)
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        return player


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


# COINS

    # Generate
    def gen_coin():
        coin = [pygame.Rect(400, GROUND - 50, 25, 25)] # FIX WHEN GET SPRITE COINS
        pygame.draw.rect(screen, COIN_COLOR, coin[0])
        return coin
    

    # Collect
    def get_coin(coin):
        coin += 1
        return coin

    # Use
    def use_coin(coin):
        coin -= 1
        return coin

    # Display Count
   # def count(count):
       # draw_text(f"Coins: {count}", 25, 25)


# PHONE BOOTH 

    # Sprite Rendering
    def draw_phonebooth():
        phonebooth = pygame.Rect(700, GROUND - 100, 75, 100)
        pygame.draw.rect(screen, PLAYER_COLOR, phonebooth)
        return phonebooth



# LEVEL / SCENES

    # 0 - Phone Call / Home 

    # 1 - Maneuver  

    # 2 - Enemy

    # 3 - Maze

    # 4 - Final


# PHONE BOOTH CUT-SCENES

    def phonebooth(order):
        screen.fill((0, 0, 0))
    # Intro 
        if order == 0: 
            print("INTRO")
    # 1 - “Have you had thoughts about how you might do this?” 
        elif order == 1: 
            print("Have you had thoughts about how you might do this?")
    # 2 - “Are you safe?”
        elif order == 2: 
            print("Are you safe?")
    # 3 - “Do you need help?”
        elif order == 3: 
            print("Do you need help?")
    # 4 - You’ve reached the end of the line…
        elif order == 4: 
            print("You’ve reached the end of the line...")
    # Ending 1 

    # Ending 2




# MAIN GAME LOOP
    while True:

        # Initial Setup
        screen.fill(BG_COLOR)
        background()
        player()
     #   count(coin_count)
        if not coin_collected: 
            coin = gen_coin()

        draw_phonebooth()

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


    # COLLISIONS

        if len(coin) > 0: ## FIX 
            if player().colliderect(coin[0]):
                coin_count = get_coin(coin_count)
                coin_collected = True
                print(f"COIN: ", coin_count)
                coin.remove(coin[0])

        if coin_count > 0:        
            if player().colliderect(draw_phonebooth()):
                insert = input("Use Coin? Y/N: ")
                if insert == "Y":
                    coin_count = use_coin(coin_count)
                    print(f"COIN: ", coin_count)
                    phonebooth(order)
                else:
                    x -= 10

            
                    




asyncio.run(main())  