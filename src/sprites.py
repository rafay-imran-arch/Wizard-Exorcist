# script for my sprites 
import pygame
import os
import random
import math 


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
        self.hit_box = (self.x_pos + 32, self.y_pos + 25, 64, 90)
        self.mana = 10
        self.health = 100
        self.max_health = 100

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

        # player death stuff
        self.is_dying = False
        self.death_animation_count = 0
        self.dying_dir = os.path.join("src", "assets", "effects", "eff", "PNG", "Smoke Bursts","stylized_skull_smoke_burst_001", "stylized_skull_smoke_burst_001_small_white")
        self.death_frames = [   pygame.transform.scale(
            pygame.image.load(os.path.join(self.dying_dir, f"frame{i:04}.png")),
            (128, 128)
        ) for i in range(12)
        ]
        
    def draw(self, screen):
        #self.rect.x = self.x_pos
        #self.rect.y = self.y_pos
        if self.is_dying:
            self.play_death_animation(screen)
            return 
        
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
        self.hit_box = (self.x_pos + 32, self.y_pos + 25, 64, 90)

        #Mana and Health bar
        pygame.draw.rect(screen, (255,128,140), (self.hit_box[0], self.hit_box[1]-20 , 80, 10))
        mana_width = int((self.mana/10)*80)
        pygame.draw.rect(screen, (128,255,210), (self.hit_box[0], self.hit_box[1]-20, mana_width, 10))
        #health bar system upgraded with better health 100 and accurate visual loss
        pygame.draw.rect(screen, (255,0,0), (self.hit_box[0], self.hit_box[1]-10, 80, 10))
        health_ratio =  self.health / self.max_health
        health_width = int(health_ratio * 80)
        if health_width < 0:
            health_width = 0
        pygame.draw.rect(screen, (40,255,40), (self.hit_box[0], self.hit_box[1]-10, health_width, 10))
    

    def hit(self, damage_ammount):
        if self.health > 0:
            self.health -= damage_ammount
            self.walk_count = 0
            if self.health <=0:
                self.health = 0
                self.is_dying = True 


    def play_death_animation(self, screen):
        if self.death_frames:
            frame_index = self.death_animation_count // 3
            if frame_index < len(self.death_frames):
                screen.blit(self.death_frames[frame_index], (self.x_pos + 64, self.y_pos + 64))
                self.death_animation_count += 1

