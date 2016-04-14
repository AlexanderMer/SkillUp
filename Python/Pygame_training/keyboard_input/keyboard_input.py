import pygame, sys
from colours import *
from pygame.locals import *

"""
There are three steps for creating a text in pygame
1. Create a Font object
 Font holds information about text-font and text-size
2. Render the surface
 call .render(string text, bool anti-aliasing, color foreground, color background)
3. Get Rect object from the surface
 .get_rect()

To display the text we need to blit it on a surface
 Display_surface.blit(text_surface, text_rect)
"""

# global variables
pygame.init()
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
MAX_FPS = 30
ALLOWED_CHARS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM 1234567890_-!?"
ticker = pygame.time.Clock()
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Main Window')

text_string = "Hey there!"
marked_text_string = ""
fontObj = pygame.font.Font('freesansbold.ttf', 32)
text_surface = fontObj.render(text_string, True, GREEN, BLUE)
marked_text_surface = fontObj.render(marked_text_string, True, YELLOW, BLUE)
text_rect = text_surface.get_rect()
marked_text_rect = marked_text_surface.get_rect()

def update_text(char):
    global text_surface
    global marked_text_surface
    global text_rect
    global marked_text_rect
    global text_string
    global marked_text_string
    if text_string != "" and text_string[0] == char:
        marked_text_string += text_string[0]
        text_string = text_string[1:]
        marked_text_surface = fontObj.render(marked_text_string, True, YELLOW, BLUE)
        marked_text_rect = marked_text_surface.get_rect()  # need to get after text changes, or textbox size won't change
        text_surface = fontObj.render(text_string, True, GREEN, BLUE)
        text_rect = text_surface.get_rect()


# GAME LOOP
while True:
    DISPLAY_SURFACE.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                update_text("CLEAR")
            else:
                update_text(event.unicode)
    # updating position of texts
    marked_text_rect.center = pygame.mouse.get_pos()
    marked_text_rect.left = pygame.mouse.get_pos()[0]
    text_rect.center = pygame.mouse.get_pos()
    text_rect.left = marked_text_rect.right
    # blitting texts
    DISPLAY_SURFACE.blit(marked_text_surface, marked_text_rect)
    DISPLAY_SURFACE.blit(text_surface, text_rect)
    pygame.display.update()
    ticker.tick(MAX_FPS)


