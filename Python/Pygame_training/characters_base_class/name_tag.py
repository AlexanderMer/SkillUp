import pygame
from pygame.locals import *
from colours import *

class Name_tag:
    def __init__(self, name, screen, font='freesansbold.ttf', font_size=30):
        self.screen = screen
        self.NAME = name
        self.name = name
        self.allowed_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_-!?"
        self.fontObj = pygame.font.Font(font, font_size)
        self.marked_text_string = ""
        self.text_surface = self.fontObj.render(self.name, True, GREEN, BLUE)
        self.marked_text_surface = self.fontObj.render(self.marked_text_string, True, YELLOW, BLUE)
        self.text_rect = self.text_surface.get_rect()
        self.marked_text_rect = self.marked_text_surface.get_rect()

    def update_text(self, char):
        if self.name == "" or self.name[0] != char:
            return
        self.marked_text_string += self.text_string[0]
        self.text_string = self.text_string[1:]
        self.marked_text_surface = self.fontObj.render(self.marked_text_string, True, YELLOW, BLUE)
        self.marked_text_rect = self.marked_text_surface.get_rect()  # need to get after text changes, or textbox size won't change
        self.text_surface = self.fontObj.render(self.text_string, True, GREEN, BLUE)
        self.text_rect = self.text_surface.get_rect()

    def update_pos(self, center):
        """Places text relevant to center coordinates"""
        self.marked_text_rect.center = center
        self.marked_text_rect.left = center[0]
        self.text_rect.center = center
        self.text_rect.left = self.marked_text_rect.right

    def render(self):
        self.screen.blit(self.marked_text_surface, self.marked_text_rect)
        self.screen.blit(self.text_surface, self.text_rect)
