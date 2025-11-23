from math3d import Vector3, matrix_multiply_vector, rotation_matrix_x, rotation_matrix_y, rotation_matrix_z, translation_matrix, perspective_matrix

class Camera:
    def __init__(self, position=Vector3(0, 0, -5), rotation=Vector3(0, 0, 0)):
        self.position = position
        self.rotation = rotation  # Углы поворота (в радианах)
        self.fov = 90  # Угол обзора
        self.near = 0.1  # Ближняя плоскость
        self.far = 100  # Дальняя плоскость

    def get_view_matrix(self):
        """Возвращает матрицу вида (обратная матрица трансформации камеры)"""
        # Матрица поворота
        rot_x = rotation_matrix_x(-self.rotation.x)
        rot_y = rotation_matrix_y(-self.rotation.y)
        rot_z = rotation_matrix_z(-self.rotation.z)
        
        # Объединяем повороты
        rotation_matrix_final = self.multiply_matrices(rot_y, self.multiply_matrices(rot_x, rot_z))
        
        # Матрица переноса (инвертируем позицию)
        translation = translation_matrix(-self.position.x, -self.position.y, -self.position.z)
        
        # Объединяем поворот и перенос
        return self.multiply_matrices(rotation_matrix_final, translation)

    def multiply_matrices(self, m1, m2):
        """Умножение двух 4x4 матриц"""
        result = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += m1[i][k] * m2[k][j]
        return result

class Mesh:
    def __init__(self, vertices, triangles):
        self.vertices = vertices  # Список Vector3
        self.triangles = triangles  # Список кортежей индексов вершин

    def get_transformed_vertices(self, world_matrix):
        """Применяет матрицу трансформации к вершинам"""
        transformed_vertices = []
        for vertex in self.vertices:
            # Применяем трансформацию
            transformed_vertex = matrix_multiply_vector(world_matrix, vertex)
            transformed_vertices.append(transformed_vertex)
        return transformed_vertices

class Object3D:
    def __init__(self, mesh, position=Vector3(), rotation=Vector3()):
        self.mesh = mesh
        self.position = position
        self.rotation = rotation

    def get_world_matrix(self):
        """Возвращает матрицу трансформации объекта в мировом пространстве"""
        # Матрица поворота
        rot_x = rotation_matrix_x(self.rotation.x)
        rot_y = rotation_matrix_y(self.rotation.y)
        rot_z = rotation_matrix_z(self.rotation.z)
        
        # Объединяем повороты
        rotation_matrix_final = self.multiply_matrices(rot_y, self.multiply_matrices(rot_x, rot_z))
        
        # Матрица переноса
        translation = translation_matrix(self.position.x, self.position.y, self.position.z)
        
        # Объединяем поворот и перенос
        return self.multiply_matrices(rotation_matrix_final, translation)

    def multiply_matrices(self, m1, m2):
        """Умножение двух 4x4 матриц"""
        result = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += m1[i][k] * m2[k][j]
        return result

class Scene:
    def __init__(self):
        self.objects = []
        self.camera = Camera()

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        """Возвращает отрендеренные треугольники в 2D координатах"""
        rendered_triangles = []
        
        # Получаем матрицы вида и проекции
        view_matrix = self.camera.get_view_matrix()
        aspect_ratio = 1.0  # Предполагаем квадратный экран
        proj_matrix = perspective_matrix(
            self.camera.fov * 3.14159 / 180,  # Переводим в радианы
            aspect_ratio,
            self.camera.near,
            self.camera.far
        )
        
        for obj in self.objects:
            # Получаем мировую матрицу объекта
            world_matrix = obj.get_world_matrix()
            
            # Объединяем все матрицы: проекция * вид * мировая
            view_world_matrix = self.multiply_matrices(view_matrix, world_matrix)
            final_matrix = self.multiply_matrices(proj_matrix, view_world_matrix)
            
            # Преобразуем вершины
            transformed_vertices = obj.mesh.get_transformed_vertices(final_matrix)
            
            # Преобразуем треугольники
            for triangle in obj.mesh.triangles:
                # Получаем вершины треугольника
                v1 = transformed_vertices[triangle[0]]
                v2 = transformed_vertices[triangle[1]]
                v3 = transformed_vertices[triangle[2]]
                
                # Добавляем в результат
                rendered_triangles.append((v1, v2, v3))
        
        return rendered_triangles

    def multiply_matrices(self, m1, m2):
        """Умножение двух 4x4 матриц"""
        result = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += m1[i][k] * m2[k][j]
        return result