import pygame
import os 
from sprites import player, enemy, ghost, bat, slime, pumpkin, keys_drop, oneI
from spells import spells, projectile_spell, repel_spell, enemy_projectile_bat, oneI_spell, oneI_beam, oneI_radial_burst, oneI_radial
from dungeon import build_dungeon
from ui import slider, draw_pause_menu
pygame.init()


screen_width = 1280
screen_height = 720 
# Some essentials
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("First Draft WE")

clock = pygame.time.Clock()
score = 0

# game states
admin_mode = False
game_state = "MENU"
game_paused = False


start_screen_path = os.path.join("src","assets","ux","start_screen.png")
if os.path.exists(start_screen_path):
    start_screen_bg = pygame.image.load(start_screen_path).convert()
else:
    start_screen_bg = None

# start screen ui buttons 
play_button_rect = pygame.Rect(300,400,200,60)
exit_button_rect = pygame.Rect(300,470,200,60)
color_normal = (70, 50, 110)
color_hover = (128, 100, 255)



#All the door work
door_width = 80
door_depth = 20

north_door_rect = pygame.Rect((screen_width // 2) - (door_width // 2), 0, door_width, door_depth)
south_door_rect = pygame.Rect((screen_width // 2)- (door_width // 2), screen_height - door_depth, door_width, door_depth)
east_door_rect = pygame.Rect(screen_width - door_depth, (screen_height // 2) - (door_width // 2), door_depth, door_width)
west_door_rect = pygame.Rect(0, (screen_height // 2) - (door_width // 2), door_depth, door_width)
#making an player object i.e the magical wizard
wizard = player(400,200,64,64)



# likely for version 2
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


def all_regular_enemies_defeated(dungeon_dict):
    for room_key, room in dungeon_dict.items():
        if getattr(room, 'is_boss_room', False):
            continue    
        if len(room.enemies) > 0 or not room.cleared:
            return False
    return True

#function to make things appear (magically!?) 
def render_game(bat_projectiles):


    if os.path.exists(current_room.background_path):
        room_bg = pygame.image.load(current_room.background_path)
        screen.blit(room_bg, (0,0))
    else:
        screen.fill('Grey')
     
    if current_room.cleared and not room_key.visible:
        hidden = getattr(current_room, 'hidden_doors', [])
        if 'north' in current_room.connections and 'north' not in hidden:
            pygame.draw.rect(screen, (0,0,0), north_door_rect)
        if 'south' in current_room.connections and 'south' not in hidden:
            pygame.draw.rect(screen, (0,0,0), south_door_rect)
        if 'east' in current_room.connections and 'east' not in hidden:
            pygame.draw.rect(screen, (0,0,0), east_door_rect)
        if 'west' in current_room.connections and 'west' not in hidden:
            pygame.draw.rect(screen, (0,0,0), west_door_rect)
    

    if boss_locked_timer > 0:
        locked_msg = font.render("Boss Door Sealed! Clear all rooms first.", True, (255, 50, 50))
        screen.blit(locked_msg, (screen_width // 2 - locked_msg.get_width() // 2, 50))

    text = font.render(f'Score: {score}', 1, (255, 0, 0))
    screen.blit(text, (670, 20))
    wizard.draw(screen) # drawing wizard
    
    #drawing enemy
    for e in enemies:
        e.draw(screen,wizard, offset_y=20, bar_width=50, enemies=enemies)
    room_key.draw(screen)
    for spell in spells:
        spell.draw(screen)

    #drawing all wizards spells

    for spell in repel_spells[:]:
        spell.draw(screen)

    # drawing all enemy spells
    for blast in oneI_radial_blast[:]:
        blast.draw(screen)

    for shoot in oneI_spells[:]:
        shoot.draw(screen)

    for spit in bat_projectiles[:]:
        spit.draw(screen)

    for beam in oneI_beam_spells[:]:
        beam.draw(screen)
    
    if room_key.collected and room_key.text_timer >0:
        clear_level_1 = font.render("Level 1 Cleared", True, (0,255,128))
        screen.blit(clear_level_1, (400,400))



#SOUND SYSTEM   
sound_dir = os.path.join('src','assets', 'sounds')
unlock_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'unlock.mp3'))
recharge_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'recharge.mp3'))
hurt_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'hurt.mp3'))
spell_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'spell.mp3'))
spell2_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'spell2.mp3'))
game_music = pygame.mixer.music.load(os.path.join(sound_dir, "bg.mp3"))
pygame.mixer.music.play(-1)