class enemy():
    
    def __init__(self,x, y, width, height, max_health, vel, damage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = max_health
        self.max_health = max_health
        self.vel = vel
        self.damage = damage
        

        #Some constants 
        self.walk_count = 0
        self.visible = True
        self.hit_box = (self.x, self.y, self.width, self.height)

        # for dead animation
        self.is_dying = False
        self.death_animation_count = 0


        # assets for death effecs
        self.spell_dir = os.path.join('src', 'assets', 'spells')
        self.effect_dir = os.path.join('src', 'assets', 'effects', 'eff', 'PNG')
        self.death_dir = os.path.join(self.effect_dir, 'Fantasy Spells', 'spell_poison_001', 'spell_poison_001_small_green')
        self.death_frames = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.death_dir, f"frame{i:04}.png")),
            (64, 64)
        ) for i in range(17)
        ]

        self.enemy_dir = os.path.join('src','assets', 'creatures')

    def draw(self, screen, offset_y, bar_width):
        if self.is_dying:
            self.play_death_animation(screen)
            return
        
        if self.visible:
            pygame.draw.rect(screen, (255,0,0), (self.hit_box[0], self.hit_box[1] - offset_y, bar_width, 8))
            health_percentage = self.health / self.max_health
            fill_width = int(bar_width * health_percentage)
            pygame.draw.rect(screen, (128,255,200), (self.hit_box[0], self.hit_box[1]- offset_y, fill_width, 8))

    def handle_seperation(self, enemies, radius=40, push_strength=2):
        #At first I did for each enemy then I remembered inheritance so....
        for other in enemies:
            if other == self or not other.visible or other.is_dying:
                continue

            distance_x = self.x - other.x
            distance_y = self.y - other.y

            if abs(distance_x) < radius and abs(distance_y) < radius:
                if distance_x > 0:
                    self.x += push_strength
                elif distance_x < 0:
                    self.x -= push_strength
                else: 
                    self.x += random.choice([-1,1])

                if distance_y > 0:
                    self.y += push_strength
                elif distance_y < 0:
                    self.y -= push_strength
                else:
                    self.y += random.choice([-1,1])

    def hit(self):
        if not self.is_dying and self.health >0:
            self.health -= 1
            if self.health <= 0:
                self.health = 0 
                self.is_dying = True
                self.death_animation_count = 0

    def play_death_animation(self, screen):

        if self.death_frames:
            frame_index = (self.death_animation_count // 2) 
            if frame_index < len(self.death_frames):
                current_frame = self.death_frames[frame_index]
                center_x = self.x + 32
                center_y = self.y + 32
                screen.blit(current_frame, (center_x, center_y))
                self.death_animation_count += 1
            else:
                self.visible = False
                self.is_dying = False
       
        else:
            self.visible = False
            self.is_dying = False



class ghost(enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x,y,width,height,max_health=10,vel=1.5, damage=2.5)

        #Asset loading of ghosts
        ghost_dir = os.path.join(self.enemy_dir, 'Ghost')

        master_sheet = pygame.image.load(os.path.join(ghost_dir, '128ghost.png')).convert_alpha()
        self.ghost_frames = [pygame.transform.scale(
            master_sheet.subsurface(pygame.Rect(i*256, 0, 256, 256)), 
            (128, 128),
            ) for i in range(4)
        ]

    def move(self, wizard, enemies):
        if not self.visible or self.is_dying:
            return
        
        wizard_center_x = wizard.hit_box[0] + wizard.hit_box[2] // 2
        wizard_center_y = wizard.hit_box[1] + wizard.hit_box[3] // 2

        ghost_center_x = self.hit_box[0] + self.hit_box[2] // 2
        ghost_center_y = self.hit_box[1] + self.hit_box[3] // 2

        if self.visible:
            if ghost_center_x < wizard_center_x:
                self.x += self.vel
            elif ghost_center_x > wizard_center_x:
                self.x -= self.vel 

            if ghost_center_y < wizard_center_y:
                self.y += self.vel
            elif ghost_center_y > wizard_center_y:
                self.y -= self.vel

            self.handle_seperation(enemies, radius=40, push_strength=2)

    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)  
        if self.is_dying:
                    self.play_death_animation(screen)
                    return
        
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

            super().draw(screen, offset_y, bar_width)

        
class bat(enemy):

    def __init__(self, x, y, width, height, facing="downwards"):
        super().__init__(x,y,width,height,max_health=5,vel=2.5, damage=1.5)
        self.shoot_cooldown = 240
        self.type = "bat"
        self.max_cooldown = 240
        self.facing = facing

        #bat assets
        self.bat_dir = os.path.join(self.enemy_dir, "Bat")

        master_sheet = pygame.image.load(os.path.join(self.bat_dir, '96bat.png'))
        self.bat_frames = [pygame.transform.scale(
            master_sheet.subsurface(pygame.Rect(i*192, 0, 192, 192)),
            (128,128)
        ) for i in range(4)
        ]

    def move(self, wizard, enemies):
        if not self.visible and self.is_dying:
            return
        
    

        if self.visible:
            if self.x < wizard.x_pos: 
                self.x += self.vel
            elif self.x > wizard.x_pos:
                self.x -= self.vel 

            if self.y < wizard.y_pos:
                self.y += self.vel
            elif self.y > wizard.y_pos:
                self.y -= self.vel

        self.handle_seperation(enemies, radius=40, push_strength=2)


    
    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)

        if self.is_dying:
            self.play_death_animation(screen)
            return
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
            


            super().draw(screen, offset_y, bar_width)
        
