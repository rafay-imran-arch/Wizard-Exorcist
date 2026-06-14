import pygame
import os 

pygame.init()


# Some essentials
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("First Draft WE")
clock = pygame.time.Clock()


#Creating a class for wizard/player 
class player(object):

    #player's attributes
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.vel = 5
        self.isjump = False
        self.walk_count = 0
        self.facing = "downwards"
        self.is_moving = False

        # For rendering animation cycles and the sprite 
        self.walk_dir = os.path.join('src','assets','wizards','Char 1','Type 1','Run')
        self.character_size = (64,64)

        #idle sprite for all positions
        self.idle = os.path.join('src', 'assets', 'wizards', 'Char 1', 'Type 1', 'Attack')

        #Idle up
        self.idle_up = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle, 'atk_1.png')),
            self.character_size
        )
        #idle right 
        self.idle_right = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle, 'atk_2.png')),
            self.character_size
        )
        #idle down
        self.idle_down = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle, 'atk_3.png')),
            self.character_size
        )
        #idle left
        self.idle_left = pygame.transform.scale(
            pygame.image.load(os.path.join(self.idle, 'atk_4.png')),
            self.character_size
        )


        #walk right cycle list 
        self.walk_right = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.walk_dir, f"Run_{i}.png")),
                self.character_size
            ) for i in range(4)
        ]

        #walk left cycle list
        self.walk_left = [
            pygame.transform.flip(sprite, True, False) for sprite in self.walk_right
        ]

        #walk up cycle list
        self.walk_up = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.walk_dir, f"RunUP_{i}.png")),
                self.character_size
            ) for i in range(4)
        ]

        self.walk_down = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.walk_dir, f"RunDW_{i}.png")),
                self.character_size
            ) for i in range(4)
        ]

    #defining a draw function so you can see how insane you look
    def draw(self, screen):

        if self.walk_count + 1 >= 24:
            self.walk_count = 0


        if not self.is_moving:
            if self.facing == "right":
                screen.blit(self.idle_right, (self.x_pos,self.y_pos))
            elif self.facing == "left":
                screen.blit(self.idle_left, (self.x_pos,self.y_pos))
            elif self.facing == "upwards":
                screen.blit(self.idle_up, (self.x_pos,self.y_pos))
            elif self.facing == "downwards":
                screen.blit(self.idle_down, (self.x_pos,self.y_pos))
            self.walk_count = 0
        else:
            if self.facing == "right":
                screen.blit(self.walk_right[self.walk_count // 6], (self.x_pos,self.y_pos))
                self.walk_count += 1
            elif self.facing == "left":
                screen.blit(self.walk_left[self.walk_count // 6], (self.x_pos,self.y_pos))
                self.walk_count += 1
            elif self.facing == "upwards":
                screen.blit(self.walk_up[self.walk_count // 6], (self.x_pos,self.y_pos))
                self.walk_count += 1
            elif self.facing == "downwards":
                screen.blit(self.walk_down[self.walk_count // 6], (self.x_pos,self.y_pos))
                self.walk_count += 1

#making an player object i.e the magical wizard

wizard = player(400,200,64,64)


#function to make things appear (magically!?)
def render_game():
    screen.fill("Black")
    wizard.draw(screen)
    #Setting frame rate
    pygame.display.update()
    clock.tick(30)


run = True

#Main loop 
while run:

    #check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #check key presses for controls 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        wizard.x_pos -= wizard.vel
        wizard.facing = "left"
        wizard.is_moving = True

    elif keys[pygame.K_RIGHT]:
        wizard.x_pos += wizard.vel
        wizard.facing = "right"
        wizard.is_moving = True
    elif keys[pygame.K_UP]:
        wizard.y_pos -= wizard.vel
        wizard.facing = "upwards"
        wizard.is_moving = True
    elif keys[pygame.K_DOWN]:
        wizard.y_pos += wizard.vel
        wizard.facing = "downwards"
        wizard.is_moving = True
    else:
        wizard.is_moving = False

    render_game()

#To close the game
pygame.quit()