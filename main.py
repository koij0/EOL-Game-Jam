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
    SCREEN_WIDTH = 600  # SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800 # SCREEN_HEIGHT = 600

    GROUND = 650

    # Physics & Mechanics
    GRAVITY = 1
    FALL = 3
    PLAYER_SPEED = 5
    JUMP_FORCE = -25
    ROPE_BOOST = 8


    # Rope
    SEGMENTS = 5
    SEGMENT_LENGTH = 30
    AIR = 0.93
    ITERATIONS = 5
    DAMPING = 0.97

    # Colors 
    BG_COLOR = (128, 128, 128) # Grey
    PLAYER_COLOR = (82, 14, 125) # Purple
    FLOOR_COLOR = (0, 0, 0) # Black
    COIN_COLOR = (255, 255, 255) # White
    FONT_COLOR = (0, 143, 145) # Teal



# INITIALIZATION

    x = 250 # x = 300
    y = 50 # y = 350
    y_velocity = 0
    x_velocity = 0
    grounded = False
    jumped = False
    coin_count = 1
    coin_collected = False
    order = 0
    coin_yes = None
    phone_answer = None

    lives = 9
    life = False

    scene = 0
    time = 5

    x_rope = 0
    y_rope = 0
    angle = 0
    angle_velocity = 0
    rope_points = []
    for i in range(SEGMENTS):
        rope_points.append([x_rope, y_rope + i * SEGMENT_LENGTH, x_rope, y_rope + i * SEGMENT_LENGTH])


    no_move = True
    swing = False
    throw_rope = False

    buttons = []
    for i in range(3):
        for j in range(3):
            buttons.append(pygame.Rect((j * 125) + 125, (i * 125) + 125 , 100, 100))
    buttons.append(pygame.Rect(250, 500, 100, 100))

    mouse_pos = (0, 0)

    phone_screen = None
    call = None
    flash_timer = None
    sequence = [7, 9, 9, 1, 6, 2, 7, 1, 4, 4]
    s = 0
    seq_played = False
    
    
    

# FILES
    phone_script = []
    with open('phone_script.txt', 'r') as phone_file:
                for line in phone_file:
                    line = line.strip()
                    phone_script.append(line)



# SET UP

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EOL")
    clock = pygame.time.Clock()    

# UPLOADS

    # Background

    BG = pygame.image.load("background.png").convert_alpha()
    BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Player
    PLAYER_IDLE = pygame.image.load("sprites/idle.png").convert_alpha()
    PLAYER_IDLE = pygame.transform.scale(PLAYER_IDLE, (100, 120))
    PLAYER_WALK1 = pygame.image.load("sprites/walk1.png").convert_alpha()
    PLAYER_WALK1 = pygame.transform.scale(PLAYER_WALK1, (100, 120))
    PLAYER_WALK2 = pygame.image.load("sprites/walk2.png").convert_alpha()
    PLAYER_WALK2 = pygame.transform.scale(PLAYER_WALK2, (100, 120))
    PLAYER_JUMP = pygame.image.load("sprites/jump.png").convert_alpha()
    PLAYER_JUMP = pygame.transform.scale(PLAYER_JUMP, (100, 120))




    # Audio


    # Font
    font = pygame.font.Font('nokiafc22.ttf', 24)


# BACKGROUND
    def ground():
    # Ground
        ground = pygame.Rect((0, GROUND, SCREEN_WIDTH, 150))
        pygame.draw.rect(screen, FLOOR_COLOR, ground)
        return ground

    def walls():
        wall1 = pygame.Rect((0, 0, 10, SCREEN_HEIGHT))
        wall2 = pygame.Rect((SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT))
        pygame.draw.rect(screen, FLOOR_COLOR, wall1)
        pygame.draw.rect(screen, FLOOR_COLOR, wall2)
        return wall1, wall2


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
    def player(jumped):
    # Sprite Rendering
        if jumped == True:
            player = PLAYER_JUMP.get_rect(topleft = (x, y)) 
            screen.blit(PLAYER_JUMP, player)
            jumped = False
        else:
            player = PLAYER_IDLE.get_rect(topleft = (x, y)) 
            screen.blit(PLAYER_IDLE, player)
        return player, jumped


