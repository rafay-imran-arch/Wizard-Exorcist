# The UI script for the game 

import pygame

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

    title_surf = font.render("PAUSED", True, (255, 255, 255))
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, py+30))

    bgm_label = font.render("MUSIC", True, (200, 200, 220))
    bgm_val_text = font.render(f"{int(bgm_slider.val * 100)}%", True, (150, 220, 255))
    screen.blit(bgm_label, (px+30, py+100))
    bgm_slider.draw(screen)
    screen.blit(bgm_val_text, (px + 335, py + 100))

    sfx_label = font.render("SFX", True, (200,200,220))
    sfx_val_text = font.render(f"{int(sfx_slider.val * 100)}%", True, (150,220,255))
    screen.blit(sfx_label, (px+ 30, py+160))
    sfx_slider.draw(screen)
    screen.blit(sfx_val_text, (px+ 335, py+ 160))

    sub_text = font.render("Press P to Resume", True, (140, 140, 160))
    screen.blit(sub_text, (screen_width // 2 - sub_text.get_width() // 2, py+ 250))