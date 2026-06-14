import pygame
import os 



pygame.init()


window = pygame.display.set_mode((800,800))
pygame.display.set_caption('Learning practice')
clock = pygame.time.Clock()


walk_dir = os.path.join('src', 'assets', 'wizards', 'Char 1', 'Type 1', 'Run')

character_size = (64,64)

wizard = pygame.transform.scale(
    pygame.image.load(os.path.join(walk_dir, 'RunUP_1.png')),
    character_size
)

walk0 = pygame.image.load(os.path.join(walk_dir, 'Run_0.png'))
walk1 = pygame.image.load(os.path.join(walk_dir, 'Run_1.png'))
walk2 = pygame.image.load(os.path.join(walk_dir, 'Run_2.png'))
walk3 = pygame.image.load(os.path.join(walk_dir, 'Run_3.png'))

walk_right = [
    pygame.transform.scale(walk0, character_size),
    pygame.transform.scale(walk1, character_size),
    pygame.transform.scale(walk2, character_size),
    pygame.transform.scale(walk3, character_size),
]

walk_left = [
    pygame.transform.flip(walk_right[0], True, False),
    pygame.transform.flip(walk_right[1], True, False),
    pygame.transform.flip(walk_right[2], True, False),
    pygame.transform.flip(walk_right[3], True, False)
]

#character 
px = 200
py = 400
width = 128
height = 128
vel = 5

going_right = False
going_left = False
walk_count = 0

isJump = False
jumpcount = 10 



def game_render():
    global walk_count
    window.fill('Black')
    if walk_count + 1 >=24:
        walk_count = 0

    if going_right:
        window.blit(walk_right[walk_count//6], (px,py))
        walk_count += 1
    elif going_left:
        window.blit(walk_left[walk_count//6], (px,py))
        walk_count += 1
    else: 
        window.blit(wizard, (px,py))


    pygame.display.update()
    clock.tick(30)


run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        px -= vel
        going_left = True
        going_right = False
    elif keys[pygame.K_RIGHT]:
        px += vel
        going_right = True
        going_left = False
    else:
        going_left = False
        going_right = False
        walk_count = 0

    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
            going_left = False
            going_right = False
            walk_count = 0

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

    game_render()


pygame.quit()


