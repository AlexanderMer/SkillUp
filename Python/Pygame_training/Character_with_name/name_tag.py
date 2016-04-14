import pygame
from pygame.locals import *
from colours import *

class name_tag:
    def __init__(self, name):
        self.name = name
        self.allowed_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM 1234567890_-!?"
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
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
        marked_text_surface = self.fontObj.render(self.marked_text_string, True, YELLOW, BLUE)
        marked_text_rect = marked_text_surface.get_rect()  # need to get after text changes, or textbox size won't change
        text_surface = self.fontObj.render(self.text_string, True, GREEN, BLUE)
        text_rect = text_surface.get_rect()