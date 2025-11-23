import math

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / length, self.y / length, self.z / length)

def matrix_multiply_vector(matrix, vector):
    """Умножение 4x4 матрицы на 3D вектор (с w=1)"""
    x = matrix[0][0]*vector.x + matrix[0][1]*vector.y + matrix[0][2]*vector.z + matrix[0][3]
    y = matrix[1][0]*vector.x + matrix[1][1]*vector.y + matrix[1][2]*vector.z + matrix[1][3]
    z = matrix[2][0]*vector.x + matrix[2][1]*vector.y + matrix[2][2]*vector.z + matrix[2][3]
    w = matrix[3][0]*vector.x + matrix[3][1]*vector.y + matrix[3][2]*vector.z + matrix[3][3]
    
    # Перспективное деление
    if w != 0:
        x /= w
        y /= w
        z /= w
    
    return Vector3(x, y, z)

def rotation_matrix_x(angle):
    """Матрица поворота вокруг оси X"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ]

def rotation_matrix_y(angle):
    """Матрица поворота вокруг оси Y"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ]

def rotation_matrix_z(angle):
    """Матрица поворота вокруг оси Z"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

def translation_matrix(x, y, z):
    """Матрица переноса"""
    return [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]

def perspective_matrix(fov, aspect_ratio, near, far):
    """Матрица перспективной проекции"""
    f = 1 / math.tan(fov / 2)
    return [
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ]