# CREATED BY: KOI JOHNSON
# START: 10/2/26

## VENV -  commands
# python3.13 -m venv venv313 
# source venv313/bin/activate
# ./venv313/bin/python main.py



# IMPORTS
import pygame
import sys
from shapely.geometry import Polygon


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
    JUMP_FORCE = -30


    # Rope
    SEGMENTS = 6
    SEGMENT_LENGTH = 30
    AIR = 0.93
    ITERATIONS = 5
    DAMPING = 0.97

    # Colors 
    GREY = (128, 128, 128) # Grey
    PLAYER_COLOR = (82, 14, 125) # Purple
    BLACK = (0, 0, 0) # Black
    WHITE = (255, 255, 255) # White
    TEAL = (0, 143, 145) # Teal



# INITIALIZATION

    x = 20 # x = 300
    y = 100 # y = 350
    y_velocity = 0
    x_velocity = 0

    grounded = False
    jumped = False
    walking_l = False
    walking_r = False

    frame = 0

    tut_track = []
    tut_screen = True
    idx = 0

    coin_count = 1
    coin_collected = False
    heart_collected = False
    order = 0
    coin_yes = None
    phone_answer = None

    lives = 9
    life = False
    respawn = False

    scene = 1
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
    touch_rope = False
    touch_x = None
    touch_y = None

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

    blink = 0
    is_visible = False

    phone_ringing = False

    
    

# FILES
    # Phone Story
    phone_script = []
    with open('phone_script.txt', 'r') as phone_file:
        for line in phone_file:
            line = line.strip()
            phone_script.append(line)

    # Tutorial
    tut_text = []
    with open('tutorial.txt', 'r') as tut_file:
        for line in tut_file:
            line = line.strip()
            tut_text.append(line)
    for i in range(len(tut_text)):
        tut_track.append(False)



# SET UP

    pygame.mixer.pre_init(44100, -16, 2, 2048)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EOL")
    clock = pygame.time.Clock()    

    animate_time = pygame.time.get_ticks()


# UPLOADS

    # Background

    BG = pygame.image.load("background.png").convert_alpha()
    BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Player
    PLAYER_IDLE = pygame.image.load("sprites/idle.png").convert_alpha()
    PLAYER_IDLE = pygame.transform.scale(PLAYER_IDLE, (80, 120))
    PLAYER_WALK1 = pygame.image.load("sprites/walk1.png").convert_alpha()
    PLAYER_WALK1 = pygame.transform.scale(PLAYER_WALK1, (90, 120))
    PLAYER_WALK2 = pygame.image.load("sprites/walk2.png").convert_alpha()
    PLAYER_WALK2 = pygame.transform.scale(PLAYER_WALK2, (100, 120))

    PLAYER_WALK = [PLAYER_WALK1, PLAYER_WALK2]
    
    PLAYER_JUMP = pygame.image.load("sprites/jump.png").convert_alpha()
    PLAYER_JUMP = pygame.transform.scale(PLAYER_JUMP, (110, 130))

    PLAYER_CLIMB = pygame.image.load("sprites/climb.png").convert_alpha()
    PLAYER_CLIMB = pygame.transform.scale(PLAYER_CLIMB, (70, 140)) 

    # Heart
    HEART = pygame.image.load("sprites/heart.png").convert_alpha()
    HEART = pygame.transform.scale(HEART, (30, 30))


    # Coin
    COIN = pygame.image.load("sprites/coin.png").convert_alpha()
    COIN = pygame.transform.scale(COIN, (50, 50))


    # Phone
    PHONE = pygame.image.load("sprites/phone.png").convert_alpha()
    PHONE = pygame.transform.scale(PHONE, (100, 150))

    # Wires
    WIRE1 = pygame.image.load("sprites/wire1.png").convert_alpha()
    WIRE2 = pygame.image.load("sprites/wire2.png").convert_alpha()

    # Buttons

    # Red
    RED_BUTTONS = []
    for i in range(10):
        RED_BUTTON = pygame.image.load(f"sprites/red/r{i+1}.png").convert_alpha()
        RED_BUTTON = pygame.transform.scale(RED_BUTTON, (100, 100))
        RED_BUTTONS.append(RED_BUTTON)

    # Blue
    BLUE_BUTTONS = []
    for i in range(10):
        BLUE_BUTTON = pygame.image.load(f"sprites/blue/b{i+1}.png").convert_alpha()
        BLUE_BUTTON = pygame.transform.scale(BLUE_BUTTON, (100, 100))
        BLUE_BUTTONS.append(BLUE_BUTTON)

    # Green
    GREEN_BUTTONS = []
    for i in range(10):
        GREEN_BUTTON = pygame.image.load(f"sprites/green/g{i+1}.png").convert_alpha()
        GREEN_BUTTON = pygame.transform.scale(GREEN_BUTTON, (100, 100))
        GREEN_BUTTONS.append(GREEN_BUTTON)

    # Audio

    RINGTONE = pygame.mixer.Sound("sfx/ringtone.wav")

    SFX_WALK1 = pygame.mixer.Sound("sfx/walk1.wav")
    SFX_WALK2 = pygame.mixer.Sound("sfx/walk2.wav")
    SFX_WALK = [SFX_WALK1, SFX_WALK2]
  # SFX_JUMP = pygame.mixer.Sound("sfx/jump.wav")

    SFX_THROW = pygame.mixer.Sound("sfx/throw.wav")


    SFX_COIN = pygame.mixer.Sound("sfx/coin.wav")
    SFX_USE_COIN = pygame.mixer.Sound("sfx/use_coin.wav")
    SFX_BEEP = pygame.mixer.Sound("sfx/beep.wav")
    SFX_CLICK = pygame.mixer.Sound("sfx/click.wav")


    



    # Font
    font = pygame.font.Font('nokiafc22.ttf', 24)


