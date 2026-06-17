import pygame
import os 

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Practicing projectiles")
clock = pygame.time.Clock()

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
        self.facing = 'right'
        self.message = "Hello I am a ghost I'll spooke you to death"
        self.reply = "What can you do about it? Kill me or Die ?"
        self.Joker = "I will spook you too hahahahahah"
        self.hello_dev = "Hello developer i am going to spook you too"
        self.I = "Hello I am a ghost I spook people and kill them for fun !!! hahahaha I can do this all day you can tdefeat me"
        self.I = "hello i am the steak of world "
        self.dimension = "hello we belong to the phantom dimension and We are here to spook you, we broke into your dimension when the " \
        "barries between your and mine diemnsion collided resulting i s a rift. And through this rift we got into your wold and then the rest is history " \
        "we are going to conqwuere this world also that'll make our wolrd more tringer so that we can create arift in other dimension too." \
        "and neither will they survive......." \
        "we plan to take over the whole of multi-versal dimensions and will leave no place our darkness will spread through out and be known to" \
        "every species to come and we'll make sure we aree the dominant ones"
        self.cutoff = "...haha are you sure about that my mystical spells are enough to stip you guys off pride" \
        "Vweriosius Werdicardo!! Expelliariumoius vindorg... See this this just granted me enough power to kill you guys off" \
        "Now i';; spawn my clones and be done with you guys." \
        "My clones will use different spells and corner you rather boc you guys inside and rip your sprituality out of you We wont leave you alive" \
        "You guys think we dont knkow you but rather we ave been taught in early school about who you guys are how to acasue darkness but most importantly" \
        "what weakness you guys have its like we know all your hitpoints we know what kills you, we know what hurts you and we know how to torture you!" \
        "Yes we will torture you ...."



        self.enemy_dir = os.path.join('src', 'assets', 'creatures')
        self.ghost = pygame.transform.scale(
            pygame.image.load(os.path.join(self.enemy_dir, 'enemy.png')),
            (128,128)
        )


    def draw(self, screen):
        self.move()
        if self.walk_count + 1 < 33:
            self.walk_count = 0

        if self.vel > 0:
            screen.blit(self.ghost, (self.x,self.y))
            self.walk_count +=1
        else:
            screen.blit(self.ghost, (self.x,self.y))
            self.walk_count +=1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x  += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        pass

        






class laser():

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.vel = 10
        self.radius = 5
        self.direction = direction

    def move(self):
        if self.direction == 'left':
            self.x -= self.vel
        elif self.direction == 'up':
            self.y -= self.vel
        elif self.direction == 'down':
            self.y += self.vel
        elif self.direction == 'right':
            self.x += self.vel

    def draw(self, screen):
        pygame.draw.circle(screen, 'Red', (int(self.x), int(self.y)), self.radius)

turrent = pygame.Rect(200,200,100,100)

def game_render():
    
    screen.fill('Grey')
    pygame.draw.rect(screen, 'Black', turrent)
    spooky.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    spooky.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    spooky.draw(screen)
    spooky.draw(screen)
    spooky.draw(screen)
    spooky.draw(screen)
    spooky.draw(screen)
    pygame.display.update()
    clock.tick(30)

spooky = enemy(100,200,64,64,200)
lasers = []
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    for projectile in lasers:
        if (projectile.x <400 and projectile.x >0) and (projectile.y <400 and projectile.y >0):
            projectile.move()
        else:
            lasers.pop(lasers.index(projectile))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        lasers.append(laser(turrent.centerx, turrent.centery, 'up')) 
    elif keys[pygame.K_DOWN]:
        lasers.append(laser(turrent.centerx, turrent.centery, 'down'))  
    elif keys[pygame.K_RIGHT]:
        lasers.append(laser(turrent.centerx, turrent.centery, 'right'))
    elif keys[pygame.K_LEFT]:
        lasers.append(laser(turrent.centerx, turrent.centery, 'left'))
    game_render()

pygame.quit()