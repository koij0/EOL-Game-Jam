# CREATED BY: KOI JOHNSON
# START: 10/2/26

## VENV -  commands
# python3.13 -m venv venv313 
# source venv313/bin/activate
# ./venv313/bin/python main.py



# IMPORTS
import pygame
import sys

import random
import math
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
    FALL = 4
    PLAYER_SPEED = 5
    JUMP_FORCE = -20
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
    jumped = False
    coin_count = 1
    coin_collected = False
    order = 0
    is_yes = None

    scene = 0

    x_rope = 350
    y_rope = 100
    angle = 0
    angle_velocity = 0
    rope_points = []
    for i in range(SEGMENTS):
        rope_points.append([x_rope, y_rope + i * SEGMENT_LENGTH, x_rope, y_rope + i * SEGMENT_LENGTH])

    touch_rope = False
    swing = False




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
    def player_move(x_loc, y_loc, grounded, keys, touch_rope, rope_points, swing, jumped):
        if keys[pygame.K_LEFT]:
            x_loc -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            x_loc += PLAYER_SPEED
        if keys[pygame.K_UP] and grounded == True:
            y_loc += JUMP_FORCE
            grounded = False
            jumped = True
        if touch_rope == True:
            if keys[pygame.K_SPACE]: 
                jumped = False
                x_loc = rope_points[-1][0] - 22
                if keys[pygame.K_UP]:
                    swing = False
                    y_loc -= (PLAYER_SPEED / 2)
                    if y_loc < rope_points[0][1] + 5:
                        y_loc = rope_points[0][1] + 5
                elif keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                    swing = True
                    y_loc = rope_points[-1][1] - 22
            else:
                swing = False
        return grounded, x_loc, y_loc, swing, jumped
        
        
    
# PHYSICS
    def physics(velocity, x_loc, y_loc, grounded, jumped, scene, touch_rope):
        # Gravity
        if velocity < 0 or jumped == True: 
            velocity += GRAVITY
          # print("Gravity")
        elif (touch_rope == False or (not keys[pygame.K_SPACE] and touch_rope == True)): 
           # print("FALL")
            velocity += FALL

        y_loc += velocity
        velocity = 0

        # Ground
        if y_loc > GROUND - 50:
            y_loc = GROUND - 50
            grounded = True
            jumped = False
            
            
             

        # Boundaries
        if x_loc < 0: 
            x_loc = SCREEN_WIDTH - 50 # Scene Shifting... 50 is just for my square
            if scene > 0:
                scene -= 1
        elif x_loc > SCREEN_WIDTH:
            x_loc = 0
            if scene < 18:
                scene += 1
        return grounded, x_loc, y_loc, scene, velocity, jumped


# ROPE
    def rope(rope_points, angle, angle_velocity, swing):
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
            if swing == True:

                angle_acceleration = (-GRAVITY / (SEGMENT_LENGTH * SEGMENTS)) * math.sin(angle)
                if keys[pygame.K_LEFT]:
                    angle_acceleration -= 0.01
                if keys[pygame.K_RIGHT]:
                    angle_acceleration += 0.01
                
                angle_velocity = max(-0.1, min(0.1, angle_velocity))
                angle_velocity += angle_acceleration 
                angle_velocity *= AIR 
                angle += angle_velocity 

                for j in range(len(rope_points) - 1):

                    distance = SEGMENT_LENGTH * j 

                    rope_points[j+1][0] = rope_points[0][0] + distance * math.sin(angle)
                    rope_points[j+1][1] = rope_points[0][1] + distance * math.cos(angle)
            else:
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
    def get_scene(scene):
    # 0 - Phone Call / Home 

        if scene == 0:
            scene = 0
        elif scene == 1:
            print("SCENE: ", scene)
        elif scene == 2:
            print("SCENE: ", scene)
        elif scene == 3:
            print("SCENE: ", scene)

        # 1 -   

        elif scene == 4:
            print("SCENE: ", scene)
        elif scene == 5:
            print("SCENE: ", scene)
        elif scene == 6:
            print("SCENE: ", scene)
        elif scene == 7:
            print("SCENE: ", scene)
        # 2 - 

        elif scene == 8:
            print("SCENE: ", scene)
        elif scene == 9:
            print("SCENE: ", scene)
        elif scene == 10:
            print("SCENE: ", scene)
        elif scene == 11:
            print("SCENE: ", scene)

        # 3 - 

        elif scene == 12:
            print("SCENE: ", scene)
        elif scene == 13:
            print("SCENE: ", scene)
        elif scene == 14:
            print("SCENE: ", scene)
        elif scene == 15:
            print("SCENE: ", scene)
        # 4 - Final

        elif scene == 16:
            print("SCENE: ", scene)
        elif scene == 17:
            print("SCENE: ", scene)
        elif scene == 18:
            print("SCENE: ", scene)


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
                        
        # Initial Setup
        # screen.fill(BG_COLOR)

        if is_yes == None:
            screen.blit(bg, (0,0))
            get_scene(scene)
            ground()
            player()
            count(coin_count)
            if not coin_collected: 
                coin = gen_coin()

            rope(rope_points, angle, angle_velocity, swing)

        # MOVE
            keys = pygame.key.get_pressed()
            grounded, x, y, swing, jumped = player_move(x, y, grounded, keys, touch_rope, rope_points, swing, jumped)
            grounded, x, y, scene, velocity, jumped = physics(velocity, x, y, grounded, jumped, scene, touch_rope)
            player()


     # COLLISIONS

            if len(coin) > 0: ## FIX 
                if player().colliderect(coin[0]):
                    coin_count = get_coin(coin_count)
                    coin_collected = True
                    coin.remove(coin[0])

            if scene == 7 or scene == 11 or scene == 15:
                draw_phonebooth()
                if coin_count > 0:        
                    if player().colliderect(draw_phonebooth()):
                        pygame.draw.rect(screen, FLOOR_COLOR, (300, 200, 200, 100)) 
                        draw_text("Use Coin?", 335, 210) 
                        draw_text("Yes", 325, 260) 
                        draw_text("No", 434, 260) 

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

        elif is_yes == True:
            coin_count = use_coin(coin_count)
            phonebooth(order)
        elif is_yes == False:
            x = 640
            is_yes = None



        pygame.display.flip()
        clock.tick(60)
                    
        await asyncio.sleep(0)




asyncio.run(main())  