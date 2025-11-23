"""
Main 3D Engine class
"""
import pygame
import sys
from core.window import Window
from render.renderer import Renderer
from objects.scene import Scene
from math3d.vector3 import Vector3


class Engine3D:
    def __init__(self, width=800, height=600, title="3D Engine"):
        self.width = width
        self.height = height
        self.title = title
        
        # Инициализация Pygame
        pygame.init()
        
        # Создание окна
        self.window = Window(self.width, self.height, self.title)
        
        # Создание рендерера
        self.renderer = Renderer(self.window)
        
        # Создание сцены
        self.scene = Scene()
        
        # Время для анимации
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        """Основной цикл движка"""
        while self.running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Очистка сцены
            self.renderer.clear()
            
            # Обновление сцены
            self.scene.update(self.clock.get_time() / 1000.0)
            
            # Рендеринг сцены
            self.renderer.render(self.scene)
            
            # Обновление дисплея
            pygame.display.flip()
            
            # Ограничение FPS
            self.clock.tick(60)
        
        # Завершение работы
        self.cleanup()
    
    def cleanup(self):
        """Очистка ресурсов"""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    engine = Engine3D()
    engine.run()