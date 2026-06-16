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