# MOVEMENT
    def player_move(x_loc, y_loc, grounded, keys, rope_points, swing, jumped, dt, time, throw_rope, no_move):

        if grounded == True:
            if keys[pygame.K_LEFT]:
                x_loc -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                x_loc += PLAYER_SPEED
            if keys[pygame.K_UP]:
                y_loc += JUMP_FORCE
                grounded = False
                jumped = True

        if throw_rope == True: 
            time -= dt
            jumped = False

            if time <= 0:
                y_loc = rope_points[-1][1] + 10
                swing = False
                throw_rope = False
                no_move = True
                time = 0 

            else:
                x_loc = rope_points[-1][0] - 22

                if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                    swing = True
                    y_loc = rope_points[-1][1] - 22

                else:
                    swing = False

                if swing == False: 
                    if keys[pygame.K_UP]:
                        swing = False
                        no_move = False
                        y_loc -= (PLAYER_SPEED / 2)

                        if y_loc < rope_points[0][1] + 5:
                            y_loc = rope_points[0][1] + 5

                    elif keys[pygame.K_DOWN]:
                        swing = False
                        y_loc += (PLAYER_SPEED / 2) 

                        if y_loc > rope_points[-1][1] - 5:
                            throw_rope = False
                    else:
                        if no_move == True:
                            y_loc = rope_points[-1][1] - 22
                            swing = False

        else:
            swing = False

        return grounded, x_loc, y_loc, swing, jumped, time, throw_rope, no_move
        
        
    
# PHYSICS
    def physics(x_velocity, y_velocity, x_loc, y_loc, grounded, jumped, scene, throw_rope):
        
        # Gravity
        
        if throw_rope == False:
            if jumped == True:
                y_velocity += GRAVITY
                x_velocity *= AIR

            else:   
                y_velocity = FALL
                x_velocity = 0

            y_loc += y_velocity
            x_loc += x_velocity

        

        # Reset Jump
        if grounded == True:
            y_velocity = 0
            jumped = False

        # Boundaries

        # Wall
        if x_loc < 0:
            x_loc = 0
        elif x_loc > SCREEN_WIDTH - 100:
            x_loc = SCREEN_WIDTH - 100 

        # Ground
        if scene == 3 or scene == 7 or scene == 11 or scene == 15 or scene == 18:
            if y_loc > GROUND - 110:
                y_loc = GROUND - 110
                grounded = True
                jumped = False
            
        # Falling        
        if y_loc > SCREEN_HEIGHT:  
            y_loc = 0 
            if scene < 18:
                scene += 1
        return grounded, x_loc, y_loc, scene, x_velocity, y_velocity, jumped


