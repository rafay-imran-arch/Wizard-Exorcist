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
        

class projectile_spell(spells):
    def __init__(self,x_pos ,y_pos, facing):
        super().__init__(x_pos,y_pos,facing)

        #loading the shooting spell asset
        self.shoot_spell_dir = os.path.join(self.spell_dir, 'SlowEffect', 'Frames')
        self.shoot_spell = pygame.transform.scale(
            pygame.image.load(os.path.join(self.shoot_spell_dir, 'SlowEffect_00.png')),
            (64,64)
        )

    def draw(self, screen):
        screen.blit(self.shoot_spell, (self.x_pos,self.y_pos))

class repel_spell(spells):
    def __init__(self, x_pos, y_pos, facing):
        super().__init__(x_pos, y_pos, facing)

        self.radius = 10
        self.max_radius = 150
        self.growth_speed = 15
        self.push_force = 60
        self.active = True
        self.walk_count = 0

        self.repel_dir = os.path.join(self.effect_dir, 'Impacts', 'symmetrical_impact_002', 'symmetrical_impact_002_small_blue')
        self.repel_frames = [
            pygame.image.load(os.path.join(self.repel_dir, f"frame{i:04}.png")).convert_alpha()
            for i in range(10)
        ]

    def update(self, enemies):
        import math

        self.radius += self.growth_speed
        if self.radius >= self.max_radius:
            self.active = False
        
        for enemy in enemies:
            if not enemy.visible: 
                continue

            enemy_center_x = enemy.hit_box[0] + enemy.hit_box[2] // 2
            enemy_center_y = enemy.hit_box[1] + enemy.hit_box[3] // 2

            dx = enemy_center_x - self.x_pos
            dy = enemy_center_y - self.y_pos 
            distance = math.hypot(dx, dy)

            repel_range = 150

            if distance < repel_range and distance > 0:
            
                push_y = dx/ distance
                push_x = dy/ distance

                

                enemy.x += push_x * self.push_force
                enemy.y += push_y * self.push_force 

    def draw(self, screen):
        if self.active:

            frame_index = (self.walk_count // 1) % len(self.repel_frames)
            current_frame = self.repel_frames[frame_index]
            self.walk_count += 1

            diameter = int(self.radius * 2)
            scaled_frame = pygame.transform.scale(current_frame, (diameter,diameter))

            screen.blit(scaled_frame, (int(self.x_pos - self.radius), int(self.y_pos - self.radius)))

