import os
import pygame

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
        self.push_force = 15
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
            distance = (dist_x**2 + dist_y**2)**0.5

            if distance <= self.radius and distance > 0:
                push_force = 15
            #This prevents the push in one sngluar direction (every time); to making it some what dynamic
                if self.facing == "left":
                    enemy.x -= push_force
                elif self.facing == "right":
                    enemy.x += push_force
                elif self.facing == "upwards":
                    enemy.y -= push_force
                elif self.facing == "downwards":
                    enemy.y += push_force


           
                
    def draw(self, screen):
        if self.active:

            frame_index = (self.walk_count // 1) % len(self.repel_frames)
            current_frame = self.repel_frames[frame_index]
            self.walk_count += 1

            diameter = int(self.radius * 2)
            scaled_frame = pygame.transform.scale(current_frame, (diameter,diameter))

            screen.blit(scaled_frame, (int(self.x_pos - self.radius), int(self.y_pos - self.radius)))


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
