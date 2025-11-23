"""
Scene class for 3D Engine
"""
from .mesh import Mesh
from core.camera import Camera
from math3d.vector3 import Vector3


class Scene:
    def __init__(self):
        self.objects = []
        self.camera = Camera()
        self.lights = []
    
    def add_object(self, obj):
        """Добавление объекта в сцену"""
        if isinstance(obj, Mesh):
            self.objects.append(obj)
    
    def remove_object(self, obj):
        """Удаление объекта из сцены"""
        if obj in self.objects:
            self.objects.remove(obj)
    
    def add_light(self, light):
        """Добавление источника света"""
        self.lights.append(light)
    
    def update(self, delta_time):
        """Обновление сцены"""
        # В текущей реализации просто пропускаем время
        # В будущем можно добавить анимацию и физику
        pass
    
    def get_camera(self):
        """Получение камеры сцены"""
        return self.camera
    
    def set_camera(self, camera):
        """Установка камеры сцены"""
        self.camera = camera