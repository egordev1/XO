"""
Camera class for 3D Engine
"""
from math3d.vector3 import Vector3
from math3d.matrix4x4 import Matrix4x4
import math


class Camera:
    def __init__(self, position=Vector3(0, 0, 0), target=Vector3(0, 0, -1), up=Vector3(0, 1, 0)):
        self.position = position
        self.target = target
        self.up = up
        self.view_matrix = Matrix4x4.identity()
        self.projection_matrix = Matrix4x4.perspective(math.radians(45), 800/600, 0.1, 100.0)
        self.update_view_matrix()
    
    def update_view_matrix(self):
        """Обновление матрицы вида"""
        # Вектор направления взгляда
        forward = (self.target - self.position).normalize()
        
        # Правый вектор
        right = forward.cross(self.up).normalize()
        
        # Перпендикулярный вектор "вверх"
        up = right.cross(forward).normalize()
        
        # Создание матрицы вида
        self.view_matrix = Matrix4x4([
            [right.x, right.y, right.z, -right.dot(self.position)],
            [up.x, up.y, up.z, -up.dot(self.position)],
            [-forward.x, -forward.y, -forward.z, forward.dot(self.position)],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    def look_at(self, target):
        """Установка направления взгляда на цель"""
        self.target = target
        self.update_view_matrix()
    
    def set_position(self, position):
        """Установка позиции камеры"""
        self.position = position
        self.update_view_matrix()
    
    def move(self, offset):
        """Перемещение камеры"""
        self.position = self.position + offset
        self.target = self.target + offset
        self.update_view_matrix()
    
    def rotate_around_point(self, point, angle_x, angle_y):
        """Вращение камеры вокруг точки"""
        # Смещение камеры относительно точки
        offset = self.position - point
        
        # Применение вращения к смещению
        # Вращение по Y
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        new_x = offset.x * cos_y - offset.z * sin_y
        new_z = offset.x * sin_y + offset.z * cos_y
        offset = Vector3(new_x, offset.y, new_z)
        
        # Вращение по X
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        new_y = offset.y * cos_x - offset.z * sin_x
        new_z = offset.y * sin_x + offset.z * cos_x
        offset = Vector3(offset.x, new_y, new_z)
        
        # Новая позиция камеры
        self.position = point + offset
        
        # Обновление направления взгляда
        self.target = point
        self.update_view_matrix()