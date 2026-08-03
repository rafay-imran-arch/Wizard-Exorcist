import os
import pygame
import math 
import random

pygame.init()

class spells():

    def __init__(self,x_pos, y_pos, facing):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.facing = facing
        self.vel = 7

        #loading spell assets dir 
        self.spell_dir = os.path.join('src', 'assets','spells')
        self.effect_dir = os.path.join('src', 'assets', 'effects', 'eff', 'PNG')
        
#The projectile spell
class projectile_spell(spells):
    def __init__(self,x_pos ,y_pos, facing):
        super().__init__(x_pos, y_pos, facing)

        #loading the shooting spell asset
        self.shoot_spell_dir = os.path.join(self.spell_dir, 'SlowEffect', 'Frames')
        self.shoot_spell = pygame.transform.scale(
            pygame.image.load(os.path.join(self.shoot_spell_dir, 'SlowEffect_00.png')),
            (64,64)
        )

    def draw(self, screen):
        screen.blit(self.shoot_spell, (self.x_pos,self.y_pos))
    

#Spell number 2 the repelent spell
class repel_spell(spells):
    def __init__(self, x_pos, y_pos, facing):
        super().__init__(x_pos, y_pos, facing)

        self.radius = 10
        self.max_radius = 200
        self.growth_speed = 9
        self.push_force = 35
        self.active = True
        self.walk_count = 0

        self.repel_dir = os.path.join(self.effect_dir, 'Impacts', 'symmetrical_impact_002', 'symmetrical_impact_002_small_blue')
        self.repel_frames = [
            pygame.image.load(os.path.join(self.repel_dir, f"frame{i:04}.png")).convert_alpha()
            for i in range(10)
        ]

    def update(self, enemies): 
        if self.active: 
            self.radius += self.growth_speed
            if self.radius >= self.max_radius:
                self.active = False
                return
        
        for enemy in enemies:
            if not enemy.visible:
                continue
            dist_x = enemy.x - self.x_pos
            dist_y = enemy.y - self.y_pos
            distance = (dist_x**2 + dist_y**2) ** 0.5

            if distance <= self.radius and distance > 0:
                push_force = 15

                dir_x = dist_x / distance
                dir_y = dist_y / distance 

                enemy.x += dir_x * push_force
                enemy.y += dir_y * push_force 
                
    def draw(self, screen):
        if self.active:

            frame_index = (self.walk_count // 1) % len(self.repel_frames)
            current_frame = self.repel_frames[frame_index]
            self.walk_count += 1

            diameter = int(self.radius * 2)
            scaled_frame = pygame.transform.scale(current_frame, (diameter,diameter))

            screen.blit(scaled_frame, (int(self.x_pos - self.radius), int(self.y_pos - self.radius)))

class mana_charge(spells):
    def __init__(self, x, y, width=128, height=128):
        super().__init__(x, y, None)
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.active = True

        self.x = x - (self.width // 4)
        self.y = y - (self.height // 4)

        self.charge_animation_count = 0
        self.charge_dir = os.path.join(self.effect_dir, "Impacts", "symmetrical_impact_002", "symmetrical_impact_002_large_blue")

        self.charge_frames = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.charge_dir, f"frame{i:04}.png")),
            (128,128)
        ) for i in range(4,9)
        ]

    def update(self, wizard):
        self.x = wizard.x_pos + (wizard.width // 2) - (self.width // 2)
        self.y = wizard.y_pos + (wizard.height // 2) - (self.height // 2)
    def draw(self, screen):

        if not self.active:
            return

        frame_index = (self.charge_animation_count // 2)
        if frame_index >= len(self.charge_frames):
            self.active = False
            return
        current_frame = self.charge_frames[frame_index]
        self.charge_animation_count += 1
        screen.blit(current_frame, (self.x + 37 , self.y + 40))

class enemy_projectile_bat(spells):
    def __init__(self, x_pos, y_pos, facing):
        super().__init__(x_pos, y_pos, facing)
        self.vel = 5
        self.active = True
        self.walkcount = 0

        self.bat_spit_dir = os.path.join(self.spell_dir, "BurnEffect", "Frames")
        self.bat_spit_frames = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.bat_spit_dir,f"BurnEffect_{i:02}.png")).convert_alpha(),
            (96,96))
            for i in range(16)
        ]

    def update(self):
        if self.facing == "left":
            self.x_pos -= self.vel
        elif self.facing == "right":
            self.x_pos += self.vel
        elif self.facing == "upwards":
            self.y_pos -= self.vel
        elif self.facing == "downwards":
            self.y_pos += self.vel

    def draw(self, screen):
        if self.active:
            
            frame_index = (self.walkcount // 4) % len(self.bat_spit_frames)
            current_index = self.bat_spit_frames[frame_index]
            self.walkcount += 1
            screen.blit(current_index, (self.x_pos, self.y_pos))


class oneI_spell(spells):
    def __init__(self,x_pos , y_pos, facing):
        super().__init__(x_pos, y_pos, facing)
        self.vel = 6
        self.active = True  
        self.walkcount = 0
        #oneI spell asset loading
        self.oneI_shoot_dir = os.path.join(self.effect_dir, "Magic Bursts", "round_light_burst_001", "round_light_burst_001_small_yellow")
        self.oneI_shoot_frames = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.oneI_shoot_dir, f"frame{i:04}.png")),
            (64,64)
        ) for i in range(9)
        ]

    def update(self):
        if self.facing == "left":
            self.x_pos -= self.vel
        elif self.facing == "right":
            self.x_pos += self.vel
        elif self.facing == "upwards":
            self.y_pos -= self.vel 
        else:
            self.y_pos += self.vel

    def draw(self, screen):
        if self.active:
            
            frame_index = (self.walkcount // 2) % len(self.oneI_shoot_frames)
            current_frame = self.oneI_shoot_frames[frame_index]
            self.walkcount += 1
            screen.blit(current_frame, (self.x_pos, self.y_pos))

class oneI_beam(spells):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = True
        self.track_speed = 6
        self.orientation = random.choice(['horizontal', 'vertical'])
        
        if self.orientation == 'horizontal':
            self.x = 0
            self.y = random.randint(50, screen_height - 50)
            self.rect = pygame.Rect(0, self.y, screen_width, 24)
        else:
            self.x = random.randint(50, screen_width -50)
            self.y = 0
            self.rect = pygame.Rect(self.x, 0, 24, screen_height)

        self.warning_timer = 20
        self.blast_timer = 200
        
    def update(self, wizard_rect, wizard, player_hit_cooldown, hurt_sound):
        
        
        wizard_center_x = wizard_rect.centerx
        wizard_center_y = wizard_rect.centery
        
        if self.orientation == "horizontal":
            target_y  = wizard_center_y - 12
            if abs(self.y - target_y) < self.track_speed:
                self.y = target_y
            elif self.y < target_y:
                self.y += self.track_speed
            elif self.y > target_y:
                self.y -= self.track_speed
            

            self.rect.y = self.y
        else:
            target_x = wizard_center_x - 12
            if abs (self.x -target_x) < self.track_speed:
                self.x = target_x
            elif self.x < target_x:
                self.x += self.track_speed
            elif self.x > target_x:
                self.x -= self.track_speed
            
            self.rect.x = self.x

        if self.warning_timer > 0:
            self.warning_timer -= 1
        elif self.blast_timer > 0:
            self.blast_timer -= 1
        
            
            if self.rect.colliderect(wizard_rect) and (player_hit_cooldown == 0):
                hurt_sound.play()
                wizard.hit(4)
                self.active = False
                return 30
            
            if self.blast_timer <= 0:
                self.active = False
        return 0 
    
    def draw(self, screen):
        if not self.active:
            return 
        
        if self.warning_timer > 0:
            if self.orientation == 'horizontal':
                pygame.draw.line(screen, (255,222,33), (0, self.rect.centery), (self.screen_width, self.rect.centery), 2)
            else:
                pygame.draw.line(screen, (255,255,197), (self.rect.centerx, 0), (self.rect.centerx, self.screen_height), 2)
        elif self.blast_timer > 0:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)
            if self.orientation == 'horizontal':
                pygame.draw.line(screen, (255,255,255), (0, self.rect.centery), (self.screen_width, self.rect.centery), 14)
            else:
                pygame.draw.line(screen, (255,255,255), (self.rect.centerx, 0), (self.rect.centerx, self.screen_height), 6)


