import pygame

pygame.init()


window = pygame.display.set_mode((800,800))
pygame.display.set_caption("Learning phase1")


px = 50
py = 50
width = 100
height = 100
vel = 5


clock = pygame.time.Clock()

run = True

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and px > 0:
        px -= vel
    if keys[pygame.K_RIGHT] and px < 800 - width:
        px += vel
    if keys[pygame.K_UP] and py > 0:
        py -= vel
    if keys[pygame.K_DOWN] and py < 800 - height:
        py += vel


    window.fill('Black')
    pygame.draw.rect(window, (255, 0, 0), (px, py, width, height))
    pygame.display.update()

    clock.tick(60)



pygame.quit()


