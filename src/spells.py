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
        self.max_radius = 80
        self.growth_speed = 20
        self.push_force = 12
        self.active = True

    def update(self, enemies):

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
            distance = (dx**2 + dy**2) ** 0.5

            if distance < self.radius:
                if distance == 0:
                    distance = 1

            push_y = dx/ distance
            push_x = dy/ distance

            enemy.x += push_x * self.push_force
            enemy.y += push_y * self.push_force 

    def draw(self, screen):
        if self.active:

            diameter = int(self.radius * 2)
            surface_layer = pygame.Surface((diameter, diameter), pygame.SRCAPLHA)

            center_on_layer = (int(self.radius), int(self.radius))
            pygame.draw.circle(surface_layer, (0,191, 255, 128), center_on_layer, int(self.radius))

            screen.blit(surface_layer, (int(self.x_pos - self.radius), int(self.y_pos - self.radius)))