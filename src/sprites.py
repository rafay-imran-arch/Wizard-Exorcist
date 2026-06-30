# script for my sprites 
import pygame
import os
import random

pygame.init()

class player():

    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

        #some constant attributes 
        (self.x_pos, self.y_pos) = (self.x_pos, self.y_pos)
        self.vel = 5
        self.facing = 'downwards'  
        self.walk_count = 0
        self.is_moving = False
        self.is_jump = False
        self.hit_box = (self.x_pos + 10, self.y_pos, 100, 128)
        self.mana = 10
        self.health = 10

        #Defining player visuals
        self.idle_dir = os.path.join('src', 'assets', 'wizards', 'Char 1', 'Type 1', 'Attack')
        self.walk_dir = os.path.join('src', 'assets', 'wizards', 'Char 1', 'Type 1', 'Run')

        self.character_size = (128,128)

        #Defining idle 
        self.idle_up = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle_dir,'atk_1.png')),
            self.character_size
        )
        self.idle_down = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle_dir,'atk_3.png')),
            self.character_size
        )
        self.idle_left = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle_dir,'atk_4.png')),
            self.character_size
        )
        self.idle_right = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle_dir,'atk_2.png')),
            self.character_size
        )

        #defining walk cycles 
        self.walk_up = [pygame.transform.scale(
            pygame.image.load(os.path.join(self.walk_dir, f"RunUP_{i}.png")),
            self.character_size
        ) for i in range(4)]

        self.walk_down = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.walk_dir, f"RunDW_{i}.png")),
            self.character_size
        ) for i in range(4)
        ]

        self.walk_right = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.walk_dir,f"Run_{i}.png")),
            self.character_size
        ) for i in range(4)
        ]

        self.walk_left = [
            pygame.transform.flip(sprite, True, False) for sprite in self.walk_right
            ]
        
    def draw(self, screen):
        #self.rect.x = self.x_pos
        #self.rect.y = self.y_pos

        if self.walk_count + 1 >= 24:
            self.walk_count = 0

        if not self.is_moving:
            if self.facing == "upwards":
                screen.blit(self.idle_up, (self.x_pos, self.y_pos))
            elif self.facing == "downwards":
                screen.blit(self.idle_down, (self.x_pos, self.y_pos))
            elif self.facing == "right":
                screen.blit(self.idle_right, (self.x_pos, self.y_pos))
            elif self.facing == 'left':
                screen.blit(self.idle_left, (self.x_pos, self.y_pos))
            self.walk_count = 0
        else:
            if self.facing == "upwards":
                screen.blit(self.walk_up[self.walk_count // 6], (self.x_pos, self.y_pos))
                self.walk_count += 1
            elif self.facing == "downwards":
                screen.blit(self.walk_down[self.walk_count // 6], (self.x_pos, self.y_pos))
                self.walk_count += 1
            elif self.facing == "left":
                screen.blit(self.walk_left[self.walk_count // 6], (self.x_pos, self.y_pos))
                self.walk_count += 1
            elif self.facing == "right":
                screen.blit(self.walk_right[self.walk_count // 6], (self.x_pos, self.y_pos))
                self.walk_count += 1
    
        # collision hitbox
        self.hit_box = (self.x_pos + 10, self.y_pos, 100, 128)
        pygame.draw.rect(screen, (0,255,0), self.hit_box, 2)

        #Mana and Health bar
        pygame.draw.rect(screen, (255,128,140), (self.hit_box[0], self.hit_box[1]-20 , 80, 10))
        mana_width = int((self.mana/10)*80)
        pygame.draw.rect(screen, (128,255,210), (self.hit_box[0], self.hit_box[1]-20, mana_width, 10))
        #health 
        pygame.draw.rect(screen, (255,0,0), (self.hit_box[0], self.hit_box[1]-10, 80, 10))
        health_width = int((self.health/10) * 80)
        if health_width <0: health_width = 0
        pygame.draw.rect(screen, (40,255,40), (self.hit_box[0], self.hit_box[1]-10, health_width, 10))


    def hit(self):
        if self.health > 0:
            self.health -= 1
            self.walk_count = 0
            pygame.display.update()
       


class enemy():
    
    def __init__(self,x, y, width, height, max_health, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = max_health
        self.max_health = max_health
        self.vel = vel

        #Some constants 
        self.walk_count = 0
        self.visible = True
        self.hit_box = (self.x, self.y, self.width, self.height)

        self.enemy_dir = os.path.join('src','assets', 'creatures')

    def draw(self, screen, offset_y, bar_width):
        if self.visible:
            pygame.draw.rect(screen, (255,0,0), (self.hit_box[0], self.hit_box[1] - offset_y, bar_width, 8))
            health_percentage = self.health / self.max_health
            fill_width = int(bar_width * health_percentage)
            pygame.draw.rect(screen, (128,255,200), (self.hit_box[0], self.hit_box[1]- offset_y, fill_width, 8))

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else: 
            self.visible = False


class ghost(enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x,y,width,height,max_health=10,vel=1.5)

        #Asset loading of ghosts
        ghost_dir = os.path.join(self.enemy_dir, 'Ghost')

        master_sheet = pygame.image.load(os.path.join(ghost_dir, '128ghost.png')).convert_alpha()
        self.ghost_frames = [pygame.transform.scale(
            master_sheet.subsurface(pygame.Rect(i*256, 0, 256, 256)), 
            (128, 128),
            ) for i in range(4)
        ]

    def move(self, wizard, enemies):
        if self.visible:
            if self.x < wizard.x_pos:
                self.x += self.vel
            elif self.x >  wizard.x_pos:
                self.x -= self.vel
            if self.y < wizard.y_pos:
                self.y += self.vel
            elif self.y > wizard.y_pos:
                self.y -= self.vel
            

        for other in enemies:
            if other == self or not other.visible:
                continue
            distance_x = self.x - other.x
            distance_y = self.y - other.y

            if abs(distance_x) < 40 and abs(distance_y) < 40:
                if distance_x > 0: self.x += 1
                else: self.x -= 1
                if distance_y > 0: self.y += 1
                else: self.y -= 1

    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)  
        if self.visible:

            frame_index = (self.walk_count // 6) % len(self.ghost_frames)
            current_frame = self.ghost_frames[frame_index]
            self.walk_count += 1
            screen.blit(current_frame, (self.x, self.y))


            pad_x = 24
            pad_y = 25
            hit_x = self.x + pad_x
            hit_y = self.y + pad_y
            hit_w = self.width - (2 * pad_x)
            hit_h = self.height - (2 * pad_y)
            self.hit_box = (hit_x, hit_y, hit_w, hit_h)
            pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)

            super().draw(screen, offset_y, bar_width)



class bat(enemy):

    def __init__(self, x, y, width, height):
        super().__init__(x,y,width,height,max_health=5,vel=2.5)

        #bat assets
        self.bat_dir = os.path.join(self.enemy_dir, "Bat")

        master_sheet = pygame.image.load(os.path.join(self.bat_dir, '96bat.png'))
        self.bat_frames = [pygame.transform.scale(
            master_sheet.subsurface(pygame.Rect(i*192, 0, 192, 192)),
            (128,128)
        ) for i in range(4)
        ]

    def move(self, wizard, enemies):
        if self.visible:
            if self.x < wizard.x_pos:
                self.x += self.vel
            elif self.x > wizard.x_pos:
                self.x -= self.vel

            if self.y < wizard.y_pos:
                self.y += self.vel
            elif self.y > wizard.y_pos:
                self.y -= self.vel 

        for other in enemies:
            if other == self or not other.visible:
                continue

            distance_x = self.x - other.x
            distance_y = self.y - other.y

            if abs(distance_x) < 40 and abs(distance_y) < 40:
                if distance_x > 0: self.x += 1
                else: self.x -= 1
                if distance_y > 0: self.y += 1
                else: self.y -= 1


    
    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)
        if self.visible:

            frame_index = (self.walk_count // 6) % len(self.bat_frames)
            current_frame = self.bat_frames[frame_index]
            self.walk_count += 1
            screen.blit(current_frame, (self.x,self.y))

            pad_x = 24
            pad_y = 25
            hit_x = self.x + pad_x
            hit_y = self.y + pad_y
            hit_w = self.width - (2 * pad_x)
            hit_h = self.height - (2 * pad_y)
            self.hit_box = (hit_x, hit_y, hit_w, hit_h)
            pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)


            super().draw(screen, offset_y, bar_width)


class slime(enemy):

    def __init__(self,x, y, width, height):
        super().__init__(x, y, width, height, max_health=15, vel=2.2)

        #loading slime assets
        slime_dir = os.path.join(self.enemy_dir, 'Slime')

        master_sheet = pygame.image.load(os.path.join(slime_dir, 'Slime-64x64.png'))
        # The sheet has 6 columns. We loop 9 times total.
        self.slime_frames = []
        for i in range(9):
            col = i % 6  # Goes 0, 1, 2, 3, 4, 5, then loops back to 0
            row = i // 6 # Stays 0 for the first 6 frames, then becomes 1 for the rest

            x_pixel = col * 64
            y_pixel = row * 64

            # Cut the tiny 64x64 frame out
            frame = master_sheet.subsurface(pygame.Rect(x_pixel, y_pixel, 64, 64))
            
            # Scale it up to 128x128 so it matches your other enemies!
            self.slime_frames.append(pygame.transform.scale(frame, (128, 128)))
            
    def move(self,wizard,enemies):
        if self.visible:
            if self.x < wizard.x_pos:
                self.x += self.vel
            elif self.x > wizard.x_pos:
                self.x -= self.vel
            
            if self.y < wizard.y_pos:
                self.y += self.vel
            elif self.y > wizard.y_pos:
                self.y -= self.vel

        for other in enemies:
            if other == self or not other.visible:
                continue
            
            distance_x =  self.x - other.x
            distance_y = self.y - other.y

            if abs(distance_x) < 40 and abs(distance_y) < 40:
                if distance_x > 0: self.x += 1
                else: self.x -= 1
                if distance_y > 0: self.y += 1
                else: self.y -= 1

    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)
        if self.visible:

            num_frames = max(1, len(self.slime_frames))
            frame_index = (self.walk_count // 3) % num_frames
            current_frame = self.slime_frames[frame_index]
            self.walk_count += 1
            screen.blit(current_frame, (self.x, self.y))

            pad_x = 20
            pad_y = 25
            hit_x = self.x + pad_x 
            hit_y = self.y + pad_y + 15
            hit_w = self.width - (2 * pad_x)
            hit_h = self.height - (2 * pad_y)
            self.hit_box = (hit_x, hit_y, hit_w, hit_h)
            pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)

            super().draw(screen, offset_y, bar_width)


class pumpkin(enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, max_health=25, vel=1.8)

        pumpkin_dir = os.path.join(self.enemy_dir, 'Pumpkin')

        master_sheet = pygame.image.load(os.path.join(pumpkin_dir, 'Pumpkin-160x160.png'))

        total_width = master_sheet.get_width()
        frame_width = total_width // 6
        frame_height = master_sheet.get_height()

        self.pumpkin_frames = [pygame.transform.scale(
            master_sheet.subsurface(pygame.Rect(i*frame_width,0,frame_width,frame_height)),
            (128,128)
        ) for i in range(6)
        ]

    def move(self, wizard, enemies):
        if self.visible: 
            if self.x < wizard.x_pos:
                self.x += self.vel
            elif self.x > wizard.x_pos:
                self.x -= self.vel
            if self.y < wizard.y_pos:
                self.y += self.vel
            elif self.y > wizard.y_pos:
                self.y -= self.vel

        for other in enemies: 
            if other == self or not other.visible:
                continue
            
            distance_x = self.x - other.x
            distance_y = self.x - other.y

            if abs(distance_x) < 40 and abs(distance_y) < 40:
                if distance_x > 0: self.x += 1
                else: self.x -= 1
                if distance_y > 0: self.y += 1
                else: self.y -= 1
            
    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)

        if self.visible:

            frame_index = (self.walk_count // 3) % len(self.pumpkin_frames)
            current_frame = self.pumpkin_frames[frame_index]
            self.walk_count += 1
            screen.blit(current_frame, (self.x, self.y))

            pad_x = 24
            pad_y = 25
            hit_x = self.x + pad_x
            hit_y = self.y + pad_y
            hit_w = self.width - (2 * pad_x)
            hit_h = self.height - (2 * pad_y)
            self.hit_box = (hit_x, hit_y, hit_w, hit_h)
            pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)


            super().draw(screen, offset_y, bar_width)


class keys_drop():
    def __init__(self):
        random_x =  random.randint(50,700)
        random_y = random.randint(50,700)
        self.rect = pygame.Rect(random_x, random_y, 16, 16)
        self.visible = False
        self.collected = False
        self.text_timer = 0

        self.current_frame = 0
        self.animated_speed = 0.2
        self.key_dir = os.path.join('src', 'assets', 'keys', 'Key 4', 'SILVER')
        self.key_frames = [ pygame.transform.scale_by(
            pygame.image.load(os.path.join(self.key_dir, f'Key 4 - SILVER - {i:04d}.png')).convert_alpha(),
            2
        ) for i in range(4)
        ]
    
    def draw(self, screen):
        if self.visible and not self.collected:
            
            self.current_frame += self.animated_speed
            if self.current_frame >= len(self.key_frames):
                self.current_frame = 0 

            active_sprite = self.key_frames[int(self.current_frame)]
            screen.blit(active_sprite, (self.rect.x, self.rect.y))