# BACKGROUND
    def ground():
    # Ground
        ground = pygame.Rect((0, GROUND, SCREEN_WIDTH, 150))
        return ground

    def walls():
        wall1 = pygame.Rect((0, 0, 10, SCREEN_HEIGHT))
        wall2 = pygame.Rect((SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT))
        pygame.draw.rect(screen, BLACK, wall1)
        pygame.draw.rect(screen, BLACK, wall2)
        return wall1, wall2

   


# TEXT

    def draw_text(text, x, y, color=TEAL):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def wrap(surface, text, sfont, color, x, y, max_width):
        wrapped_lines = textwrap.wrap(text, width=max_width // (sfont.size(' ')[0] // 2))

        for i, line in enumerate(wrapped_lines):
            line_surf = sfont.render(line, True, color)
            surface.blit(line_surf, (x, y + i * sfont.get_height()))

# TUTORIAL
    def tutorial(tut_text, idx, tut_track):
        pygame.draw.rect(screen, BLACK, (150, 300, 300, 170))  
        wrap(screen, tut_text[idx], font, TEAL, 160, 320, 75)
        draw_text("RETURN", 250, 430) 
        tut_track[idx] = True


# PLAYER
    def player(jumped, grounded, walking_l, walking_r, animate_time, touch_rope, frame, x, y):
        now = pygame.time.get_ticks()
    # Sprite Rendering

        if touch_rope == True and grounded == False:
            character = PLAYER_CLIMB.get_rect(topleft = (x, y)) 
            screen.blit(PLAYER_CLIMB, character)
        elif jumped == True: # or grounded == False:
          #  SFX_JUMP.play()
            character = PLAYER_JUMP.get_rect(topleft = (x, y)) 
            screen.blit(PLAYER_JUMP, character)
        elif walking_l == True or walking_r == True:
            if now -  animate_time > 200:
                animate_time = now
                frame = (frame + 1) % len(PLAYER_WALK)
                SFX_WALK[frame].play()

            walk = PLAYER_WALK[frame]
            

            if walking_l == True: 
                walk = pygame.transform.flip(walk, True, False)

            character = walk.get_rect(topleft = (x, y)) 
            screen.blit(walk, character)
        
        else:
            character = PLAYER_IDLE.get_rect(topleft = (x, y)) 
            screen.blit(PLAYER_IDLE, character)
            frame = 0
        return character, animate_time, frame


# MOVEMENT
    def player_move(x_loc, y_loc, grounded, keys, rope_points, swing, jumped, dt, time, throw_rope, no_move, touch_rope, touch_x, touch_y, walking_l, walking_r):
        walking_l = False
        walking_r = False

        if grounded == True:
            if keys[pygame.K_LEFT]:
                x_loc -= PLAYER_SPEED
                walking_l = True
                
            if keys[pygame.K_RIGHT]:
                x_loc += PLAYER_SPEED
                walking_r = True
            
            if keys[pygame.K_UP]:
                y_loc += JUMP_FORCE
                grounded = False
                jumped = True    
            


        if throw_rope == True: 
            time -= dt
            jumped = False

            if time <= 0:
                throw_rope = False
                time = 0

            if touch_rope == True and keys[pygame.K_SPACE]:
                if time <= 0:
                    y_loc = rope_points[-1][1] + 10
                    swing = False
                    throw_rope = False
                    touch_rope = False
                    no_move = True
                    time = 0 

                else:
                    x_loc = touch_x
                    y_loc = touch_y

                    if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                        swing = True
                        x_loc = rope_points[-1][0] - 22
                        y_loc = rope_points[-3][1] - 22

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
                                touch_rope = False
                        else:
                            if no_move == True:
                                y_loc = touch_y
                                swing = False

        else:
            swing = False

        return grounded, x_loc, y_loc, swing, jumped, time, throw_rope, no_move, walking_l, walking_r
        
        
    
# PHYSICS
    def physics(x_velocity, y_velocity, x_loc, y_loc, grounded, jumped, scene, touch_rope):
        
        # Gravity
        attached = touch_rope and keys[pygame.K_SPACE]
        if attached == False:
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

                vx = (point[0] - point[2]) * 0.95
                vy = (point[1] - point[3]) * 0.95

                old_x = point[0]
                old_y = point[1]

                point[0] += vx
                point[1] += vy + GRAVITY

                point[2] = old_x
                point[3] = old_y

            for j in range(ITERATIONS):
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

                    if i == 1:
                        p2[0] -= offset_x
                        p2[1] -= offset_y
                    else:
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
        pygame.draw.circle(screen, (229, 185, 11), (int(anchor_x), int(anchor_y)), 10)

        return angle, angle_velocity, x_velocity, y_velocity

        

# COINS

    # Generate
    def gen_coin(x, y):
        coin = [COIN.get_rect(topleft = (x, y))] # FIX WHEN GET SPRITE COINS
        screen.blit(COIN, coin[0])
        return coin
    

    # Collect
    def get_coin(coin):
        SFX_COIN.play()
        coin += 1
        return coin

    # Use
    def use_coin(coin):
        SFX_USE_COIN.play()
        coin -= 1
        return coin

    # Display Count
    def count(count):
        draw_text(f"Coins: {count}", 25, 25)

# LIVES
    # Count
    def heart(lives):
        heart = []
        if lives > 9:
            lives = 9
        for i in range(lives):
            heart.append(HEART.get_rect(topleft = (560 - (i*30), 20)))
            screen.blit(HEART, heart[i])
        return heart

    # Generate
    def gen_heart(x, y):
            heart = [HEART.get_rect(topleft = (x, y))] 
            screen.blit(HEART, heart[0])
            return heart
    
    # Collect
    def get_heart(lives):
        lives += 1
        return lives
    
    # Lose
    def lose_life(lives):
        lives -= 1
        return lives

# PHONE BOOTH 

    # Sprite Rendering
    def draw_phonebooth():
        phonebooth = PHONE.get_rect(topleft = (480, GROUND - 130))
        screen.blit(PHONE, phonebooth)
        return phonebooth

    # Phone Screen
    def phone_buttons(buttons):
        screen.fill((0, 0, 0))
        for i in range(len(buttons)):
            screen.blit(BLUE_BUTTONS[i], buttons[i])

    # Phone sequence
    def phone_sequence(sequence, current_time):
        flash_timer = {
            'sequence': sequence,
            'step': 0,
            'sprite': GREEN_BUTTONS,
            'start_time': current_time,
            'duration': 500
            }

        return flash_timer

    # Dial
    def dial(buttons, sequence, mouse_pos, s, flash_timer):
        current_time = pygame.time.get_ticks()
    
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                SFX_CLICK.play()
                if s < len(sequence) and i == sequence[s]:
                    s += 1
                    flash_timer = {
                        'index': i,
                        'sprite': GREEN_BUTTONS,
                        'start_time': current_time,
                        'duration': 300
                    }

                    if s >= len(sequence):
                        return s, flash_timer, True

                    return s, flash_timer, None

                flash_timer = {
                    'index': i,
                    'sprite': RED_BUTTONS,
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
    
        if 'index' in flash_timer and 'sprite' in flash_timer:
            if elapsed >= flash_timer['duration']:
                return None

            index = flash_timer['index']
            color = flash_timer['sprite']

            for i, button in enumerate(buttons):
                if i == index:
                    screen.blit(color[i], button)
                else:
                    screen.blit(BLUE_BUTTONS[i], button)

            return flash_timer


        if 'sequence' in flash_timer:
            if elapsed >= flash_timer['duration']:
                flash_timer['step'] += 1
                flash_timer['start_time'] = current_time
                
                if flash_timer['step'] % 2 == 0:
                    SFX_BEEP.play()

                if flash_timer['step'] >= len(flash_timer['sequence']) * 2:
                    return None

            step = flash_timer['step']
            index = flash_timer['sequence'][step // 2]

            if step % 2 == 0:
                color = GREEN_BUTTONS  
            else:
                color = BLUE_BUTTONS

            for i, button in enumerate(buttons):
                if i == index:
                    screen.blit(color[i], button)
                else:
                    screen.blit(BLUE_BUTTONS[i], button)

            return flash_timer

        return None


    blink = pygame.time.get_ticks() + 4000


# LEVEL / SCENES
    def get_scene(scene, coin_collected, heart_collected, is_visible):
        barriers = []
        platforms = []
        structures = []
        coin = []
        hearts = []
    # 0 - Phone Call / Home 

        if scene == 1:
            structures.append(Polygon([(600, 0), (220, 0), (600, 180)]))
            platforms.append(pygame.Rect(10, 200, 300, 15)) # bed room loft
            platforms.append(pygame.Rect(310, 250, 75, 15)) # stairs
            platforms.append(pygame.Rect(390, 300, 75, 15)) # stairs
            platforms.append(pygame.Rect(390, 520, 200, 15)) # landing
            platforms.append(pygame.Rect(110, 520, 100, 15)) # landing
            platforms.append(pygame.Rect(10, 790, 100, 15))

            platforms.append(pygame.Rect(260, 790, 150, 15))
            # barriers.append([pygame.transform.scale(WIRE2, (400, 60)), (pygame.transform.scale(WIRE2, (400, 60))).get_rect(topleft = (290, 750))]) 
       

        elif scene == 2:
            structures.append(pygame.Rect(250, 0, 30, 200))


            platforms.append(pygame.Rect(120, 200, 200, 15))
            platforms.append(pygame.Rect(290, 200, 200, 15))

            structures.append(pygame.Rect(250, 415, 30, 280))

            platforms.append(pygame.Rect(120, 400, 310, 15))

            structures.append(pygame.Rect(400, 415, 30, 280))


            platforms.append(pygame.Rect(400, 680, 200, 15))
            
            platforms.append(pygame.Rect(0, 680, 120, 15)) 

            if not coin_collected: 
                coin = gen_coin(480, 620)


           
        elif scene == 3:
            structures.append(pygame.Rect(210, 0, 40, 300))
            structures.append(Polygon([(210, 260), (210, 360), (360, 360)]))

            platforms.append(pygame.Rect(0, 500, 250, 150)) 
            platforms.append(pygame.Rect(250, 550, 100, 100)) 
            platforms.append(pygame.Rect(350, 600, 100, 50)) 




            barriers.append([pygame.transform.scale(WIRE2, (360, 60)), (pygame.transform.scale(WIRE2, (360, 60))).get_rect(topleft = (240, 235))]) 



        # 1 -   

        elif scene == 4:
            platforms.append(pygame.Rect(10, 200, 200, 15))  
            platforms.append(pygame.Rect(500, 400, 100, 15))   
            platforms.append(pygame.Rect(250, 450, 100, 15))  
            platforms.append(pygame.Rect(10, 785, 300, 15))  

            barriers.append([pygame.transform.scale(WIRE2, (100, 60)), (pygame.transform.scale(WIRE2, (100, 60))).get_rect(topleft = (210, 250))]) 
            barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (350, 500))]) 
            
            

        
        elif scene == 5: 
            platforms.append(pygame.Rect(310, 200, 100, 15))
            platforms.append(pygame.Rect(400, 720, 200, 15))
            platforms.append(pygame.Rect(10, 200, 100, 15))

            if not coin_collected: 
                coin = gen_coin(150, 425)

            if not heart_collected: 
                hearts = gen_heart(50, 150)

            structures.append(pygame.Rect(350, 410, 20, 100))

            barriers.append([pygame.transform.scale(WIRE2, (340, 60)), (pygame.transform.scale(WIRE2, (340, 60))).get_rect(topleft = (10, 400))]) 



        elif scene == 6: 
            platforms.append(pygame.Rect(10, 200, 300, 15))
            platforms.append(pygame.Rect(210, 500, 200, 15))

            barriers.append([pygame.transform.scale(WIRE2, (100, 60)), (pygame.transform.scale(WIRE2, (100, 60))).get_rect(topleft = (320, 250))]) 
            barriers.append([pygame.transform.scale(WIRE2, (100, 60)), (pygame.transform.scale(WIRE2, (100, 60))).get_rect(topleft = (420, 550))]) 
           
            barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (10, 750))]) 

            
        elif scene == 7: ### EDIT -- add more?
            barriers.append([pygame.transform.scale(WIRE2, (200, 60)), (pygame.transform.scale(WIRE2, (200, 60))).get_rect(topleft = (10, 300))]) 

        # 2 - 

        elif scene == 8:
            platforms.append(pygame.Rect(10, 200, 150, 15))
            platforms.append(pygame.Rect(300, 200, 150, 15))

            barriers.append([pygame.transform.scale(WIRE2, (100, 60)), (pygame.transform.scale(WIRE2, (100, 60))).get_rect(topleft = (180, 250))]) 

            platforms.append(pygame.Rect(440, 450, 150, 15))

            barriers.append([pygame.transform.scale(WIRE2, (100, 60)), (pygame.transform.scale(WIRE2, (100, 60))).get_rect(topleft = (330, 500))]) 

            platforms.append(pygame.Rect(180, 450, 150, 15))

            platforms.append(pygame.Rect(10, 750, 150, 15))
            platforms.append(pygame.Rect(300, 750, 150, 15))

            barriers.append([pygame.transform.scale(WIRE2, (100, 60)), (pygame.transform.scale(WIRE2, (100, 60))).get_rect(topleft = (180, 750))]) 


        elif scene == 9:
            platforms.append(pygame.Rect(300, 200, 300, 15))

            platforms.append(pygame.Rect(300, 400, 300, 15))
            
            structures.append(pygame.Rect(300, 410, 20, 200))

            if not coin_collected: 
                coin = gen_coin(440, 500)

            if not heart_collected: 
                hearts = gen_heart(450, 350)

            platforms.append(pygame.Rect(10, 785, 400, 15))

            if is_visible == True:
                barriers.append([pygame.transform.scale(WIRE2, (300, 60)), (pygame.transform.scale(WIRE2, (300, 60))).get_rect(topleft = (10, 200))]) 
                barriers.append([pygame.transform.scale(WIRE2, (300, 60)), (pygame.transform.scale(WIRE2, (300, 60))).get_rect(topleft = (10, 400))]) 
                barriers.append([pygame.transform.scale(WIRE2, (180, 60)), (pygame.transform.scale(WIRE2, (180, 60))).get_rect(topleft = (420, 790))]) 

            else:
                barriers.append([pygame.transform.scale(WIRE1, (300, 10)), (pygame.transform.scale(WIRE1, (300, 10))).get_rect(topleft = (10, 200))]) 
                barriers.append([pygame.transform.scale(WIRE1, (300, 10)), (pygame.transform.scale(WIRE1, (300, 10))).get_rect(topleft = (10, 400))]) 
                barriers.append([pygame.transform.scale(WIRE1, (180, 10)), (pygame.transform.scale(WIRE1, (180, 10))).get_rect(topleft = (420, 790))]) 
                

            

        elif scene == 10: 
            platforms.append(pygame.Rect(400, 200, 200, 15))
            barriers.append([pygame.transform.scale(WIRE2, (100, 60)), (pygame.transform.scale(WIRE2, (100, 60))).get_rect(topleft = (290, 230))]) 
            platforms.append(pygame.Rect(130, 200, 150, 15))

            platforms.append(pygame.Rect(200, 500, 200, 15))
            barriers.append([pygame.transform.scale(WIRE2, (200, 60)), (pygame.transform.scale(WIRE2, (200, 60))).get_rect(topleft = (0, 500))]) 

            platforms.append(pygame.Rect(200, 750, 200, 15))
            barriers.append([pygame.transform.scale(WIRE2, (200, 60)), (pygame.transform.scale(WIRE2, (200, 60))).get_rect(topleft = (400, 750))]) 

        elif scene == 11:
            platforms.append(pygame.Rect(10, 200, 200, 15))

            if is_visible == True:
                barriers.append([pygame.transform.scale(WIRE2, (600, 60)), (pygame.transform.scale(WIRE2, (600, 60))).get_rect(topleft = (0, 300))]) 
                barriers.append([pygame.transform.scale(WIRE2, (600, 60)), (pygame.transform.scale(WIRE2, (600, 60))).get_rect(topleft = (0, 500))]) 

            else:
                barriers.append([pygame.transform.scale(WIRE1, (600, 10)), (pygame.transform.scale(WIRE1, (600, 10))).get_rect(topleft = (0, 300))]) 
                barriers.append([pygame.transform.scale(WIRE1, (600, 10)), (pygame.transform.scale(WIRE1, (600, 10))).get_rect(topleft = (0, 500))]) 
                



        # 3 - 

        elif scene == 12: 
            platforms.append(pygame.Rect(10, 200, 150, 15))
            platforms.append(pygame.Rect(450, 200, 150, 15))

            platforms.append(pygame.Rect(220, 400, 200, 15))

            platforms.append(pygame.Rect(10, 600, 150, 15))
            platforms.append(pygame.Rect(450, 600, 150, 15))

            platforms.append(pygame.Rect(220, 785, 200, 15))


            if is_visible == True:
                barriers.append([pygame.transform.scale(WIRE2, (200, 60)), (pygame.transform.scale(WIRE2, (200, 60))).get_rect(topleft = (220, 200))]) 
                barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (10, 400))]) 
                barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (450, 400))]) 
                barriers.append([pygame.transform.scale(WIRE2, (200, 60)), (pygame.transform.scale(WIRE2, (200, 60))).get_rect(topleft = (220, 600))]) 
                barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (10, 750))]) 
                barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (450, 750))]) 
            
            else:
                barriers.append([pygame.transform.scale(WIRE1, (200, 10)), (pygame.transform.scale(WIRE1, (200, 10))).get_rect(topleft = (220, 200))]) 
                barriers.append([pygame.transform.scale(WIRE1, (150, 10)), (pygame.transform.scale(WIRE1, (150, 10))).get_rect(topleft = (10, 400))]) 
                barriers.append([pygame.transform.scale(WIRE1, (150, 10)), (pygame.transform.scale(WIRE1, (150, 10))).get_rect(topleft = (450, 400))]) 
                barriers.append([pygame.transform.scale(WIRE1, (200, 10)), (pygame.transform.scale(WIRE1, (200, 10))).get_rect(topleft = (220, 600))]) 
                barriers.append([pygame.transform.scale(WIRE1, (150, 10)), (pygame.transform.scale(WIRE1, (150, 10))).get_rect(topleft = (10, 790))]) 
                barriers.append([pygame.transform.scale(WIRE1, (150, 10)), (pygame.transform.scale(WIRE1, (150, 10))).get_rect(topleft = (450, 790))]) 

                


        elif scene == 13: ### EDIT -- the top (3 platforms)
            platforms.append(pygame.Rect(10, 200, 100, 15))
            platforms.append(pygame.Rect(260, 250, 100, 15))
            platforms.append(pygame.Rect(490, 200, 100, 15))

            if not coin_collected: 
                coin = gen_coin(500, 120)

            if not heart_collected: 
                hearts = gen_heart(40, 130)


            if is_visible == True:
                barriers.append([pygame.transform.scale(WIRE2, (120, 60)), (pygame.transform.scale(WIRE2, (120, 60))).get_rect(topleft = (120, 300))]) 
                barriers.append([pygame.transform.scale(WIRE2, (120, 60)), (pygame.transform.scale(WIRE2, (120, 60))).get_rect(topleft = (380, 300))]) 
                barriers.append([pygame.transform.scale(WIRE2, (180, 60)), (pygame.transform.scale(WIRE2, (180, 60))).get_rect(topleft = (240, 600))]) 
 
            else:
                barriers.append([pygame.transform.scale(WIRE1, (120, 10)), (pygame.transform.scale(WIRE1, (120, 10))).get_rect(topleft = (120, 300))]) 
                barriers.append([pygame.transform.scale(WIRE1, (120, 10)), (pygame.transform.scale(WIRE1, (120, 10))).get_rect(topleft = (380, 300))]) 
                barriers.append([pygame.transform.scale(WIRE1, (180, 10)), (pygame.transform.scale(WIRE1, (180, 10))).get_rect(topleft = (240, 600))]) 
                

            barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (10, 750))]) 
            barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (440, 750))]) 

            
            

        elif scene == 14:
            platforms.append(pygame.Rect(175, 200, 250, 15))

            if is_visible == True:
                barriers.append([pygame.transform.scale(WIRE2, (600, 60)), (pygame.transform.scale(WIRE2, (600, 60))).get_rect(topleft = (0, 300))]) 
            else:
                barriers.append([pygame.transform.scale(WIRE1, (600, 10)), (pygame.transform.scale(WIRE1, (600, 10))).get_rect(topleft = (0, 300))]) 


            platforms.append(pygame.Rect(175, 500, 250, 15))

            barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (10, 750))]) 
            barriers.append([pygame.transform.scale(WIRE2, (150, 60)), (pygame.transform.scale(WIRE2, (150, 60))).get_rect(topleft = (440, 750))]) 

             

        elif scene == 15:
            platforms.append(pygame.Rect(250, 200, 150, 15))

            barriers.append([pygame.transform.scale(WIRE2, (200, 60)), (pygame.transform.scale(WIRE2, (200, 60))).get_rect(topleft = (400, 200))]) 

            platforms.append(pygame.Rect(120, 300, 100, 15))

            platforms.append(pygame.Rect(10, 500, 200, 15))

            if is_visible:
                barriers.append([pygame.transform.scale(WIRE2, (400, 60)), (pygame.transform.scale(WIRE2, (400, 60))).get_rect(topleft = (220, 500))]) 
            else:
                barriers.append([pygame.transform.scale(WIRE1, (400, 10)), (pygame.transform.scale(WIRE1, (400, 10))).get_rect(topleft = (220, 500))]) 





        # 4 - Final

        elif scene == 16:
            print("SCENE: ", scene)
        elif scene == 17:
            print("SCENE: ", scene)
        elif scene == 18:
            print("SCENE: ", scene)


        for barrier in barriers:
            screen.blit(barrier[0], barrier[1])
                    
        for platform in platforms:
            pygame.draw.rect(screen, BLACK, platform)

        for structure in structures:
            if isinstance(structure, Polygon):
                point = list(structure.exterior.coords)
                pygame.draw.polygon(screen, BLACK, point)
            else: 
                pygame.draw.rect(screen, BLACK, structure)
                

        return barriers, platforms, structures, coin, hearts


