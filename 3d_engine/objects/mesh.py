"""
Mesh class for 3D Engine
"""
from math3d.vector3 import Vector3
from math3d.matrix4x4 import Matrix4x4


class Mesh:
    def __init__(self, vertices=None, triangles=None, position=Vector3(0, 0, 0), rotation=Vector3(0, 0, 0), scale=Vector3(1, 1, 1)):
        self.vertices = vertices or []
        self.triangles = triangles or []  # Список индексов вершин для треугольников
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
        # Матрица трансформации объекта
        self.model_matrix = self.calculate_model_matrix()
    
    def calculate_model_matrix(self):
        """Вычисление матрицы модели"""
        # Матрица масштабирования
        scale_matrix = Matrix4x4.scale(self.scale.x, self.scale.y, self.scale.z)
        
        # Матрицы вращения
        rot_x = Matrix4x4.rotation_x(self.rotation.x)
        rot_y = Matrix4x4.rotation_y(self.rotation.y)
        rot_z = Matrix4x4.rotation_z(self.rotation.z)
        rotation_matrix = rot_z * rot_y * rot_x
        
        # Матрица переноса
        translation_matrix = Matrix4x4.translation(self.position.x, self.position.y, self.position.z)
        
        # Комбинирование матриц: T * R * S
        return translation_matrix * rotation_matrix * scale_matrix
    
    def update_transform(self):
        """Обновление матрицы трансформации"""
        self.model_matrix = self.calculate_model_matrix()
    
    def move(self, offset):
        """Перемещение объекта"""
        self.position = self.position + offset
        self.update_transform()
    
    def rotate(self, rotation):
        """Вращение объекта"""
        self.rotation = self.rotation + rotation
        self.update_transform()
    
    def set_scale(self, scale):
        """Установка масштаба"""
        self.scale = scale
        self.update_transform()
    
    def get_world_vertex(self, vertex_index):
        """Получение вершины в мировых координатах"""
        if vertex_index < len(self.vertices):
            vertex = self.vertices[vertex_index]
            # Применение матрицы модели к вершине
            return self.model_matrix * vertex
        return None
    
    def get_world_triangle(self, triangle_index):
        """Получение треугольника в мировых координатах"""
        if triangle_index < len(self.triangles):
            indices = self.triangles[triangle_index]
            if len(indices) == 3:
                v1 = self.get_world_vertex(indices[0])
                v2 = self.get_world_vertex(indices[1])
                v3 = self.get_world_vertex(indices[2])
                return (v1, v2, v3)
        return None


class Cube(Mesh):
    """Класс куба"""
    def __init__(self, position=Vector3(0, 0, 0), size=1.0):
        # Определяем вершины куба
        s = size / 2
        vertices = [
            Vector3(-s, -s, -s),  # 0
            Vector3(s, -s, -s),   # 1
            Vector3(s, s, -s),    # 2
            Vector3(-s, s, -s),   # 3
            Vector3(-s, -s, s),   # 4
            Vector3(s, -s, s),    # 5
            Vector3(s, s, s),     # 6
            Vector3(-s, s, s)     # 7
        ]
        
        # Определяем треугольники (грани куба)
        triangles = [
            [0, 1, 2], [0, 2, 3],  # Передняя грань
            [4, 6, 5], [4, 7, 6],  # Задняя грань
            [0, 4, 1], [1, 4, 5],  # Нижняя грань
            [2, 6, 7], [2, 7, 3],  # Верхняя грань
            [0, 3, 7], [0, 7, 4],  # Левая грань
            [1, 5, 6], [1, 6, 2]   # Правая грань
        ]
        
        super().__init__(vertices, triangles, position)