class oneI_radial(spells):
    def __init__(self, x_pos, y_pos, angle):
        super().__init__(x_pos, y_pos, 'radial')
        self.vel = 5
        self.angle = angle 
        self.active = True 
        self.radius = 8

        self.dx = math.cos(self.angle) * self.vel
        self.dy = math.sin(self.angle) * self.vel 

    def update(self, screen_width, screen_height):
        
        self.x_pos += self.dx 
        self.y_pos += self.dy

        if (self.x_pos < -50 or self.x_pos > screen_width + 50 or
            self.y_pos < -50 or self.y_pos > screen_height +50):
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, (255,255,255), (int(self.x_pos), int(self.y_pos)), self.radius)
            pygame.draw.circle(screen, (255,255,143), (int(self.x_pos), int(self.y_pos)), self.radius - 3)

class oneI_radial_burst(spells):
    def __init__(self, x_pos, y_pos, num_shoots=8):
        super().__init__(x_pos, y_pos, "none")
        self.active = True
        self.num_shoots = num_shoots
        self.is_charging = True 
        self.charge_timer = 40
        self.walk_count = 0

        self.oneI_radial_dir = os.path.join(self.effect_dir, "Impacts", "symmetrical_impact_003", "symmetrical_impact_003_small_yellow")
        self.oneI_radial_frames = [ pygame.transform.scale(
            pygame.image.load(os.path.join(self.oneI_radial_dir, f"frame{i:04}.png")).convert_alpha(),
            (128,128)) for i in range(7)
        ]



        self.current_ring_radius = 5
        self.max_ring_radius = 60
        self.expansion_speed = 3
        self.has_burst = False

    def update(self, oneI_radial_blast, screen_width, screen_height, enemy_instance=None):
        if not self.active: 
            return  
    
        if self.is_charging:
            if enemy_instance: 
                enemy_instance.x = self.x_pos
                enemy_instance.y = self.y_pos

            self.charge_timer -= 1
            if self.charge_timer <= 0:
                self.is_charging = False
            return 



        if self.current_ring_radius < self.max_ring_radius:
            self.current_ring_radius += self.expansion_speed
        elif not self.has_burst:
            self.has_burst = True 

            for i in range(self.num_shoots):
                angle = (2 * math.pi / self.num_shoots) * i
                bullet = oneI_radial(self.x_pos, self.y_pos, angle)
                oneI_radial_blast.append(bullet)
            
            self.active = False
    
    def draw(self, screen):
        if not self.active and self.has_burst:
            return
        
        if self.is_charging:
            frame_index = (self.walk_count // 2) % len(self.oneI_radial_frames)
            current_frame = self.oneI_radial_frames[frame_index]
            self.walk_count += 1

            screen.blit(current_frame, (int(self.x_pos-48) + 36, int(self.y_pos - 48) + 36))
            return 


        raw_intensity = int((self.current_ring_radius / self.max_ring_radius) * 255)
        color_intensity = max(0, min(255, raw_intensity))
        ring_color = (255, 238, color_intensity)

        pygame.draw.circle(
            screen, 
            ring_color,
            (int(self.x_pos),int(self.y_pos)),
            int(self.current_ring_radius),
            2
        )

        pygame.draw.circle(screen, (255,255,197), (int(self.x_pos), int(self.y_pos)), 4)