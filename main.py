# CREATED BY: KOI JOHNSON
# START: 10/2/26
# LAST UPDATED: 5/5/26

## VENV -  commands
# python3.13 -m venv venv313
# source venv313/bin/activate
# ./venv313/bin/python main.py



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

    GROUND = 450

    # Physics & Mechanics
    GRAVITY = 1
    PLAYER_SPEED = 5
    JUMP_FORCE = -80
    LEVEL_WIDTH = 5000  

    # Rope
    SEGMENTS = 10
    SEGMENT_LENGTH = 30
    AIR = 0.85
    ITERATIONS = 5

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
    is_yes = None

    x_rope = 350
    y_rope = 100
    rope_points = []
    for i in range(SEGMENTS):
        rope_points.append([x_rope, y_rope + i * SEGMENT_LENGTH, x_rope, y_rope + i * SEGMENT_LENGTH])

    touch_rope = False


# SET UP

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EOL")
    clock = pygame.time.Clock()    

# UPLOADS

    # Art
    bg = pygame.image.load("background.png").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT-150))



    # Audio


    # Font
    font = pygame.font.Font('nokiafc22.ttf', 24)


# BACKGROUND
    def ground():
    # Ground
        ground = pygame.Rect((0, GROUND, SCREEN_WIDTH, 150))
        pygame.draw.rect(screen, FLOOR_COLOR, ground)
        return ground


# TEXT

    def draw_text(text, x, y, color=FONT_COLOR):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def wrap(surface, text, sfont, color, x, y, max_width):
        wrapped_lines = textwrap.wrap(text, width=max_width // (sfont.size(' ')[0] // 2))

        for i, line in enumerate(wrapped_lines):
            line_surf = sfont.render(line, True, color)
            surface.blit(line_surf, (x, y + i * sfont.get_height()))


# PLAYER
    def player():
    # Sprite Rendering
        player = pygame.Rect(x, y, 50, 50)
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        return player


# MOVEMENT
    def player_move(x_loc, y_loc, grounded, keys, touch_rope, rope_points):
        if keys[pygame.K_LEFT]:

            x_loc -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            x_loc += PLAYER_SPEED
        if keys[pygame.K_UP] and grounded == True:
            y_loc += JUMP_FORCE
            grounded = False
        if touch_rope == True:
            if keys[pygame.K_SPACE]: 
                x_loc = start_point[0] - 22
                if keys[pygame.K_UP]:
                    y_loc -= (PLAYER_SPEED / 2)
                    if y_loc < rope_points[0][1] + 5:
                        y_loc = rope_points[0][1] + 5
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


# ROPE
    def rope(rope_points):
        # Update points
        for i in rope_points[1:]:
            vx = (i[0] - i[2]) * AIR
            vy = (i[1] - i[3]) * AIR
            i[2] = i[0]
            i[3] = i[1]
            i[0] += vx
            i[1] += vy + GRAVITY

        # Constraints
        for i in range(ITERATIONS):
            for j in range(len(rope_points) - 1):
                p1 = rope_points[j]
                p2 = rope_points[j+1]

                dx = p2[0] - p1[0]
                dy = p2[1] -p1[1]
                distance = (dx**2 +  dy**2)**(1/2)

                difference = SEGMENT_LENGTH - distance
                offset_x = dx * (difference / distance / 2.0)
                offset_y = dy * (difference / distance / 2.0)

                if j != 0:
                    p1[0] -= offset_x
                    p1[1] -= offset_y
                p2[0] += offset_x
                p2[1] += offset_y

        # Draw
        for i in range(len(rope_points) - 1):
            pygame.draw.line(screen, (255, 223, 0), (rope_points[i][0], rope_points[i][1]), (rope_points[i+1][0], rope_points[i+1][1]), 5)
        for i in rope_points:
            pygame.draw.circle(screen, (229, 184, 11), (int(i[0]), int(i[1])), 4)
        pygame.draw.circle(screen, (229, 185, 11), (int(rope_points[0][0]), int(rope_points[0][1])), 10)




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
    def count(count):
        draw_text(f"Coins: {count}", 25, 25)


# PHONE BOOTH 

    # Sprite Rendering
    def draw_phonebooth():
        phonebooth = pygame.Rect(700, GROUND - 100, 75, 100)
        pygame.draw.rect(screen, PLAYER_COLOR, phonebooth)
        return phonebooth




# LEVEL / SCENES

    # 0 - Phone Call / Home 

    # 1 -   

    # 2 - 

    # 3 - 

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
            print("You've reached the end of the line...")
    # Ending 1 

    # Ending 2




# MAIN GAME LOOP
    while True:

        # Initial Setup
        # screen.fill(BG_COLOR)
        screen.blit(bg, (0,0))
        ground()
        player()
        count(coin_count)
        if not coin_collected: 
            coin = gen_coin()

        draw_phonebooth()


    # Check Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit() 

            if event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos = event.pos
                # ROPE
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rope_points[0][0] = mouse_x
                rope_points[0][1] = mouse_y
                rope_points[0][2] = mouse_x
                rope_points[0][3] = mouse_y
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    is_yes = True
                if event.key == pygame.K_n:
                    is_yes = False
                


        rope(rope_points)
                


    # MOVE
        keys = pygame.key.get_pressed()
        grounded, x, y = player_move(x, y, grounded, keys, touch_rope, rope_points)
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
                pygame.draw.rect(screen, FLOOR_COLOR, (300, 200, 200, 100)) 
                draw_text("Use Coin?", 335, 210) 
                draw_text("Yes", 325, 260) 
                draw_text("No", 434, 260) 

                if is_yes == True:
                    coin_count = use_coin(coin_count)
                    phonebooth(order)
                    is_yes = None
                elif is_yes == False:
                    x = 640
                    is_yes = None

        # Rope hits ground/platforms/etc
        for i in range(len(rope_points)):
            if ground().collidepoint(rope_points[i][0], rope_points[i][1]):
                rope_points[i][1] = ground().top

        # Grab Rope
        for i in range(len(rope_points) - 1):
            start_point = (rope_points[i][0], rope_points[i][1])
            end_point = (rope_points[i+1][0], rope_points[i+1][1])

            if player().clipline(start_point, end_point):
                touch_rope = True
                break
            else:
                touch_rope = False

        
        
            

            




        pygame.display.flip()
        clock.tick(60)
                    
        await asyncio.sleep(0)




asyncio.run(main())  