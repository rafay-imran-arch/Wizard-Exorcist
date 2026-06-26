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