# ROPE
    def rope(rope_points, angle, angle_velocity, swing, x_velocity, y_velocity, keys):

        anchor_x = rope_points[0][0]
        anchor_y = rope_points[0][1]

        if swing == True:
            angle_acceleration = (- GRAVITY / (SEGMENT_LENGTH * (len(rope_points)-1))) * math.sin(angle)
            if keys[pygame.K_LEFT]:
                angle_acceleration -= 0.005
            if keys[pygame.K_RIGHT]:
                angle_acceleration += 0.005
                
            
            angle_velocity += angle_acceleration 
            angle_velocity *= (AIR * DAMPING) 

            angle_velocity = max(-0.12, min(0.12, angle_velocity))
           
            angle += angle_velocity         

            # Constraints
            for i in range(1, len(rope_points)):
                distance = SEGMENT_LENGTH * i

                rope_points[i][0] = (anchor_x + distance * math.sin(angle))
                rope_points[i][1] = (anchor_y + distance * math.cos(angle))

                rope_points[i][2] = rope_points[i][0]
                rope_points[i][3] = rope_points[i][1]

        else:
            for i in range(1, len(rope_points)):
                point = rope_points[i]

                vx = (point[0] - point[2]) * 0.85
                vy = (point[1] - point[3]) * 0.85

                old_x = point[0]
                old_y = point[1]

                point[0] += vx
                point[1] += vy + GRAVITY

                point[2] = old_x
                point[3] = old_y

            for _ in range(ITERATIONS):
                rope_points[0][0] = anchor_x
                rope_points[0][1] = anchor_y

                for i in range(1, len(rope_points)):
                    p1 = rope_points[i - 1]
                    p2 = rope_points[i]

                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]

                    distance = math.hypot(dx, dy)

                    if distance < 0.001:
                        continue

                    difference = (distance - SEGMENT_LENGTH) / distance

                    offset_x = dx * difference
                    offset_y = dy * difference

                    if i > 1:
                        p1[0] += offset_x * 0.5
                        p1[1] += offset_y * 0.5

                    p2[0] -= offset_x * 0.5
                    p2[1] -= offset_y * 0.5

        for i in range(len(rope_points) - 1):
            p1 = (int(rope_points[i][0]), int(rope_points[i][1]))
            p2 = (int(rope_points[i + 1][0]),int(rope_points[i + 1][1]))


        # Draw

            # Rope
            pygame.draw.line(screen, (255, 223, 0), p1, p2, 4)

        for i, point in enumerate(rope_points):
            pygame.draw.circle(screen, (229, 184, 11), (int(point[0]), int(point[1])), 4)

        # Ball
        pygame.draw.circle(screen, (229, 185, 11), (int(anchor_x), int(anchor_y)), 7)

        return angle, angle_velocity, x_velocity, y_velocity

        

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

# LIVES
    # Generate
    def heart():
        heart = [pygame.Rect(400, 400, 25, 25)] 
        pygame.draw.rect(screen, (255, 192, 203), heart[0])
        return heart
    
    # Lose
    def lose_life(lives):
        lives -= 1
        return lives