class slime(enemy):

    def __init__(self,x, y, width, height, is_small=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.type = 'slime'
        self.is_small = is_small
        if self.is_small:
            super().__init__(x, y, width, height, max_health=5, vel=3.5, damage=2)
            self.type = 'small_slime'
        else:
            super().__init__(x, y, width, height, max_health=15, vel=2.2, damage=4.5)
            self.type = 'slime'
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
            if self.is_small:
                self.slime_frames.append(pygame.transform.scale(frame, (64, 64)))
            else:
                self.slime_frames.append(pygame.transform.scale(frame, (128,128)))
            
    def move(self,wizard,enemies):
        if not self.visible and self.is_dying:
            return
        wizard_center_x = wizard.hit_box[0] + wizard.hit_box[2] // 2
        wizard_center_y = wizard.hit_box[1] + wizard.hit_box[3] // 2
        
        current_size = 64 if self.is_small else 128
        slime_center_x = self.x + current_size // 2
        slime_center_y = self.y + current_size // 2

        if self.visible:
            if slime_center_x < wizard_center_x:
                self.x += self.vel
            elif slime_center_x > wizard_center_x:
                self.x -= self.vel
            
            if slime_center_y < wizard_center_y:
                self.y += self.vel
            elif slime_center_y > wizard_center_y:
                self.y -= self.vel

        sep_radius = 20 if self.is_small else 40
        self.handle_seperation(enemies, radius=sep_radius, push_strength=2)

    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)

        if self.is_dying:
            self.play_death_animation(screen)
            return 
        
        if self.visible:
    
            num_frames = max(1, len(self.slime_frames))
            frame_index = (self.walk_count // 3) % num_frames
            current_frame = self.slime_frames[frame_index]
            self.walk_count += 1
            screen.blit(current_frame, (self.x, self.y))

            pad_x = 10 if self.is_small else 20
            pad_y = 13 if self.is_small else 25
            hit_x = self.x + pad_x 
            hit_y = self.y + pad_y + 15
            hit_w = self.width - (2 * pad_x)
            hit_h = self.height - (2 * pad_y)
            self.hit_box = (hit_x, hit_y, hit_w, hit_h)

            super().draw(screen, offset_y, bar_width)

    def hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health <= 0:
                self.health = 0
                self.is_dying = True 
                #self.visible = False

class pumpkin(enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, max_health=25, vel=1.8, damage=5)

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

        self.state = "chase"
        self.state_timer = 0
        self.charge_dx = 0 
        self.charge_dy = 0
        self.charge_speed = 9.0
        self.rotation_angle = 0 

    def move(self, wizard, enemies):
        if not self.visible and self.is_dying:
            return
        wizard_center_x = wizard.hit_box[0] + wizard.hit_box[2] // 2
        wizard_center_y = wizard.hit_box[1] + wizard.hit_box[3] // 2

        pumpkin_center_x = self.hit_box[0] + self.hit_box[2] // 2
        pumpkin_center_y = self.hit_box[1] + self.hit_box[3] // 2   

        dist_x = wizard_center_x - pumpkin_center_x
        dist_y = wizard_center_y - pumpkin_center_y
        distance = math.hypot(dist_x, dist_y)

        if self.state == "chase":
            if distance > 0:
                self.x += (dist_x / distance) * self.vel 
                self.y += (dist_y / distance) * self.vel 

            if distance < 250:
                self.state = "windup"
                self.state_timer = 20 

                self.charge_dx = dist_x / distance if distance > 0 else 1
                self.charge_dy = dist_y / distance if distance > 0 else 0
        
        elif self.state == "windup":
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = "charge"
                self.state_timer = 40

        elif self.state == "charge":
            self.x += self.charge_dx * self.charge_speed
            self.y += self.charge_dy * self.charge_speed

            self.rotation_angle = (self.rotation_angle - 25) % 360

            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = "cooldown"
                self.state_timer = 10

        elif self.state == "cooldown":
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = "chase"

        self.handle_seperation(enemies, radius=40, push_strength=2)
            
    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)
        if self.is_dying:
            self.play_death_animation(screen)
            return 
        
        if self.visible:

            frame_index = (self.walk_count // 3) % len(self.pumpkin_frames)
            current_frame = self.pumpkin_frames[frame_index]
            self.walk_count += 1
            
            if self.state == "charge":
                rotated_frame = pygame.transform.rotate(current_frame, self.rotation_angle)
                new_rect = rotated_frame.get_rect(center=current_frame.get_rect(topleft=(self.x, self.y)).center)
                screen.blit(rotated_frame, new_rect.topleft)

            elif self.state == "windup":
                tinted = current_frame.copy()
                tinted.fill((255, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted, (self.x, self.y))
            else:
                screen.blit(current_frame, (self.x, self.y))

            pad_x = 24
            pad_y = 25
            hit_x = self.x + pad_x
            hit_y = self.y + pad_y
            hit_w = self.width - (2 * pad_x)
            hit_h = self.height - (2 * pad_y)
            self.hit_box = (hit_x, hit_y, hit_w, hit_h)

            if getattr(wizard, 'admin_mode', False):
                pygame.draw.rect(screen, (255,0,0), self.hit_box, 2)
            super().draw(screen, offset_y, bar_width)

#Likely the boss in the dungeon stairs room (this room shall only open once all others are cleared)
class oneI(enemy):
    
    def __init__(self,x, y, width, height, facing="downwards"):
        super().__init__(x, y, width, height, max_health=60, vel=3, damage=10)
        self.type = "oneI"
        self.facing = facing
        self.shoot_cooldown = 120
        self.max_shoot_cooldown = 120
        self.beam_cooldown = 300
        self.radial_cooldown = 240



        #loading the oneI-ed assets
        oneI_dir = os.path.join(self.enemy_dir, "Pyramid")

        master_sheet = pygame.image.load(os.path.join(oneI_dir, "Pyramid-160x144.png"))
        
        total_width = master_sheet.get_width()
        frame_width = total_width // 6
        total_height = master_sheet.get_height()
        frame_height = total_height // 5

        self.oneI_frames = []
        # The master sheet I have is very confusing so 4 rows x  6 cols plus 1 extra sprite 
        for row in range(5):
            for col in range(6):
                frame_x = col * frame_width
                frame_y = row * frame_height

                frame_rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
                frame_surface = master_sheet.subsurface(frame_rect)

                scaled_frame = pygame.transform.scale(frame_surface, (128,128))
                self.oneI_frames.append(scaled_frame)

        self.oneI_frames = self.oneI_frames[:25]

    def move(self, wizard, enemies):
        if not self.visible and self.is_dying:
            return 
        wizard_center_x = wizard.hit_box[0] + wizard.hit_box[2] // 2
        wizard_center_y = wizard.hit_box[1] + wizard.hit_box[3] // 2

        oneI_center_x = self.hit_box[0] + self.hit_box[2] // 2
        oneI_center_y = self.hit_box[1] + self.hit_box[3] // 2

        if self.visible: 
            if oneI_center_x - 10 < wizard_center_x:
                self.x += self.vel
            elif oneI_center_x - 10 > wizard_center_x:
                self.x -= self.vel

            if oneI_center_y - 10 < wizard_center_y:
                self.y += self.vel 
            elif oneI_center_y - 10 > wizard_center_y:
                self.y -= self.vel 


            self.handle_seperation(enemies, radius=50, push_strength=3)
        

    def draw(self, screen, wizard, offset_y, bar_width, enemies):
        self.move(wizard, enemies)
        if self.is_dying: 
            self.play_death_animation(screen)
            return
        if len(self.oneI_frames) > 0:
            frame_index = (self.walk_count // 6) % len(self.oneI_frames)
            current_frame = self.oneI_frames[frame_index]
            self.walk_count += 1
            screen.blit(current_frame, (self.x, self.y))

        pad_x = 24
        pad_y = 25
        hit_x = self.x + pad_x
        hit_y = self.y + pad_y
        hit_w = self.width - (2 * pad_x)
        hit_h = self.height - (2 * pad_y)
        self.hit_box = (hit_x, hit_y, hit_w, hit_h)

        super().draw(screen, offset_y, bar_width)


class keys_drop():
    def __init__(self):
        random_x =  random.randint(50,700)
        random_y = random.randint(50,700)
        self.rect = pygame.Rect(0, 0, 16, 16)
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

    def spawn(self, min_x = 150, max_x = 1050, min_y = 100, max_y = 600):
        self.rect.x = random.randint(min_x, max_x)
        self.rect.y = random.randint(min_y, max_y)
        self.visible = True 
        self.collected = False
    
    def draw(self, screen):
        if self.visible and not self.collected:
            
            self.current_frame += self.animated_speed
            if self.current_frame >= len(self.key_frames):
                self.current_frame = 0 

            active_sprite = self.key_frames[int(self.current_frame)]
            screen.blit(active_sprite, (self.rect.x, self.rect.y))


class chest():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, 96 , 96)
        self.visible = False
        self.collected = False 
        self.text_timer = 0

        self.current_frame = 0 
        self.animation_speed = 0.2

        #loading the assets for the chest
        chest_dir = os.path.join("src", "assets", "chest")
        chest_mastersheet = pygame.image.load(os.path.join(chest_dir, "chest_e.png"))
    
        frame_width = chest_mastersheet.get_width() // 7
        frame_height = chest_mastersheet.get_height()

        self.chest_frames = [ pygame.transform.scale(
            chest_mastersheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)),
            (128,128)
        ) for i in range(7)
        ]

    def spawn(self, min_x = 150, max_x= 1050, min_y= 150, max_y=690):
        self.x = random.randint(min_x, max_x)
        self.y = random.randint(min_y, max_y)
        self.rect.topleft = (self.x, self.y)

        self.visible = True 
        self.collected = False
        self.is_opened = False
        self.current_frame = 0 


    def update(self):
        if self.is_opened:
            if self.current_frame < len(self.chest_frames) - 1:
                self.current_frame += self.animation_speed

            if self.current_frame > len(self.chest_frames) - 1:
                self.current_frame = len(self.chest_frames) - 1


    def draw(self, screen):
        if self.visible:
            frame_index = int(self.current_frame)
            screen.blit(self.chest_frames[frame_index], (self.x, self.y))


class hp_particles():
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.is_visible = False
        self.is_collected = False

        self.current_frame = 0.0
        self.animation_speed = 0.5

        self.spell_dir = os.path.join('src', 'assets', 'spells')
        self.heal_dir = os.path.join(self.spell_dir, "HealEffect", 'Frames')

        self.heal_frames = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.heal_dir, f"HealEffect_{i:02d}.png")).convert_alpha(),
            (96, 96)
        ) for i in range(16)
        ]

    def trigger(self, chest):
        self.x = chest.x + (chest.rect.width // 2) - (96 // 2) + 15
        self.y = chest.y + (chest.rect.height // 2) - (96 // 2) + 10

        self.rect.topleft = (self.x, self.y)
        self.current_frame = 0.0
        self.is_visible = True 


    def update(self):
        if self.is_visible:
            self.current_frame += self.animation_speed

            if self.current_frame >= len(self.heal_frames):
                self.current_frame = 0.0


    def draw(self, screen):
        if self.is_visible:
            frame_index = int(self.current_frame)
            screen.blit(self.heal_frames[frame_index], (self.x, self.y))
        