import pygame
import os 

pygame.init()

# Some essentials
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("First Draft WE")
clock = pygame.time.Clock()
score = 0

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
        self.mana = 10
        self.health = 10 
        self.halth = "I need to make the health lose once the character hit box is = to the ghost hitbox woeking on that tomorrow"
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

        pygame.draw.rect(screen, (255,128,240), (self.hit_box[0], self.hit_box[1] - 20, 80, 10))
        pygame.draw.rect(screen, (128,255,210), (self.hit_box[0], self.hit_box[1] - 20, 80 - ((80/10) * (10 - self.mana)), 10))
        pygame.draw.rect(screen, (255,0,0), (self.hit_box[0], self.hit_box[1] - 10, 80, 10))
        pygame.draw.rect(screen, (0,255,0), (self.hit_box[0], self.hit_box[1] - 10, 80 - ((80/10)*(10- self.health)), 10))

    def hit(self):
        if self.health > 0:
            self.health -= 1
            self.walk_count = 0
            pygame.display.update()
        elif self.health == 0:
            spell_shoot_sound.play()

    
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
        self.health = 10
        self.visible = True    


        self.enemy_dir = os.path.join('src', 'assets', 'creatures')
        self.ghost = pygame.transform.scale(
            pygame.image.load(os.path.join(self.enemy_dir, 'enemy.png')),
            (128,128)
        )

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walk_count + 1 < 44:
                self.walk_count = 0
            
            screen.blit(self.ghost, (self.x, self.y))
            self.walk_count += 1
            pygame.draw.rect(screen, (255,123,140), (self.hit_box[0], self.hit_box[1] - 20, 50, 10))
            pygame.draw.rect(screen, (128,255,200), (self.hit_box[0], self.hit_box[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))

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

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class spells_shoot():
    
    def __init__(self, x_pos, y_pos, facing):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.facing = facing
        self.vel = 8

        self.spell_dir = os.path.join("src", 'assets', 'spells')
        self.blue_spell = pygame.transform.scale(
            pygame.image.load(os.path.join(self.spell_dir, 'spell_1.png')),
            (64,64)
        )
    def draw(self, screen):
        screen.blit(self.blue_spell, (self.x_pos,self.y_pos))


class revive():
    
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.vel = 2
        self.text = "You have used one health spell"
        self.health_spell_count = 10

    def draw(self, screen):
        pass 

    def hit(self):
        pass

class spell_book():

    def __init__(self, x_pos, y_pos, pointer, cell, row):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.pointer = pointer
        self.cell = cell
        self.row = row

        self.graphics = "This thing is yet to be decided as I plan to make something of a gui thing the player can open this up mid commbat " \
        "then select its spells I will possible give 3 spells to players at most but for the starting levels he can only use one spell" \
        "then I will decide on the world building on how he gets the book to use other spells or rather learn other spells after deffeating some enemies" \
        "hmm maybe i want to keep that for the mana regeneration thing or something lets see what I'll do" \
        "If i really really think hard enought i can add secret chests per room in the castle which appears only once you defeat the enemies" \
        "after you defeat the enemies in that room the box appears with the scroll of spell which the wizards book absorbs automatically hmmm" \
        "some animation effect ? or something I'll have to work on this maybe leave this for part 2 I suppose ? " \
        "these are some insane ideas I hope I am able to complete these" \
        "also i need to incorportate the system of room lock once the player moves in a room he gets locked in until he defeaths the enemies" \
        "and then after all enemies die the doors open? like the binding of issac stuff I think i suppose" \
        "plus what else can I add in this ? I can also incorporte the system of boss fights to make hi mana stronger ? but how many levels do I " \
        "intend to make for this installment? IDK yet but these are some good ideas and I hope I am able to work on these." \
        "I also need the enemies to attack the player with some kind of attack? also follow the player around rather that in one straight plane" \
        "or something" \
        "i really need to so something about this stuff I need to learn ore and more and more" \
        "May i be able to finish this game"
        

#function to make things appear (magically!?)
def render_game():
    screen.fill("Grey")
    text = font.render(f'Score: {score}', 1, (255,0,0))
    game_name = font.render(f"Weclome to Wizard Excorcist: Redemption of the fallen castle", 1, (128,100,255))
    screen.blit(game_name,(70, 20))
    screen.blit(text, (670, 20))
    spooky.draw(screen)
    spooky2.draw(screen)
    wizard.draw(screen)
    for spell in spells:
        spell.draw(screen)
    pygame.display.update()
    clock.tick(30)



sound_dir = os.path.join('src','assets', 'sounds')
recharge_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'recharge.mp3'))
spell_shoot_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'spellshoot.mp3'))
spell_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'spell.mp3'))
game_music = pygame.mixer.music.load(os.path.join(sound_dir, "bg.mp3"))
pygame.mixer.music.play(-1)

font = pygame.font.SysFont('comicsans', 30, True)
spooky = enemy(100,200,64,64,200)
spell_limit = 2
spells = []
run = True
shoot_loop = 0
spooky2 = enemy(200,100,64,64,600)
#Main loop
while run:

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0


    #check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    if wizard.hit_box[1] < spooky.hit_box[1] + spooky.hit_box[3] and wizard.hit_box[3] > spooky.hit_box[1]:
        if wizard.hit_box[0] + wizard.hit_box[2] > spooky.hit_box[0] and wizard.hit_box[0] < spooky.hit_box[0] + spooky.hit_box[2]:
            spell_shoot_sound.play()
            wizard.hit()
            score -= 2

    # Safe array slice method [:] stops skipping logic loops when popping offscreen objects
    for spell in spells:
        if spell.y_pos < spooky.hit_box[1] + spooky.hit_box[3] and spell.y_pos > spooky.hit_box[1]:
            if spell.x_pos > spooky.hit_box[0] and spell.x_pos < spooky.hit_box[0] + spooky.hit_box[2]:
                spooky.hit()
                wizard.mana -= 1
                score += 1
                spells.pop(spells.index(spell))

        if spell.y_pos < spooky2.hit_box[1] + spooky2.hit_box[3] and spell.y_pos > spooky2.hit_box[1]:
            if spell.x_pos > spooky2.hit_box[0] and spell.x_pos < spooky2.hit_box[0] + spooky2.hit_box[2]:
                spooky2.hit()
                spells.pop(spells.index(spell))
                 
        if (spell.x_pos < 800 and spell.x_pos > 0) and (spell.y_pos < 400 and spell.y_pos > 0):
        
            if spell.facing == "right":
                spell.x_pos += spell.vel
            elif spell.facing == "left":
                spell.x_pos -= spell.vel
            elif spell.facing == "upwards":
                spell.y_pos -= spell.vel
            elif spell.facing == 'downwards':
                spell.y_pos += spell.vel
        else: 
            spells.pop(spells.index(spell))

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
    
    if keys[pygame.K_COMMA]:
        recharge_sound.play()
        if wizard.mana < 10:
            wizard.mana += 1
    
    if keys[pygame.K_SPACE] and shoot_loop == 0:
        if len(spells) < spell_limit:
            spell_sound.play()
            spells.append(spells_shoot(round(wizard.x_pos + wizard.width//2), round(wizard.y_pos + wizard.height//2), wizard.facing))
        shoot_loop = 1
    render_game()

pygame.quit()