# PHONE BOOTH CUT-SCENES

    def phone_call(order, phone_script, phone_answer, lives):
        screen.fill((0, 0, 0))
    # Intro 
        if order == 0: 
            draw_text(phone_script[0], 100, 200)
            draw_text(phone_script[1], 100, 300)
            draw_text("Yes", 225, 600) 
            draw_text("No", 334, 600)

            if phone_answer != None:
                order = 1
            
    # 1 - “Have you had thoughts about how you might do this?” 
        elif order == 1: 
            draw_text(phone_script[2], 130, 200)
            draw_text(phone_script[3], 80, 250)
            draw_text("Yes", 225, 600) 
            draw_text("No", 334, 600) 
            if phone_answer != None:
                order = 2
            
            if phone_answer == True:
                lives = lose_life(lives)
                
                
    # 2 - “Are you safe?”
        elif order == 2: 
            draw_text(phone_script[4], 200, 200)
            draw_text("Yes", 225, 600) 
            draw_text("No", 334, 600) 
            if phone_answer != None:
                order = 3

            if phone_answer == False:
                lives = lose_life(lives)
                
    # 3 - “Do you need help?”
        elif order == 3: 
            draw_text(phone_script[5], 180, 200)
            draw_text("Yes", 225, 600) 
            draw_text("No", 334, 600) 
            if phone_answer != None:
                order = 4

            if phone_answer == False:
                lives = lose_life(lives)
                
    # 4 - You’ve reached the end of the line…
        elif order == 4: 
            draw_text(phone_script[6], 100, 200)
            draw_text(phone_script[7], 100, 250)
    # Ending 1 

    # Ending 2
        return order, phone_answer, lives
        



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
                if phone_ringing == False:
                    if seq_played == True:   
                        s, flash_timer, call = dial(buttons, sequence, mouse_pos, s, flash_timer)

                    elif event.button == 1:
                        SFX_THROW.play()
                        x_rope, y_rope = mouse_pos
                        rope_points = []
                        for i in range(SEGMENTS):
                            rope_points.append([x_rope, y_rope + i * SEGMENT_LENGTH, x_rope, y_rope + i * SEGMENT_LENGTH])
                        rope_points[1][0] += random.uniform(-5, 5)


                        # Reset swing physics
                        angle = 0
                        angle_velocity = 0
                        swing = False

                        throw_rope = True
                        time = 5

            if event.type == pygame.KEYDOWN:
                if coin_yes == None:
                    if event.key == pygame.K_y:
                        coin_yes = True
                    if event.key == pygame.K_n:
                        coin_yes = False

                elif coin_yes == True:
                    if event.key == pygame.K_y:
                        phone_answer = True
                    elif event.key == pygame.K_n:
                        phone_answer = False

                if tut_screen == True:
                    if event.key == pygame.K_RETURN:
                        if throw_rope == True:
                            idx += 1
                        tut_screen = False

        
        if coin_yes == None:
            screen.blit(BG, (0,0))
            current_time = pygame.time.get_ticks()

            

            
            if current_time >= blink:
                is_visible = not is_visible
                blink = current_time + 4000
            barriers, platforms, structures, coin, hearts = get_scene(scene, coin_collected, heart_collected, is_visible)
            walls()

            if scene == 3 or scene == 7 or scene == 11 or scene == 15 or scene == 18:
                floor = ground()
                pygame.draw.rect(screen, BLACK, floor)

                # Rope hits ground/platforms/etc
                for i in range(len(rope_points)):
                    if floor.collidepoint(rope_points[i][0], rope_points[i][1]):
                        rope_points[i][1] = floor.top

            # TUT
            if scene <= 3:
                if tut_screen == True:
                    tutorial(tut_text, idx, tut_track)

            if scene == 3 and grounded == True and tut_track[7] == False:
                idx = 7
                tut_screen = True

            if (scene == 4 or scene == 8 or scene == 12 or scene == 16) and respawn == True:
                x = 20
                y = 100
                respawn = False

            player(jumped, grounded, walking_l, walking_r, animate_time, touch_rope, frame, x, y)
            
            

        
            keys = pygame.key.get_pressed()
    

        # ROPE
            if throw_rope == True:
                if scene == 1 and tut_track[2] == False:
                        idx = 2
                        tut_screen = True
                elif scene == 1 and tut_track[3] == False:
                    tut_screen = True
                elif scene == 1 and tut_track[4] == False:
                    tut_screen = True
                angle, angle_velocity, x_velocity, y_velocity = rope(rope_points, angle, angle_velocity, swing, x_velocity, y_velocity, keys)
        
        # MOVE      
            character, animate_time, frame = player(jumped, grounded, walking_l, walking_r, animate_time, touch_rope, frame, x, y)  
            grounded, x, y, swing, jumped, time, throw_rope, no_move, walking_l, walking_r = player_move(x, y, grounded, keys, rope_points, swing, jumped, dt, time, throw_rope, no_move, touch_rope, touch_x, touch_y, walking_l, walking_r)
            grounded, x, y, scene, x_velocity, y_velocity, jumped = physics(x_velocity, y_velocity, x, y, grounded, jumped, scene, touch_rope)

            

     # COLLISIONS

            # coins
            if len(coin) > 0: ## FIX 
                if character.colliderect(coin[0]):
                    coin_count = get_coin(coin_count)
                    coin_collected = True
                    coin.remove(coin[0])

            # hearts
            if len(hearts) > 0: ## FIX 
                if character.colliderect(hearts[0]):
                    lives = get_heart(lives)
                    heart_collected = True
                    hearts.remove(hearts[0])

                          

            if scene == 3 or scene == 7 or scene == 11 or scene == 15:
                draw_phonebooth()
                if coin_count > 0:        
                    if character.colliderect(draw_phonebooth()):
                        pygame.draw.rect(screen, BLACK, (200, 400, 200, 100))  
                        draw_text("Use Coin?", 235, 410) 
                        draw_text("Yes", 225, 460) 
                        draw_text("No", 334, 460) 

            # Rope collision
            rope_collision = False
            if throw_rope == True:
                for i in range(len(rope_points) - 1):
                    start_point = (rope_points[i][0], rope_points[i][1])
                    end_point = (rope_points[i+1][0], rope_points[i+1][1])

                    if character.clipline(start_point, end_point):
                        rope_collision = True
                        break

            if rope_collision == True:
                touch_x = x
                touch_y = y
                if touch_rope == False and not keys[pygame.K_SPACE]:
                    time = 5
                    touch_rope = True
            else:
                touch_x = None
                touch_y = None
                swing = False
                touch_rope = False


        # Barriers  
            hit_barrier = False
            for barrier in barriers:
                if character.colliderect(barrier[1]):
                    hit_barrier = True
                    break

        # Lives
            if hit_barrier == True:
                if scene <= 3 and tut_track[6] == False:
                    idx = 6
                    tut_screen = True
                if life == False: 
                    lives = lose_life(lives)
                    life = True
            else:
                life = False

        # Check Lives
            if lives <= 0:
                print("END GAME")


        # Platforms

            #tut
            if scene == 1 and tut_track[1] == False:
                if character.colliderect(platforms[3]):
                    idx = 1
                    tut_screen = True

            if scene == 2 and tut_track[5] == False:
                if character.colliderect(platforms[0]) or character.colliderect(platforms[1]):
                    idx = 5
                    tut_screen = True

            

            for platform in platforms:
                if character.colliderect(platform):
                    grounded = True
                    if y > platform.y - 110: 
                        y = platform.y - 110
                    break
                if scene == 3 or scene == 7 or scene == 11 or scene == 15:
                    if character.colliderect(ground()):
                        if y > GROUND - 110:
                            y = GROUND - 100
                            grounded = True
                    else: 
                        grounded = False

                else:
                    grounded = False
            

        # Structures
            for structure in structures:

                if not isinstance(structure, Polygon):    
                    if character.colliderect(structure):

                        overlap_left = character.right - structure.left
                        overlap_right = structure.right - character.left

                        if overlap_left < overlap_right:
                            character.right = structure.left
                        else:
                            character.left = structure.right

                        x = character.left
                    
                        break

           

            # Coin Count Display
            count(coin_count)

            # Hearts
            heart(lives)

        elif coin_yes == True:

            # Phone call
            if phone_screen == None:
                coin_count = use_coin(coin_count)
                phone_screen = True

            if phone_screen == True:
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
                    if phone_ringing == False:
                        RINGTONE.play(-1)  
                        phone_ringing = True
                    order, phone_answer, lives = phone_call(order, phone_script, phone_answer, lives) 
                    if phone_answer != None:
                        RINGTONE.stop()
                        phone_ringing = False
                        call = None
                        s = 0
                        scene += 1
                        seq_played = False
                        coin_yes = False
                        phone_answer = None
                        phone_screen = None
                elif call == False:
                    RINGTONE.stop()
                    phone_ringing = False
                    call = None
                    s = 0
                    seq_played = False

            # Reset for next level
            respawn = True
            coin_collected = False
            heart_collected = False



        elif coin_yes == False:
            x = 390
            coin_yes = None

        
        pygame.display.flip()
        
                    
        await asyncio.sleep(0)




asyncio.run(main())  