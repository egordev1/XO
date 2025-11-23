"""
3D Vector class for 3D Engine
"""
import math


class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        """Сложение векторов"""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        """Вычитание векторов"""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        """Умножение вектора на скаляр"""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        """Умножение вектора на скаляр (в другом порядке)"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        """Деление вектора на скаляр"""
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def length(self):
        """Длина вектора"""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        """Нормализация вектора"""
        length = self.length()
        if length == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / length, self.y / length, self.z / length)
    
    def dot(self, other):
        """Скалярное произведение"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        """Векторное произведение"""
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
    
    def to_tuple(self):
        """Преобразование в кортеж"""
        return (self.x, self.y, self.z)