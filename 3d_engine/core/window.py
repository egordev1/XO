"""
Window module for 3D Engine
"""
import pygame


class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        
        # Создание окна Pygame
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
    def get_surface(self):
        """Возвращает поверхность окна для рендеринга"""
        return self.screen
        
    def resize(self, width, height):
        """Изменение размера окна"""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))