"""
4x4 Matrix class for 3D transformations
"""
import math
from .vector3 import Vector3


class Matrix4x4:
    def __init__(self, data=None):
        if data is None:
            # Инициализация единичной матрицы
            self.data = [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ]
        else:
            self.data = data
    
    @staticmethod
    def identity():
        """Возвращает единичную матрицу"""
        return Matrix4x4()
    
    @staticmethod
    def translation(x, y, z):
        """Матрица переноса"""
        return Matrix4x4([
            [1.0, 0.0, 0.0, x],
            [0.0, 1.0, 0.0, y],
            [0.0, 0.0, 1.0, z],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def rotation_x(angle):
        """Матрица вращения вокруг оси X"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Matrix4x4([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, cos_a, -sin_a, 0.0],
            [0.0, sin_a, cos_a, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def rotation_y(angle):
        """Матрица вращения вокруг оси Y"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Matrix4x4([
            [cos_a, 0.0, sin_a, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-sin_a, 0.0, cos_a, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def rotation_z(angle):
        """Матрица вращения вокруг оси Z"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Matrix4x4([
            [cos_a, -sin_a, 0.0, 0.0],
            [sin_a, cos_a, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def scale(sx, sy, sz):
        """Матрица масштабирования"""
        return Matrix4x4([
            [sx, 0.0, 0.0, 0.0],
            [0.0, sy, 0.0, 0.0],
            [0.0, 0.0, sz, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def perspective(fov, aspect, near, far):
        """Матрица перспективной проекции"""
        tan_half_fov = math.tan(fov / 2)
        z_range = near - far
        
        return Matrix4x4([
            [1.0 / (aspect * tan_half_fov), 0.0, 0.0, 0.0],
            [0.0, 1.0 / tan_half_fov, 0.0, 0.0],
            [0.0, 0.0, (far + near) / z_range, (2 * far * near) / z_range],
            [0.0, 0.0, -1.0, 0.0]
        ])
    
    @staticmethod
    def orthographic(left, right, bottom, top, near, far):
        """Матрица ортографической проекции"""
        width = right - left
        height = top - bottom
        depth = far - near
        
        return Matrix4x4([
            [2.0 / width, 0.0, 0.0, -(right + left) / width],
            [0.0, 2.0 / height, 0.0, -(top + bottom) / height],
            [0.0, 0.0, -2.0 / depth, -(far + near) / depth],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    def __mul__(self, other):
        """Умножение матриц"""
        if isinstance(other, Matrix4x4):
            result = [[0.0 for _ in range(4)] for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        result[i][j] += self.data[i][k] * other.data[k][j]
            return Matrix4x4(result)
        elif isinstance(other, Vector3):
            # Умножение матрицы на вектор
            x = (self.data[0][0] * other.x + self.data[0][1] * other.y + 
                 self.data[0][2] * other.z + self.data[0][3])
            y = (self.data[1][0] * other.x + self.data[1][1] * other.y + 
                 self.data[1][2] * other.z + self.data[1][3])
            z = (self.data[2][0] * other.x + self.data[2][1] * other.y + 
                 self.data[2][2] * other.z + self.data[2][3])
            w = (self.data[3][0] * other.x + self.data[3][1] * other.y + 
                 self.data[3][2] * other.z + self.data[3][3])
            
            # Перевод из однородных координат в декартовы
            if w != 0:
                x /= w
                y /= w
                z /= w
            
            return Vector3(x, y, z)
    
    def __str__(self):
        """Строковое представление матрицы"""
        result = "Matrix4x4:\n"
        for row in self.data:
            result += f"  {row}\n"
        return result