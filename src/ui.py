# The UI script for the game 

import pygame
import os


#setting up the font assets for the all the texts 
font_path = "src/assets/ux/font/NicerNightie.ttf"
custom_font = pygame.font.Font(font_path, 30)
title_font = pygame.font.Font(font_path, 40)

if custom_font:
    custom_font_is = True
#icons assets 
dash_icon_path = os.path.join("src", "assets", "ux", "powers_icons", "dash.png")
repel_icon_path = os.path.join("src", "assets", "ux", "powers_icons", "repel_spell.png")
shoot_icon_path = os.path.join("src", "assets", "ux", "powers_icons", "shoot.png")
recharge_icon_path = os.path.join("src", "assets", "ux", "powers_icons", "recharge.png")



dash_icon_image = pygame.image.load(dash_icon_path) if os.path.exists(dash_icon_path) else None
repel_icon_image = pygame.image.load(repel_icon_path) if os.path.exists(repel_icon_path) else None 
shoot_icon_image = pygame.image.load(shoot_icon_path) if os.path.exists(shoot_icon_path) else None
recharge_icon_image = pygame.image.load(recharge_icon_path) if os.path.exists(recharge_icon_path) else None

start_bg_path = os.path.join("src", "assets", "ux", "start_screen.png")
start_bg_image = pygame.image.load(start_bg_path) if os.path.exists(start_bg_path) else None

#colors 
GRAY = (50,50,50)
LIGHT_GRAY = (80,80,120)
WHITE = (255,255,255)
DARK_PANEL = (25,25,35)
BORDER_PURPLE = (200, 200, 255)