# PHONE BOOTH 

    # Sprite Rendering
    def draw_phonebooth():
        phonebooth = pygame.Rect(500, GROUND - 100, 75, 100)
        pygame.draw.rect(screen, PLAYER_COLOR, phonebooth)
        return phonebooth

    # Phone Screen
    def phone_buttons(buttons):
        screen.fill((0, 0, 0))
        for button in buttons:
            pygame.draw.rect(screen, (0, 0, 255), button)

    # Phone sequence
    def phone_sequence(sequence, current_time):
        flash_timer = {
            'sequence': sequence,
            'step': 0,
            'color': (0, 225, 0),
            'start_time': current_time,
            'duration': 500
            }

        return flash_timer

    # Dial
    def dial(buttons, sequence, mouse_pos, s, flash_timer):
        current_time = pygame.time.get_ticks()
    
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                if s < len(sequence) and i == sequence[s]:
                    s += 1
                    flash_timer = {
                        'index': i,
                        'color': (0, 255, 0),
                        'start_time': current_time,
                        'duration': 300
                    }

                    if s >= len(sequence):
                        return s, flash_timer, True

                    return s, flash_timer, None

                flash_timer = {
                    'index': i,
                    'color': (255, 0, 0),
                    'start_time': current_time,
                    'duration': 1000,
                    'wrong': True
                }

                return s, flash_timer, False    
                    
        return s, flash_timer, None

    # Flash 
    def flash(flash_timer, current_time, buttons):
        if not flash_timer:
            return None

        elapsed = current_time - flash_timer['start_time']
    
        if 'index' in flash_timer and 'color' in flash_timer:
            if elapsed >= flash_timer['duration']:
                return None

            index = flash_timer['index']
            color = flash_timer['color']

            for i, button in enumerate(buttons):
                if i == index:
                    pygame.draw.rect(screen, color, button)
                else:
                    pygame.draw.rect(screen, (0, 0, 255), button)

            return flash_timer


        if 'sequence' in flash_timer:
            if elapsed >= flash_timer['duration']:
                flash_timer['step'] += 1
                flash_timer['start_time'] = current_time

                if flash_timer['step'] >= len(flash_timer['sequence']) * 2:
                    return None

            step = flash_timer['step']
            index = flash_timer['sequence'][step // 2]

            if step % 2 == 0:
                color = (0, 225, 0)  
            else:
                color = (0, 0, 255)  

            for i, button in enumerate(buttons):
                if i == index:
                    pygame.draw.rect(screen, color, button)
                else:
                    pygame.draw.rect(screen, (0, 0, 255), button)

            return flash_timer

        return None


# LEVEL / SCENES
    def get_scene(scene):
        barriers = []
        platforms = []
    # 0 - Phone Call / Home 

        if scene == 0:
            barriers.append(pygame.Rect(0, 500, 200, 10))
            barriers.append(pygame.Rect(400, 500, 200, 10))
            platforms.append(pygame.Rect(250, 150, 100, 10))

            for barrier in barriers:
                pygame.draw.rect(screen, (255, 0, 0), barrier)

            for platform in platforms:
                pygame.draw.rect(screen, (0, 255, 0), platform)
        elif scene == 1:
            barriers.append(pygame.Rect(200, 300, 200, 10))
            platforms.append(pygame.Rect(250, 600, 100, 10))
            
            for barrier in barriers:
                pygame.draw.rect(screen, (255, 0, 0), barrier)
            
            for platform in platforms:
                pygame.draw.rect(screen, (0, 255, 0), platform)

        elif scene == 2:
            barriers.append(pygame.Rect(200, 600, 200, 10))
            barriers.append(pygame.Rect(400, 600, 200, 10))
            barriers.append(pygame.Rect(0, 200, 200, 10))
            barriers.append(pygame.Rect(200, 200, 200, 10))
            
            for barrier in barriers:
                pygame.draw.rect(screen, (255, 0, 0), barrier)
            
            for platform in platforms:
                pygame.draw.rect(screen, (0, 255, 0), platform)
        elif scene == 3:
            scene = 3

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

        return barriers, platforms


# PHONE BOOTH CUT-SCENES

    def phone_call(order, phone_script, phone_answer):
        screen.fill((0, 0, 0))
    # Intro 
        if order == 0: 
            draw_text(phone_script[0], 100, 200)
            draw_text(phone_script[1], 100, 300)
            if phone_answer == True:
                order = 1
                return order, phone_answer
    # 1 - “Have you had thoughts about how you might do this?” 
        elif order == 1: 
            draw_text(phone_script[2], 130, 200)
            draw_text(phone_script[3], 80, 250)
            draw_text("Yes", 225, 600) 
            draw_text("No", 334, 600) 
            if phone_answer == True:
                order = 2
                return order, phone_answer
    # 2 - “Are you safe?”
        elif order == 2: 
            draw_text(phone_script[4], 200, 200)
            draw_text("Yes", 225, 600) 
            draw_text("No", 334, 600) 
            if phone_answer == True:
                order = 3
                return order, phone_answer
    # 3 - “Do you need help?”
        elif order == 3: 
            draw_text(phone_script[5], 180, 200)
            draw_text("Yes", 225, 600) 
            draw_text("No", 334, 600) 
            if phone_answer == True:
                order = 4
                return order, phone_answer
    # 4 - You’ve reached the end of the line…
        elif order == 4: 
            draw_text(phone_script[6], 100, 200)
            draw_text(phone_script[7], 100, 250)
    # Ending 1 

    # Ending 2
        return order, False
        




# MAIN GAME LOOP
    while True:
        dt = clock.tick(60) / 1000

        rope_points[0][0] = x_rope
        rope_points[0][1] = y_rope
        rope_points[0][2] = x_rope
        rope_points[0][3] = y_rope
                

# Check Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() 
                    sys.exit()   

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  
                if seq_played == True:   
                    s, flash_timer, call = dial(buttons, sequence, mouse_pos, s, flash_timer)

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if throw_rope == True and swing == True:
                        rope_vx = rope_points[-1][0] - rope_points[-2][0]
                        rope_vy = rope_points[-1][1] - rope_points[-2][1]

                        throw_rope = False
                        swing = False
                        no_move = True

                        x_velocity = max(-3, min(3, rope_vx * 0.5))
                        y_velocity = -150 + rope_vy * 0.8

                        jumped = True
                        grounded = False 

                    elif throw_rope == False:
                        x_rope = x + 25
                        y_rope = y
                        throw_rope = True
                        time = 5
                        
                if coin_yes == None:
                    if event.key == pygame.K_y:
                        coin_yes = True
                    if event.key == pygame.K_n:
                        coin_yes = False

                elif coin_yes == True:
                    if event.key == pygame.K_y or event.key == pygame.K_n:
                        phone_answer = True
                    
            
                        
        # Initial Setup
        # screen.fill(BG_COLOR)

        if life == True:
            lives = lose_life(lives)
            life = False
        
        if coin_yes == None:
            screen.blit(BG, (0,0))
            barriers, platforms = get_scene(scene)
            walls()

            if scene == 3 or scene == 7 or scene == 11 or scene == 15 or scene == 18:
                ground()
                # Rope hits ground/platforms/etc
                for i in range(len(rope_points)):
                    if ground().collidepoint(rope_points[i][0], rope_points[i][1]):
                        rope_points[i][1] = ground().top

            player(jumped)
            count(coin_count)
            if not coin_collected: 
                coin = gen_coin()

        
            keys = pygame.key.get_pressed()
            # print("LIVES: ", lives)
    

        # ROPE
            if throw_rope == True:
                angle, angle_velocity, x_velocity, y_velocity = rope(rope_points, angle, angle_velocity, swing, x_velocity, y_velocity, keys)
        
        # MOVE        
            grounded, x, y, swing, jumped, time, throw_rope, no_move = player_move(x, y, grounded, keys, rope_points, swing, jumped, dt, time, throw_rope, no_move)
            grounded, x, y, scene, x_velocity, y_velocity, jumped = physics(x_velocity, y_velocity, x, y, grounded, jumped, scene, throw_rope)
            character, jumped = player(jumped)


     # COLLISIONS

            if len(coin) > 0: ## FIX 
                if character.colliderect(coin[0]):
                    coin_count = get_coin(coin_count)
                    coin_collected = True
                    coin.remove(coin[0])

            if scene == 3 or scene == 7 or scene == 11 or scene == 15:
                draw_phonebooth()
                if coin_count > 0:        
                    if character.colliderect(draw_phonebooth()):
                        pygame.draw.rect(screen, FLOOR_COLOR, (200, 400, 200, 100))  
                        draw_text("Use Coin?", 235, 410) 
                        draw_text("Yes", 225, 460) 
                        draw_text("No", 334, 460) 


        # Barriers
            if life == False:   
                for barrier in barriers:
                    if character.colliderect(barrier):
                        life = True                      

        # Platforms
            for platform in platforms:
                if character.colliderect(platform):
                    grounded = True
                    y = platform.y - 110
                else:
                    grounded = False

                           

        elif coin_yes == True:

            if phone_screen == None:
                coin_count = use_coin(coin_count)
                phone_screen = True

            elif phone_screen == True:
                phone_buttons(buttons)
                current_time = pygame.time.get_ticks()

                if seq_played == False and flash_timer == None:
                    flash_timer = phone_sequence(sequence, current_time)
                    seq_played = True
                    

                if flash_timer: 
                    flash_timer = flash(flash_timer, current_time, buttons)

                    if flash_timer and flash_timer.get('wrong', False):
                        if current_time - flash_timer['start_time'] >= flash_timer['duration']:
                            flash_timer = None
                            s = 0
                            call = None
                            seq_played = False
                    
            
            if seq_played == True:
                if call == True:
                    order, phone_answer = phone_call(order, phone_script, phone_answer) 
                    if phone_answer == True:
                        call = None
                        s = 0
                        scene += 1
                        seq_played = False
                        coin_yes = False
                        phone_answer = None
                elif call == False:
                    call = None
                    s = 0
                    seq_played = False
            

        elif coin_yes == False:
            x = 390
            coin_yes = None


        
        pygame.display.flip()
        
                    
        await asyncio.sleep(0)




asyncio.run(main())  