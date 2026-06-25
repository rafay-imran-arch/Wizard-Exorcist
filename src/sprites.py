# script for my sprites 
import pygame
import os





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
       