class button():
    def __init__(self, x, y, width, height, text, font, bg_color=GRAY, hover_color=LIGHT_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
        
#menu volume control 
class slider():
    def __init__(self, x, y, width, height, initial_val = 0.5):
        self.rect= pygame.Rect(x, y, width, height)
        self.val = max(0.0, min(1.0, initial_val))
        self.handle_radius = height // 2 + 4
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            handle_x = self.rect.x + int(self.val * self.rect.width)
            handle_rect = pygame.Rect(handle_x - 12, self.rect.y - 6, 24, self.rect.height + 12)
            if handle_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
                self.dragging = True
                self.update_val(mouse_pos[0])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_val(event.pos[0])

    def update_val(self, mouse_x):
        relative_x = mouse_x - self.rect.x 
        self.val = max(0.0, min(1.0, relative_x / self.rect.width))

    def draw(self, screen):
        pygame.draw.rect(screen,  (50, 50, 65), self.rect, border_radius=4)

        fill_width = int(self.val * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)  
            pygame.draw.rect(screen, (100, 200,255), fill_rect, 2, border_radius= 4)

        pygame.draw.rect(screen, (120,120,150), self.rect, 2, border_radius=4)

        handle_x = self.rect.x + fill_width
        handle_y= self.rect.y + self.rect.height // 2
        pygame.draw.circle(screen, (240,240,250), (handle_x, handle_y), self.handle_radius)
        pygame.draw.circle(screen, (40, 40, 50), (handle_x, handle_y), self.handle_radius, 2)

def draw_pause_menu(screen, font, screen_width, screen_height, bgm_slider, sfx_slider):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((10,10,20,190))
    screen.blit(overlay, (0,0))

    pw, ph = 440, 320
    px = (screen_width - pw) // 2
    py = (screen_height - ph) // 2

    panel_rect = pygame.Rect(px, py, pw, ph)
    pygame.draw.rect(screen, (25, 25, 35), panel_rect, border_radius=10)
    pygame.draw.rect(screen, (70, 70, 100), panel_rect, 3, border_radius=10)
    title_surf = font.render("Paused", True, (255, 255, 255))
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, py+30))

    bgm_slider.rect.y = py + 105
    bgm_label = font.render("Music", True, (200, 200, 220))
    bgm_val_text = font.render(f"{int(bgm_slider.val * 100)}%", True, (150, 220, 255))
    screen.blit(bgm_label, (px+30, py+100))
    bgm_slider.draw(screen)
    screen.blit(bgm_val_text, (px + 335, py + 100))

    sfx_slider.rect.y = py + 165
    sfx_label = font.render("sfx", True, (200,200,220))
    sfx_val_text = font.render(f"{int(sfx_slider.val * 100)}%", True, (150,220,255))
    screen.blit(sfx_label, (px+ 30, py+160))
    sfx_slider.draw(screen)
    screen.blit(sfx_val_text, (px+ 335, py+ 160))

    sub_text = font.render("Press P to Resume", True, (140, 140, 160))
    screen.blit(sub_text, (screen_width // 2 - sub_text.get_width() // 2, py+ 250))



#for the ui of the spells lkely for cooldown
def draw_ability_icons(screen, x , y , size, key_text, current_cooldown, max_cooldown, spell_type="dash"):

    icon_rect = pygame.Rect(x,y, size, size)
    pygame.draw.rect(screen, (45, 30, 20), icon_rect, border_radius=6)
    pygame.draw.rect(screen, (140, 100, 60), icon_rect, width=2, border_radius=6)

    if spell_type == "dash":
        icon_img = dash_icon_image
    elif spell_type == "repel":
        icon_img = repel_icon_image
    elif spell_type == "shoot":
        icon_img = shoot_icon_image
    elif spell_type == "recharge":
        icon_img = recharge_icon_image

    if icon_img:
        padding = 0
        selected_img = pygame.transform.scale(icon_img, (size - padding * 2, size - padding * 2))
        screen.blit(selected_img, (x + padding, y + padding))


    key_font = pygame.font.SysFont("comicsans", 14, True)
    label = key_font.render(key_text, True, (215, 195, 150))
    screen.blit(label, (x + 5, y + 3))

    if current_cooldown and max_cooldown and current_cooldown > 0 and max_cooldown > 0:

        pct = current_cooldown / max_cooldown
        mask_height = int(size*pct)

        mask_surf = pygame.Surface((size, mask_height), pygame.SRCALPHA)
        mask_surf.fill((0,0,0,180))
        screen.blit(mask_surf, (x, y + (size - mask_height)))
        

def draw_skill_hud(screen, screen_height, dash_cooldown, repel_cooldown):

    draw_ability_icons(screen, x=10 , y=screen_height - 70, size=50, key_text="SHIFT", current_cooldown=dash_cooldown,
                       max_cooldown=300, spell_type="dash")

    draw_ability_icons(screen, x=70, y=screen_height - 70, size=50, key_text="F", current_cooldown=repel_cooldown,
                       max_cooldown= 300, spell_type="repel")

    draw_ability_icons(screen, x =140, y=screen_height - 70, size=50, key_text=",", current_cooldown=0,
                       max_cooldown= 0, spell_type="shoot")

    draw_ability_icons(screen, x=200, y = screen_height - 70, size=50, key_text=".", current_cooldown=0,
                        max_cooldown=0, spell_type="recharge")

def draw_start_menu(screen, screen_width, screen_height, ply_btn, exit_btn, mouse_pos):

    if start_bg_image:
        screen.blit(pygame.transform.scale(start_bg_image, (screen_width, screen_height)), (0,0))
    else:
        screen.fill((30,30,45))

    title_surf = title_font.render("Wizard Exorcist: Redemption of Falled Castle", True, (180,150,255))
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 100))

    ply_btn.is_hovered = ply_btn.rect.collidepoint(mouse_pos)
    exit_btn.is_hovered = exit_btn.rect.collidepoint(mouse_pos)

    ply_btn.draw(screen)
    exit_btn.draw(screen)


def draw_game_over_screen(screen, font, screen_width, screen_height, score, retry_btn, menu_btn, mouse_pos):

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((15, 5, 10, 220))
    screen.blit(overlay, (0,0))

    pw, ph = 520, 360
    px = (screen_width - pw) // 2
    py = (screen_height - ph) // 2

    panel_rect = pygame.Rect(px, py, pw, ph)
    pygame.draw.rect(screen, (25, 15, 20), panel_rect, border_radius=12)

    title_surf = custom_font.render("The Wizard has Fallen", True, (220, 60, 60))
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, py+35))

    score = score
    score_surf = custom_font.render(f"Final Score: {score}", True, (220,220,240))
    screen.blit(score_surf, (screen_width // 2 - score_surf.get_width() // 2, py + 145))

    retry_btn.rect.x = screen_width // 2 - 110
    retry_btn.rect.y = py + 200
    menu_btn.rect.x = screen_width // 2 - 110
    menu_btn.rect.y = py + 270

    retry_btn.is_hovered = retry_btn.rect.collidepoint(mouse_pos)
    menu_btn.is_hovered = menu_btn.rect.collidepoint(mouse_pos)

    retry_btn.draw(screen)
    menu_btn.draw(screen)



