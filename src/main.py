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
        self.hit_box = (self.x_pos + 10, self.y_pos, 100, 128)

        # For rendering animation cycles and the sprite 
        self.walk_dir = os.path.join('src','assets','wizards','Char 1','Type 1','Run')
        self.character_size = (128,128)
        
        # Initialize the rect immediately so K_SPACE doesn't crash on frame 1
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.character_size[0], self.character_size[1])

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
        # Update rect position alongside position changes
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

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
        self.hit_box = (self.x_pos + 10, self.y_pos, 100, 128)
        pygame.draw.rect(screen, (0,255,0), self.hit_box,2)

#making an player object i.e the magical wizard
wizard = player(400,200,64,64)
wizard2 = player(300,100,64,64)

class enemy():

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end  
        self.path = (self.x, self.end)
        self.walk_count = 0
        self.vel = 3
        self.hit_box = (self.x + 20, self.y, 90,128)
        
        self.enemy_dir = os.path.join('src', 'assets', 'creatures')
        self.ghost = pygame.transform.scale(
            pygame.image.load(os.path.join(self.enemy_dir, 'enemy.png')),
            (128,128)
        )

    def draw(self, screen):
        self.move()
        if self.walk_count + 1 < 44:
            self.walk_count = 0
        
        screen.blit(self.ghost, (self.x, self.y))
        self.walk_count += 1
        self.hit_box = (self.x + 20, self.y, 90, 128)
        pygame.draw.rect(screen, (255,0,0), self.hit_box, 2)
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0


class spell_1():  
    
    def __init__(self, spawn_center, width, height, facing):
        self.width = width
        self.height = height
        self.facing = facing 
        self.vel = 8


        self.spell_dir = os.path.join('src', 'assets', 'spells')
        self.spell_1 = pygame.transform.scale(
            pygame.image.load(os.path.join(self.spell_dir, 'spell_1.png')),
            (self.width, self.height)
        )    

        # Set up standard Pygame center alignment
        self.rect = self.spell_1.get_rect()
        self.rect.center = spawn_center
        # Store positions safely as decimals/floats for consistency
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)

    def draw_spell(self, screen):
        # Sync updates back to the actual drawing rectangle coordinates
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)
        screen.blit(self.spell_1, (self.rect.x, self.rect.y))


#function to make things appear (magically!?)
def render_game():
    screen.fill("Grey")
    spooky.draw(screen)
    wizard.draw(screen)
    for spell in spells:
        spell.draw_spell(screen)
    pygame.display.update()
    clock.tick(30)

spooky = enemy(100,200,64,64,200)
spell_limit = 2
spells = []
run = True

#Main loop 
while run:

    #check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Safe array slice method [:] stops skipping logic loops when popping offscreen objects
    for spell in spells[:]:
        if (spell.x_pos < 800 and spell.x_pos > -64) and (spell.y_pos < 400 and spell.y_pos > -64):
            if spell.facing == 'upwards':
                spell.y_pos -= spell.vel
            elif spell.facing == 'downwards':
                spell.y_pos += spell.vel
            elif spell.facing == 'right':
                spell.x_pos += spell.vel
            elif spell.facing == 'left':
                spell.x_pos -= spell.vel
        else:
            spells.remove(spell)

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
    
    if keys[pygame.K_SPACE]:
        if len(spells) < spell_limit:
            spells.append(spell_1(wizard.rect.center, 64, 64, wizard.facing))

    render_game()

pygame.quit()