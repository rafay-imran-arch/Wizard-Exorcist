import pygame


screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Practicing projectiles")
clock = pygame.time.Clock()


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
    for laser in lasers:
        laser.draw(screen)
    
    pygame.display.update()
    clock.tick(30)


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