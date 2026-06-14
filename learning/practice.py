import pygame

pygame.init()


window = pygame.display.set_mode((800,800))
pygame.display.set_caption('Learning practice')
clock = pygame.time.Clock()



#character 
px = 50
py = 50
width = 100
height = 100
vel = 5

isJump = False
jumpcount = 10 



run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        px -= vel
    if keys[pygame.K_RIGHT]:
        px += vel

    if not(isJump):
        if keys[pygame.K_UP]:
            py -= vel
        if keys[pygame.K_DOWN]:
            py += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpcount >= -10:
            neg = 1
            if jumpcount < 0:
                neg = -1
            py -= (jumpcount ** 2) * 0.5 * neg
            jumpcount -= 1  
        else:
            isJump = False
            jumpcount = 10

    window.fill('Black')
    pygame.draw.rect(window, (255, 0, 0), (px, py, width, height))    
    pygame.display.update()
    clock.tick(60)
pygame.quit()


