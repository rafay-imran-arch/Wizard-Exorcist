import pygame
import os 
from sprites import player
pygame.init()

# Some essentials
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("First Draft WE")
clock = pygame.time.Clock()
score = 0

    
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
        self.vel = 1.5
        self.hit_box = (self.x + 20, self.y, 90,128)
        self.health = 10
        self.visible = True    


        self.enemy_dir = os.path.join('src', 'assets', 'creatures','Ghost')
        master_sheet = pygame.image.load(os.path.join(self.enemy_dir, '128ghost.png')).convert_alpha()
        frame_width = 256
        frame_height = 256 

        self.ghost_frames = []

        for i in range(4):
            frame_box = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            sliced_frame = master_sheet.subsurface(frame_box)

            final_sprite = pygame.transform.scale(sliced_frame, (128,128))
            self.ghost_frames.append(final_sprite)

        self.ghost = self.ghost_frames[0]

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 24:
                self.walk_count = 0
        
            current_frame = self.ghost_frames[self.walk_count // 6]
            screen.blit(current_frame, (self.x, self.y))

            self.walk_count += 1
            pygame.draw.rect(screen, (255,123,140), (self.hit_box[0], self.hit_box[1] - 20, 50, 10))
            pygame.draw.rect(screen, (128,255,200), (self.hit_box[0], self.hit_box[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))

            self.hit_box = (self.x + 20, self.y, 90, 128)
            pygame.draw.rect(screen, (255,0,0), self.hit_box, 2)
    def move(self):
        if self.visible:
            if self.x < wizard.x_pos:
                self.x += self.vel
            elif self.x > wizard.x_pos:
                self.x -= self.vel
            
            if self.y < wizard.y_pos:
                self.y += self.vel
            elif self.y > wizard.y_pos:
                self.y -= self.vel

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
    wizard.draw(screen)
    for spell in spells:
        spell.draw(screen)

    pygame.draw.rect(screen, (255,0,0), (20, 360, 100, 30))
    pygame.draw.rect(screen, (0,255,0), (wizard.hit_box[0], wizard.hit_box[1] - 10, 80 - ((80/10)*(10- wizard.health)), 10))
    health = font.render(f"Health", 1, (0,0,0))
    screen.blit(health,(40,360))
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
spell_limit = 5
spells = []
run = True
shoot_loop = 0
player_hit_cooldown = 0


#Main loop
while run:

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0

    if player_hit_cooldown > 0:
        player_hit_cooldown -= 1

    #check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # Keeps your index style, but fixes the lower boundary check math
    if wizard.hit_box[1] < spooky.hit_box[1] + spooky.hit_box[3] and wizard.hit_box[1] + wizard.hit_box[3] > spooky.hit_box[1]:
        if wizard.hit_box[0] + wizard.hit_box[2] > spooky.hit_box[0] and wizard.hit_box[0] < spooky.hit_box[0] + spooky.hit_box[2]:
            if spooky.visible:
                if player_hit_cooldown == 0:  # Only hit if the ghost is alive
                    spell_shoot_sound.play()
                    wizard.hit()
                    score -= 2
                    player_hit_cooldown = 30

    # Safe array slice method [:] stops skipping logic loops when popping offscreen objects
    # Added 'break' statements after your pops so it stops looking at deleted items
    for spell in spells:
        if spooky.visible and spell.y_pos < spooky.hit_box[1] + spooky.hit_box[3] and spell.y_pos > spooky.hit_box[1]:
            if spell.x_pos > spooky.hit_box[0] and spell.x_pos < spooky.hit_box[0] + spooky.hit_box[2]:
                if spooky.visible:
                    spooky.hit()
                    wizard.mana -= 1
                    score += 1
                    spells.pop(spells.index(spell))
                    break  # <--- Stops processing this spell instantly

                 
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
            break  # <--- Stops processing this spell instantly
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
        if wizard.mana > 0 and len(spells) < spell_limit:
            wizard.mana -= 1
            spell_sound.play()
            spells.append(spells_shoot(round(wizard.x_pos + wizard.width//2), round(wizard.y_pos + wizard.height//2), wizard.facing))
        shoot_loop = 1
    render_game()

pygame.quit()


