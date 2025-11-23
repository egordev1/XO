"""
Renderer class for 3D Engine
"""
import pygame
from math3d.vector3 import Vector3
from math3d.matrix4x4 import Matrix4x4


class Renderer:
    def __init__(self, window):
        self.window = window
        self.screen = window.get_surface()
        self.width = window.width
        self.height = window.height
        
        # Цвет фона
        self.clear_color = (0, 0, 0)
    
    def clear(self):
        """Очистка экрана"""
        self.screen.fill(self.clear_color)
    
    def project_vertex(self, vertex, view_matrix, projection_matrix):
        """Проекция вершины из 3D в 2D"""
        # Применение матрицы вида
        view_vertex = view_matrix * vertex
        
        # Применение матрицы проекции
        proj_vertex = projection_matrix * view_vertex
        
        # Перевод в экранное пространство
        if proj_vertex.z != 0:  # Избегаем деления на 0
            x = proj_vertex.x / proj_vertex.z
            y = proj_vertex.y / proj_vertex.z
        else:
            x = proj_vertex.x
            y = proj_vertex.y
        
        # Преобразование в экранные координаты
        screen_x = int((x + 1) * 0.5 * self.width)
        screen_y = int((1 - y) * 0.5 * self.height)  # Инвертируем Y
        
        return (screen_x, screen_y)
    
    def draw_line(self, start, end, color=(255, 255, 255)):
        """Рисование линии между двумя точками"""
        pygame.draw.line(self.screen, color, start, end, 1)
    
    def render_triangle(self, v1, v2, v3, color=(255, 255, 255)):
        """Рендеринг треугольника"""
        # Проекция вершин в 2D
        p1 = self.project_vertex(v1, self.view_matrix, self.projection_matrix)
        p2 = self.project_vertex(v2, self.view_matrix, self.projection_matrix)
        p3 = self.project_vertex(v3, self.view_matrix, self.projection_matrix)
        
        # Рисование треугольника как каркаса
        self.draw_line(p1, p2, color)
        self.draw_line(p2, p3, color)
        self.draw_line(p3, p1, color)
    
    def render_mesh(self, mesh, camera):
        """Рендеринг меша"""
        # Получаем текущие матрицы камеры
        self.view_matrix = camera.view_matrix
        self.projection_matrix = camera.projection_matrix
        
        # Рендерим каждый треугольник меша
        for i in range(len(mesh.triangles)):
            triangle = mesh.get_world_triangle(i)
            if triangle:
                v1, v2, v3 = triangle
                self.render_triangle(v1, v2, v3)
    
    def render(self, scene):
        """Рендеринг сцены"""
        # Получаем камеру сцены
        camera = scene.get_camera()
        
        # Рендерим каждый объект на сцене
        for obj in scene.objects:
            self.render_mesh(obj, camera)