sfx_list = [unlock_sound, recharge_sound, hurt_sound, spell_sound, spell2_sound]

#audio sliders setting 
panel_x = (screen_width - 440) // 2
bgm_slider = slider(panel_x+130, screen_height // 2 - 30, 200, 16, initial_val=0.5)
sfx_slider = slider(panel_x + 130, screen_height // 2 - 80, 200, 16, initial_val=0.7)

# the start volume 
pygame.mixer.music.set_volume(bgm_slider.val)
for sfx in sfx_list:
    sfx.set_volume(sfx_slider.val)


font = pygame.font.SysFont('comicsans', 30, True)
spell_limit = 5

room_key = keys_drop()
run = True
shoot_loop = 0

#game timers
player_hit_cooldown = 0
boss_locked_timer = 0


#game lists
spells = []
bat_projectiles = []
oneI_spells = []
oneI_beam_spells = []
repel_spells = []
oneI_radial_blast = []



dungeon = build_dungeon()
dungeon_stairs_room_key = None # Add this later a cool type looking key which appears only once you kill all the other enemies
current_room_key = 'spawn room'
current_room = dungeon[current_room_key]
enemies = current_room.enemies
#Main loop
while run:

    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN and game_state == 'PLAYING':
            if event.key == pygame.K_p:
                game_paused = not game_paused

        if game_state == 'MENU':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(mouse_pos):
                    game_state = "PLAYING"
                elif exit_button_rect.collidepoint(mouse_pos):
                    run = False

        if game_state == "PLAYING" and game_paused:
            bgm_slider.handle_event(event)
            sfx_slider.handle_event(event)

            pygame.mixer.music.set_volume(bgm_slider.val)
            for sfx in sfx_list:
                sfx.set_volume(sfx_slider.val)

    if game_state == "MENU":
        if start_screen_bg:
            screen.blit(start_screen_bg, (0,0))
        else:
            screen.fill('Grey')

        
        if play_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, color_hover, play_button_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, color_normal, play_button_rect, border_radius=10)

        if exit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, color_hover, exit_button_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, color_normal, exit_button_rect, border_radius=10)

        #Display game name on the screen
        game_name = font.render("Wizard Excorcist: Redemption of the fallen castle", True, (128,100,255))
        screen.blit(game_name, (200,40))
        
        # Play button
        play_text = font.render("ENTER CASTLE", True, (255,255,255))
        screen.blit(play_text, (325, 415))
        # Exit button
        exit_text = font.render("ABANDON", True, (255,255,255))
        screen.blit(exit_text, (350, 495))
        
        pygame.display.update()
    
    elif game_state == "victory":
        screen.fill((20,10,10))
        victory_text = font.render("Castle Purified!", True, (0,255,128))
        score_text = font.render(f"Grand score: {score}", True, (255,255,255))
        retry_text = font.render("Press SPACE to return to main menu", True, (150,150,150))

        screen.blit(victory_text, (260,300))
        screen.blit(score_text, (325,360))
        screen.blit(retry_text, (230, 450))

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score = 0
            game_state = "MENU"

    elif game_state == "game_over":
        screen.fill((20,10,10))
        over_text = font.render("The wizard has fallen GAME OVER!", True, (255,0,0))
        score_text = font.render(f"Final score {score}", True, (255,255,255))
        retry_text = font.render("To revive press space!", True, (150,150,150))

        screen.blit(over_text, (280,300))
        screen.blit(score_text, (320,360))
        screen.blit(retry_text, (230, 450))

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score = 0
            game_state = "MENU"

    # game state of playing 
    elif game_state == "PLAYING":
        if not game_paused:
            if shoot_loop > 0:
                shoot_loop += 1
            if shoot_loop > 3:
                shoot_loop = 0

            if player_hit_cooldown > 0:
                player_hit_cooldown -= 1


            if room_key.collected and room_key.text_timer > 0:
                room_key.text_timer -= 1

            active_spells = []
            for spell in spells[:]:        
                if (spell.x_pos < screen_width and spell.x_pos > 0) and (spell.y_pos < screen_height and spell.y_pos > 0):
                    if spell.facing == "right":
                        spell.x_pos += spell.vel
                    elif spell.facing == "left":
                        spell.x_pos -= spell.vel
                    elif spell.facing == "upwards":
                        spell.y_pos -= spell.vel
                    elif spell.facing == 'downwards':
                        spell.y_pos += spell.vel
                    active_spells.append(spell)           
            spells = active_spells

            wizard_rect = pygame.Rect(wizard.hit_box[0], wizard.hit_box[1], wizard.hit_box[2], wizard.hit_box[3])

            if current_room.is_boss_room and not current_room.cleared:
                pass

            new_spawned_enemies = []

            for enemy in enemies:
                if enemy.x < 0:
                    enemy.x = 0
                elif enemy.x > screen_width - enemy.hit_box[2]:
                    enemy.x = screen_width - enemy.hit_box[2]

                if enemy.y < 0:
                    enemy.y = 0 
                elif enemy.y > screen_height - enemy.hit_box[3]:
                    enemy.y = screen_height - enemy.hit_box[3]

                enemy.hit_box = (enemy.x, enemy.y, enemy.hit_box[2], enemy.hit_box[3])

                enemy_rect = pygame.Rect(enemy.hit_box[0], enemy.hit_box[1], enemy.hit_box[2], enemy.hit_box[3])
                
                #Position of bat spit
                if hasattr(enemy, 'type') and enemy.type == "bat":
                    enemy.shoot_cooldown -= 1

                    if enemy.shoot_cooldown <= 0:
                        dx = wizard.x_pos - enemy.x
                        dy = wizard.y_pos - enemy.y

                        if abs(dx) > abs (dy):
                            if dx > 0:
                                spit_dirc = "right"
                            else:
                                spit_dirc = "left"
                        else:
                            if dy > 0:
                                spit_dirc = "downwards"
                            else:
                                spit_dirc = "upwards"

            

                        new_spit = enemy_projectile_bat(enemy.x + 56, enemy.y + 56, spit_dirc)
                        bat_projectiles.append(new_spit)
                        enemy.shoot_cooldown = enemy.max_cooldown


                #position of oneI shoot
                if hasattr(enemy, 'type') and enemy.type == "oneI":
                    enemy.shoot_cooldown -= 1

                    if enemy.shoot_cooldown <= 0:
                        dx = wizard.x_pos - enemy.x 
                        dy = wizard.y_pos - enemy.y
                        
                        if abs(dx) > abs (dy):
                            if dx < 0:
                                shoot_dirc = "left"
                            else: 
                                shoot_dirc = "right"
                        else:
                            if dy < 0:
                                shoot_dirc = "upwards"
                            else: 
                                shoot_dirc = "downwards"
                        
                        new_shoot = oneI_spell(enemy.x+48, enemy.y+18, shoot_dirc)
                        oneI_spells.append(new_shoot)
                        enemy.shoot_cooldown = enemy.max_shoot_cooldown
                    #oneI beam 
                    enemy.beam_cooldown -= 1
                    if enemy.beam_cooldown <= 0:
                        oneI_beam_spells.append(oneI_beam(screen_width, screen_height))
                        enemy.beam_cooldown = 300       
        
                if enemy_rect.colliderect(wizard_rect):
                    if player_hit_cooldown == 0:
                        hurt_sound.play()
                        wizard.hit(enemy.damage)
                        if score > 0:
                            score -= 2
                        else:
                            score -= 0
                        player_hit_cooldown = 30

                if enemy.visible:
                    for spell in spells[:]:
                            spell_rect = pygame.Rect(spell.x_pos, spell.y_pos, 16, 16)

                            if enemy_rect.colliderect(spell_rect):
                                enemy.hit()
                                score += 1

                                if spell in spells:
                                    spells.remove(spell)
                                if not enemy.visible or getattr(enemy, 'is_dying', False):
                                    if getattr(enemy, 'health', 0) <= 0 or not enemy.visible:
                                        enemy.visible = False
                                        if isinstance(enemy, slime) and not getattr(enemy, 'is_small', False):
                                            slime_a = slime(enemy.x, enemy.y, 64, 64, is_small=True)
                                            slime_b = slime(enemy.x, enemy.y + 15, 64, 64, is_small=True)
                                            new_spawned_enemies.extend([slime_a, slime_b])
                                break
                

                # oneI radial blast 
                if hasattr(enemy, 'type') and enemy.type == "oneI":
                    if enemy.radial_cooldown > 0:
                        enemy.radial_cooldown -= 1
                    else:
                        new_burst = oneI_radial_burst(enemy.x +32, enemy.y + 32, num_shoots=12)
                        oneI_radial_blast.append(new_burst)
                        enemy.radial_cooldown = 240

            if new_spawned_enemies: 
                enemies.extend(new_spawned_enemies)
               
            # Wizard repel spell

            for spell in repel_spells[:]:
                spell.update(enemies)
                if not spell.active:
                    repel_spells.remove(spell)

            #oneI shoot collision code 
            for shoot in oneI_spells[:]:
                shoot.update()    
            
                shoot_rect = pygame.Rect(shoot.x_pos, shoot.y_pos, 16, 16)
                if shoot_rect.colliderect(wizard_rect):
                    if player_hit_cooldown == 0:
                        hurt_sound.play()
                        wizard.hit(4)
                        if score > 0:
                            score -= 4
                        player_hit_cooldown = 30
                    shoot.active = False
                    oneI_spells.remove(shoot)
                    continue
                
                if (shoot.x_pos < 0 or shoot.x_pos > screen_width or
                    shoot.y_pos < 0 or shoot.y_pos > screen_height):
                    shoot.active = False
                    oneI_spells.remove(shoot)
                
            
            #oneI beam collision code
            for beam in oneI_beam_spells[:]:
                cooldown_val = beam.update(wizard_rect, wizard, player_hit_cooldown, hurt_sound)
                if cooldown_val > 0:
                    player_hit_cooldown = cooldown_val 
                    if score > 0:
                        score -= 3
                if not beam.active:
                    oneI_beam_spells.remove(beam)

            #oneI radial burst code 
            for blast in oneI_radial_blast[:]:
                
                if isinstance(blast, oneI_radial_burst):
                    casting_enemy = None
                    for e in enemies:
                        if hasattr(e, "type") and e.type == "oneI":
                            if abs((e.x + 32) - blast.x_pos) < 50 and abs((e.y + 32) - blast.y_pos) < 50:
                                casting_enemy = e  
                                break
                    blast.update(oneI_radial_blast, screen_width, screen_height, casting_enemy)

                elif isinstance(blast, oneI_radial):
                    blast.update(screen_width, screen_height)
                    
                    blast_rect = pygame.Rect(blast.x_pos-4, blast.y_pos -4, 8,8)
                    if blast_rect.colliderect(wizard_rect) and player_hit_cooldown == 0:
                        hurt_sound.play()
                        wizard.hit(9)
                        if score > 0:
                            score -= 5
                        blast.active = False 
                if not blast.active:
                    oneI_radial_blast.remove(blast)

            #Bat spit collision code
            for spit in bat_projectiles[:]:
                spit.update()

                spit_rect = pygame.Rect(spit.x_pos, spit.y_pos, 16,16)

                if spit_rect.colliderect(wizard_rect):
                    if player_hit_cooldown == 0:
                        hurt_sound.play()
                        wizard.hit(1.0)
                        if score > 0:
                            score -= 2
                        player_hit_cooldown = 30
                    spit.active = False
                    bat_projectiles.remove(spit)
                    continue
                
                if (spit.x_pos < 0 or spit.x_pos > screen_width or
                    spit.y_pos < 0 or spit.y_pos > screen_height):
                    spit.active = False
                    bat_projectiles.remove(spit)

            
                    
            enemies = [e for e in enemies if e.visible]
            current_room.enemies = enemies
            
            if len(enemies) == 0 and not current_room.cleared:
                current_room.cleared = True 

                if current_room.is_boss_room:
                    game_state = "victory"
                else:
                    room_key.visible = True


            if boss_locked_timer > 0:
                boss_locked_timer -= 1

            next_room_key = None

            if current_room.cleared and not room_key.visible:
                #East and west doors
                if wizard_rect.colliderect(east_door_rect) and 'east' in current_room.connections:
                    candidate_key = current_room.connections['east']
                    if dungeon[candidate_key].is_boss_room and not  all_regular_enemies_defeated(dungeon):
                        wizard.x_pos -= 15
                        boss_locked_timer = 60
                    else:
                        next_room_key = candidate_key
                        wizard.x_pos = door_depth + 10
                
                elif wizard_rect.colliderect(west_door_rect) and 'west' in current_room.connections:
                    candidate_key = current_room.connections['west']
                    if dungeon[candidate_key].is_boss_room and not all_regular_enemies_defeated(dungeon):
                        wizard.x_pos += 15
                        boss_locked_timer = 60
                    else:
                        next_room_key = candidate_key 
                        wizard.x_pos = screen_width - 128 - door_depth - 10


                #North and south doors
                if wizard_rect.colliderect(north_door_rect) and 'north' in current_room.connections:
                    candidate_key = current_room.connections['north']
                    if dungeon[candidate_key].is_boss_room and not all_regular_enemies_defeated(dungeon):
                        wizard.y_pos += 15
                        boss_locked_timer = 60
                    else:
                        next_room_key = candidate_key 
                        wizard.y_pos = screen_height - 128 - door_depth - 10
                elif wizard_rect.colliderect(south_door_rect) and 'south' in current_room.connections:
                    candidate_key = current_room.connections['south']
                    if dungeon[candidate_key].is_boss_room and not all_regular_enemies_defeated(dungeon):
                        wizard.y_pos -= 15
                        boss_locked_timer = 60
                    else:
                        next_room_key = candidate_key
                        wizard.y_pos = door_depth + 10 
                    
                    

            if next_room_key:
                current_room_key = next_room_key
                current_room = dungeon[current_room_key]
                enemies = current_room.enemies

                if not current_room.cleared:
                    room_key.visible = False
                    room_key.collected = False
                    
            if room_key.visible and not room_key.collected:
                if  wizard_rect.colliderect(room_key.rect):
                    score += 10
                    unlock_sound.play()
                    room_key.visible = False
                    room_key.collected = True
                    room_key.text_timer = 150
                    
            #check key presses for controls 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                wizard.facing = "left"
                wizard.is_moving = True
                if wizard.hit_box[0]> 0:
                    wizard.x_pos -= wizard.vel
            
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                wizard.facing = "right"
                wizard.is_moving = True
                if wizard.hit_box[0] + wizard.hit_box[2] < screen_width :
                    wizard.x_pos += wizard.vel

            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                wizard.facing = "upwards"
                wizard.is_moving = True 
                if wizard.hit_box[1] > 0:
                    wizard.y_pos -= wizard.vel

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                wizard.facing = "downwards"
                wizard.is_moving = True
                if wizard.hit_box[1] + wizard.hit_box[3] < screen_height:
                    wizard.y_pos += wizard.vel
            else:
                wizard.is_moving = False
            
            if keys[pygame.K_PERIOD]:
                recharge_sound.play()
                if wizard.mana < 10:
                    wizard.mana += 1
            else:
                recharge_sound.stop()
            
            if keys[pygame.K_f]:
                
                if len(repel_spells) == 0 and wizard.mana >=3:
                    spell2_sound.play()
                    wizard.mana -= 3

                    center_x = wizard.x_pos + wizard.character_size[0] // 2
                    center_y = wizard.y_pos + wizard.character_size[1] // 2

                    new_repel = repel_spell(center_x, center_y, wizard.facing)
                    repel_spells.append(new_repel)
            
            if (keys[pygame.K_SPACE] or keys[pygame.K_COMMA]) and shoot_loop == 0 and not keys[pygame.K_PERIOD]:
                if wizard.mana > 0 and len(spells) < spell_limit:
                    wizard.mana -= 1
                    spell_sound.play()
                    spells.append(projectile_spell(round(wizard.x_pos + wizard.width//2), round(wizard.y_pos + wizard.height//2), wizard.facing))
                shoot_loop = 1  
            

            if wizard.health <= 0:
                if admin_mode:
                    pass
                else:
                    game_state = "game_over"
                    score = 0
                    
                    wizard.health = wizard.max_health
                    wizard.x_pos, wizard.y_pos = 400,200
                    current_room_key = "spawn room"
                    current_room = dungeon[current_room_key]
                    enemies = current_room.enemies
                    room_key.visible = False
                    room_key.collected = False  
                    
                    
        render_game(bat_projectiles)

        if game_paused:
            draw_pause_menu(screen, font, screen_width, screen_height, bgm_slider, sfx_slider)

        pygame.display.update()
        clock.tick(30)
pygame.quit()





