import pygame
import asyncio
import os 

from sprites import player, enemy, ghost, bat, slime, pumpkin, keys_drop, oneI, chest, hp_particles
from spells import projectile_spell, repel_spell, enemy_projectile_bat, oneI_spell, oneI_beam, oneI_radial_burst, oneI_radial, mana_charge 
from dungeon import build_dungeon
from ui import button, slider, draw_pause_menu, draw_ability_icons, draw_skill_hud, draw_start_menu, draw_game_over_screen, draw_victory_screen

async def main():

    pygame.init()

    screen_width = 1280
    screen_height = 720 

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Wizard Exorcist")
    clock = pygame.time.Clock()

    score = 0
    admin_mode = False
    game_state = "MENU"
    game_paused = False

    spells = []
    bat_projectiles = []
    oneI_spells = []
    oneI_beam_spells = []
    repel_spells = []
    oneI_radial_blast = []
    active_mana_charge = []

    dash_cooldown = 0
    repel_cooldown = 0
    player_hit_cooldown = 0
    boss_locked_timer = 0
    player_death_timer = 0 
    max_death_frames = 30
    shoot_loop = 0

    wizard = player(400, 200, 64, 64)
    room_chest = chest()
    heal_particle = hp_particles(200, 200)
    room_key = keys_drop()

    dungeon = build_dungeon()
    current_room_key = 'spawn room'
    current_room = dungeon[current_room_key]
    enemies = current_room.enemies

    door_width = 80
    door_depth = 20
    door_frame_count = 10
    door_frames_horiz = []
    door_frames_vert = []

    for i in range(door_frame_count):
        filename = f"frame{i:04d}.png"
        door_assets = os.path.join("src", "assets", "effects", "eff", "PNG", "Explosions", "doors", "large", filename)
        
        if os.path.exists(door_assets):
            raw_img = pygame.image.load(door_assets).convert_alpha()
            door_frames_horiz.append(pygame.transform.scale(raw_img, (door_width, door_depth)))
            door_frames_vert.append(pygame.transform.scale(raw_img, (door_depth, door_width)))

    north_door_rect = pygame.Rect((screen_width // 2) - (door_width // 2), 0, door_width, door_depth)
    south_door_rect = pygame.Rect((screen_width // 2) - (door_width // 2), screen_height - door_depth, door_width, door_depth)
    east_door_rect = pygame.Rect(screen_width - door_depth, (screen_height // 2) - (door_width // 2), door_depth, door_width)
    west_door_rect = pygame.Rect(0, (screen_height // 2) - (door_width // 2), door_depth, door_width)

    custom_font = pygame.font.Font("src/assets/ux/font/NicerNightie.ttf", 30)

    play_btn = button((screen_width // 2) - 120, 380, 240, 60, "Enter Castle", custom_font)
    exit_btn = button((screen_width // 2) - 120, 470, 240, 60, "Abandon", custom_font)
    retry_btn = button(0, 0, 220, 50, "Try Again", custom_font, bg_color=(80, 20, 20), hover_color=(120, 30, 30)) 
    menu_btn = button(0, 0, 220, 50, "Main Menu", custom_font, bg_color=(40, 40, 50), hover_color=(70, 70, 90))

    def start_new_game():
        nonlocal score, dungeon, current_room_key, current_room, enemies
        nonlocal spells, bat_projectiles, oneI_spells, oneI_beam_spells, repel_spells, oneI_radial_blast, active_mana_charge
        nonlocal game_state, game_paused, dash_cooldown, repel_cooldown, player_hit_cooldown

        score = 0
        wizard.health = wizard.max_health
        wizard.mana = 10
        wizard.is_dying = False 
        wizard.x_pos, wizard.y_pos = 400, 200

        dash_cooldown = 0
        repel_cooldown = 0
        player_hit_cooldown = 0

        spells.clear()   
        bat_projectiles.clear()
        oneI_spells.clear()
        oneI_beam_spells.clear()
        repel_spells.clear()
        oneI_radial_blast.clear()
        active_mana_charge.clear()
        
        dungeon = build_dungeon()
        current_room_key = "spawn room"
        current_room = dungeon[current_room_key]
        enemies = current_room.enemies

        room_chest.visible = False
        room_chest.collected = False
        room_chest.is_opened = False

        room_key.visible = False
        room_key.collected = False 

        game_state = "PLAYING"

    loaded_backgrounds = {}
    def get_room_background(room):
        path = room.background_path
        if path not in loaded_backgrounds:
            if os.path.exists(path):
                image = pygame.image.load(path).convert()
                loaded_backgrounds[path] = pygame.transform.scale(image, (screen_width, screen_height))
            else: 
                fallback = pygame.Surface((screen_width, screen_height))
                fallback.fill((40, 40, 40))
                loaded_backgrounds[path] = fallback
        return loaded_backgrounds[path]

    def all_regular_enemies_defeated(dungeon):
        for key, room in dungeon.items():
            if not room.is_boss_room and not room.cleared:
                return False
        return True

    def render_game(bat_projectiles):
        room_bg = get_room_background(current_room)
        screen.blit(room_bg, (0, 0))
        
        if current_room.cleared and not room_key.visible:
            hidden = getattr(current_room, 'hidden_doors', [])
            
            if door_frames_horiz:
                frame_index = (pygame.time.get_ticks() // 100) % len(door_frames_horiz)
                portal_h = door_frames_horiz[frame_index]
                portal_v = door_frames_vert[frame_index]
            else:
                portal_h = portal_v = None

            doors = [
                ('north', north_door_rect, portal_h),
                ('south', south_door_rect, portal_h),
                ('east',  east_door_rect,  portal_v),
                ('west',  west_door_rect,  portal_v)
            ]

            for d_name, d_rect, frame_img in doors:
                if d_name in current_room.connections and d_name not in hidden:
                    if frame_img:
                        screen.blit(frame_img, d_rect.topleft)
                    else:
                        pygame.draw.rect(screen, (80, 50, 180), d_rect)

        if boss_locked_timer > 0:
            locked_msg = font.render("Boss Door Sealed! Clear all rooms first.", True, (255, 50, 50))
            screen.blit(locked_msg, (screen_width // 2 - locked_msg.get_width() // 2, 50))

        text = font.render(f'Score: {score}', 1, (255, 0, 0))
        room_chest.draw(screen)
        heal_particle.draw(screen)

        screen.blit(text, (670, 20))
        wizard.draw(screen)

        for e in enemies:
            e.draw(screen, wizard, offset_y=20, bar_width=50, enemies=enemies)

        room_key.draw(screen)

        for spell in spells:
            spell.draw(screen)

        for spell in repel_spells[:]:
            spell.draw(screen)

        for blast in oneI_radial_blast[:]:
            blast.draw(screen)

        for shoot in oneI_spells[:]:
            shoot.draw(screen)

        for spit in bat_projectiles[:]:
            spit.draw(screen)

        for beam in oneI_beam_spells[:]:
            beam.draw(screen)

        for mana in active_mana_charge[:]:
            mana.update(wizard)
            mana.draw(screen)
            if not mana.active:
                active_mana_charge.remove(mana)

        draw_skill_hud(screen, screen_height, dash_cooldown, repel_cooldown)

    sound_dir = os.path.join('src', 'assets', 'sounds')
    unlock_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'unlock.mp3'))
    recharge_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'recharge.mp3'))
    hurt_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'hurt.mp3'))
    spell_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'spell.mp3'))
    spell2_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'spell2.mp3'))
    pygame.mixer.music.load(os.path.join(sound_dir, "bg.mp3"))
    pygame.mixer.music.play(-1)

    sfx_list = [unlock_sound, recharge_sound, hurt_sound, spell_sound, spell2_sound]

    panel_x = (screen_width - 440) // 2
    bgm_slider = slider(panel_x + 130, screen_height // 2 - 30, 200, 16, initial_val=0.5)
    sfx_slider = slider(panel_x + 130, screen_height // 2 - 80, 200, 16, initial_val=0.7)

    pygame.mixer.music.set_volume(bgm_slider.val)
    for sfx in sfx_list:
        sfx.set_volume(sfx_slider.val)

    font = pygame.font.Font("src/assets/ux/font/NicerNightie.ttf", 30)
    spell_limit = 5

    run = True

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
                    if play_btn.handle_event(event):
                        start_new_game()
                    elif exit_btn.handle_event(event):
                        run = False

            if game_state == "PLAYING" and game_paused:
                bgm_slider.handle_event(event)
                sfx_slider.handle_event(event)

                pygame.mixer.music.set_volume(bgm_slider.val)
                for sfx in sfx_list:
                    sfx.set_volume(sfx_slider.val)

            if game_state in ("game_over", "victory"):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_btn.handle_event(event):
                        start_new_game()
                    elif menu_btn.handle_event(event):
                        score = 0 
                        game_state = "MENU"

        if game_state == "MENU":    
            draw_start_menu(screen, screen_width, screen_height, play_btn, exit_btn, mouse_pos)
            pygame.display.update()

        elif game_state == "victory":
            draw_victory_screen(screen, font, screen_width, screen_height, score, menu_btn, retry_btn, mouse_pos)
            pygame.display.update()

        elif game_state == "game_over":
            render_game(bat_projectiles)
            draw_game_over_screen(screen, font, screen_width, screen_height, score, retry_btn, menu_btn, mouse_pos)
            pygame.display.update()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                score = 0
                game_state = "MENU"

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

                if wizard.health <= 0 and not admin_mode:
                    game_state = 'Dying'
                    player_death_timer = max_death_frames
                    wizard.is_dying = True 

                active_spells = []
                for spell in spells[:]:        
                    if (0 < spell.x_pos < screen_width) and (0 < spell.y_pos < screen_height):
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
                new_spawned_enemies = []

                for enemy in enemies:
                    if getattr(enemy, 'is_dying', False) or not enemy.visible:
                        continue
                    
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
                    
                    if hasattr(enemy, 'type') and enemy.type == "bat":
                        enemy.shoot_cooldown -= 1
                        if enemy.shoot_cooldown <= 0:
                            dx = wizard.x_pos - enemy.x
                            dy = wizard.y_pos - enemy.y
                            spit_dirc = "right" if dx > 0 else "left" if abs(dx) > abs(dy) else "downwards" if dy > 0 else "upwards"
                            new_spit = enemy_projectile_bat(enemy.x + 56, enemy.y + 56, spit_dirc)
                            bat_projectiles.append(new_spit)
                            enemy.shoot_cooldown = enemy.max_cooldown

                    if hasattr(enemy, 'type') and enemy.type == "oneI":
                        enemy.shoot_cooldown -= 1
                        if enemy.shoot_cooldown <= 0:
                            dx = wizard.x_pos - enemy.x 
                            dy = wizard.y_pos - enemy.y
                            shoot_dirc = "right" if dx > 0 else "left" if abs(dx) > abs(dy) else "downwards" if dy > 0 else "upwards"
                            new_shoot = oneI_spell(enemy.x + 48, enemy.y + 18, shoot_dirc)
                            oneI_spells.append(new_shoot)
                            enemy.shoot_cooldown = enemy.max_shoot_cooldown

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
                            player_hit_cooldown = 30

                    if enemy.visible and not getattr(enemy, 'is_dying', False):
                        for spell in spells[:]:
                            spell_rect = pygame.Rect(spell.x_pos, spell.y_pos, 16, 16)
                            if enemy_rect.colliderect(spell_rect):
                                enemy.hit()
                                score += 1
                                if spell in spells:
                                    spells.remove(spell)
                                if isinstance(enemy, slime) and enemy.is_dying and not getattr(enemy, 'is_small', False):
                                    slime_a = slime(enemy.x, enemy.y, 64, 64, is_small=True)
                                    slime_b = slime(enemy.x, enemy.y + 25, 64, 64, is_small=True)
                                    new_spawned_enemies.extend([slime_a, slime_b])
                                break

                    if hasattr(enemy, 'type') and enemy.type == "oneI":
                        if enemy.radial_cooldown > 0:
                            enemy.radial_cooldown -= 1
                        else:
                            new_burst = oneI_radial_burst(enemy.x + 32, enemy.y + 32, num_shoots=12)
                            oneI_radial_blast.append(new_burst)
                            enemy.radial_cooldown = 240
                    
                if new_spawned_enemies: 
                    enemies.extend(new_spawned_enemies)

                for spell in repel_spells[:]:
                    spell.update(enemies)
                    if not spell.active:
                        repel_spells.remove(spell)

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
                    
                    if not (0 <= shoot.x_pos <= screen_width and 0 <= shoot.y_pos <= screen_height):
                        shoot.active = False
                        oneI_spells.remove(shoot)

                for beam in oneI_beam_spells[:]:
                    cooldown_val = beam.update(wizard_rect, wizard, player_hit_cooldown, hurt_sound)
                    if cooldown_val > 0:
                        player_hit_cooldown = cooldown_val 
                        if score > 0:
                            score -= 3
                    if not beam.active:
                        oneI_beam_spells.remove(beam)

                for blast in oneI_radial_blast[:]:
                    if isinstance(blast, oneI_radial_burst):
                        casting_enemy = next((e for e in enemies if hasattr(e, "type") and e.type == "oneI" and abs((e.x + 32) - blast.x_pos) < 50 and abs((e.y + 32) - blast.y_pos) < 50), None)
                        blast.update(oneI_radial_blast, screen_width, screen_height, casting_enemy)
                    elif isinstance(blast, oneI_radial):
                        blast.update(screen_width, screen_height)
                        blast_rect = pygame.Rect(blast.x_pos - 4, blast.y_pos - 4, 8, 8)
                        if blast_rect.colliderect(wizard_rect) and player_hit_cooldown == 0:
                            hurt_sound.play()
                            wizard.hit(9)
                            if score > 0:
                                score -= 5
                            blast.active = False 
                    if not blast.active:
                        oneI_radial_blast.remove(blast)

                for spit in bat_projectiles[:]:
                    spit.update()
                    spit_rect = pygame.Rect(spit.x_pos, spit.y_pos, 16, 16)
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
                    
                    if not (0 <= spit.x_pos <= screen_width and 0 <= spit.y_pos <= screen_height):
                        spit.active = False
                        bat_projectiles.remove(spit)

                enemies = [e for e in current_room.enemies if e.visible or e.is_dying]
                current_room.enemies = enemies
                
                if len(enemies) == 0 and not current_room.cleared:
                    current_room.cleared = True 
                    if current_room.is_boss_room:
                        game_state = "victory"
                    else:
                        room_key.spawn(min_x=150, max_x=1050, min_y=100, max_y=600)
                        room_chest.spawn(min_x=150, max_x=1050, min_y=100, max_y=600)

                if current_room.is_boss_room:
                    boss_alive = any(hasattr(e, 'type') and e.type == 'oneI' and (e.visible or getattr(e, 'health', 1) > 0) for e in enemies)
                    if not boss_alive:
                        current_room.cleared = True 
                        game_state = "victory"

                next_room_key = None

                if current_room.cleared and not room_key.visible:
                    if wizard_rect.colliderect(east_door_rect) and 'east' in current_room.connections:
                        candidate_key = current_room.connections['east']
                        if dungeon[candidate_key].is_boss_room and not all_regular_enemies_defeated(dungeon):
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

                    room_key.visible = False
                    room_key.collected = False
                    room_chest.visible = False
                    room_chest.collected = False
                    room_chest.is_opened = False
                    heal_particle.is_visible = False
                    heal_particle.is_collected = False

                    if len(enemies) == 0:
                        current_room.cleared = True
                        if current_room.is_boss_room:
                            game_state = 'victory'
                        elif not getattr(current_room, 'chest_opened', False):
                            room_chest.spawn(min_x=150, max_x=1050, min_y=100, max_y=600)
                            room_chest.visible = True
                            room_chest.is_opened = False

                if room_key.visible and not room_key.collected:
                    if wizard_rect.colliderect(room_key.rect):
                        score += 10
                        unlock_sound.play()
                        room_key.visible = False
                        room_key.collected = True 
                        room_key.text_timer = 150

                if room_chest.visible and not room_chest.collected:
                    if wizard_rect.colliderect(room_chest.rect):
                        room_chest.collected = True
                        room_chest.is_opened = True 
                        current_room.chest_opened = True
                        heal_particle.trigger(room_chest)

                if heal_particle.is_visible and not heal_particle.is_collected:
                    if wizard_rect.colliderect(heal_particle.rect):
                        heal_particle.is_collected = True
                        heal_particle.is_visible = False
                        room_chest.visible = False
                        room_chest.is_opened = False

                        if all_regular_enemies_defeated(dungeon):
                            wizard.health = wizard.max_health
                        else:
                            wizard.health = min(wizard.max_health, wizard.health + 7)

                room_chest.update()
                heal_particle.update()
                        
                keys = pygame.key.get_pressed()
                wizard.is_moving = False

                if keys[pygame.K_a]:
                    wizard.facing = "left"
                    wizard.is_moving = True
                    if wizard.hit_box[0] > 0:
                        wizard.x_pos -= wizard.vel 

                if keys[pygame.K_d]:
                    wizard.facing = "right"
                    wizard.is_moving = True
                    if wizard.hit_box[0] + wizard.hit_box[2] < screen_width:
                        wizard.x_pos += wizard.vel

                if keys[pygame.K_w]:
                    wizard.facing = "upwards"
                    wizard.is_moving = True 
                    if wizard.hit_box[1] > 0:
                        wizard.y_pos -= wizard.vel 

                if keys[pygame.K_s]:
                    wizard.facing = "downwards"
                    wizard.is_moving = True
                    if wizard.hit_box[1] + wizard.hit_box[3] < screen_height:
                        wizard.y_pos += wizard.vel 

                if keys[pygame.K_PERIOD]:
                    if len(active_mana_charge) == 0:
                        charge_effect = mana_charge(wizard.x_pos, wizard.y_pos, 128, 128)
                        active_mana_charge.append(charge_effect)
                        recharge_sound.play(-1)
                    if wizard.mana < 10:
                        wizard.mana += 1
                else:
                    recharge_sound.stop()
                
                if repel_cooldown > 0:
                    repel_cooldown -= 1
                if keys[pygame.K_f]:
                    if len(repel_spells) == 0 and repel_cooldown == 0 and wizard.mana >= 3:
                        spell2_sound.play()
                        wizard.mana -= 3
                        repel_cooldown = 300
                        center_x = wizard.x_pos + wizard.character_size[0] // 2
                        center_y = wizard.y_pos + wizard.character_size[1] // 2
                        new_repel = repel_spell(center_x, center_y, wizard.facing)
                        repel_spells.append(new_repel)
                
                if (keys[pygame.K_SPACE] or keys[pygame.K_COMMA]) and shoot_loop == 0 and not keys[pygame.K_PERIOD] and not keys[pygame.K_f]:
                    if wizard.mana > 0 and len(spells) < spell_limit:
                        wizard.mana -= 1
                        spell_sound.play()
                        spells.append(projectile_spell(round(wizard.x_pos + wizard.width // 2), round(wizard.y_pos + wizard.height // 2), wizard.facing))
                    shoot_loop = 1  
                
                if dash_cooldown > 0:
                    dash_cooldown -= 1
                if keys[pygame.K_LSHIFT] and dash_cooldown == 0 and wizard.mana >= 2:
                    dash_cooldown = 300
                    dash_dist = 70
                    if wizard.facing == "left" and wizard.hit_box[0] - dash_dist > 0:
                        wizard.x_pos -= dash_dist
                        wizard.mana -= 2
                    elif wizard.facing == "right" and wizard.hit_box[0] + wizard.hit_box[2] + dash_dist < screen_width:
                        wizard.x_pos += dash_dist
                        wizard.mana -= 2
                    elif wizard.facing == "upwards" and wizard.hit_box[1] - dash_dist > 0:
                        wizard.y_pos -= dash_dist
                        wizard.mana -= 2
                    elif wizard.facing == "downwards" and wizard.hit_box[1] + wizard.hit_box[3] + dash_dist < screen_height:
                        wizard.y_pos += dash_dist
                        wizard.mana -= 2

                if boss_locked_timer > 0:
                    boss_locked_timer -= 1

            render_game(bat_projectiles)

            if game_paused:
                draw_pause_menu(screen, font, screen_width, screen_height, bgm_slider, sfx_slider)

        elif game_state == "Dying":
            render_game(bat_projectiles)
            if hasattr(wizard, 'play_death_animation'):
                wizard.play_death_animation(screen)  

            player_death_timer -= 1
            if player_death_timer <= 0:
                game_state = "game_over"

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())