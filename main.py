import tkinter as tk
from math3d import Vector3
from engine3d import Scene, Object3D, Mesh, Camera

class Renderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        
        # Создаем окно
        self.root = tk.Tk()
        self.root.title("3D Движок на Tkinter")
        
        # Создаем холст
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="black")
        self.canvas.pack()
        
        # Создаем сцену
        self.scene = Scene()
        self.scene.camera = Camera(position=Vector3(0, 0, -5))
        
        # Создаем куб
        self.create_cube()
        
        # Переменные для вращения
        self.rotation_y = 0
        self.rotation_x = 0
        
        # Привязываем клавиши
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
        
        # Запускаем цикл рендеринга
        self.render_loop()
    
    def create_cube(self):
        # Вершины куба
        vertices = [
            Vector3(-1, -1, -1),  # 0
            Vector3(1, -1, -1),   # 1
            Vector3(1, 1, -1),    # 2
            Vector3(-1, 1, -1),   # 3
            Vector3(-1, -1, 1),   # 4
            Vector3(1, -1, 1),    # 5
            Vector3(1, 1, 1),     # 6
            Vector3(-1, 1, 1)     # 7
        ]
        
        # Треугольники (грани) куба
        triangles = [
            # Передняя грань
            (0, 1, 2), (0, 2, 3),
            # Задняя грань
            (4, 6, 5), (4, 7, 6),
            # Левая грань
            (4, 0, 3), (4, 3, 7),
            # Правая грань
            (1, 5, 6), (1, 6, 2),
            # Верхняя грань
            (3, 2, 6), (3, 6, 7),
            # Нижняя грань
            (4, 5, 1), (4, 1, 0)
        ]
        
        # Создаем сетку
        cube_mesh = Mesh(vertices, triangles)
        
        # Создаем 3D объект
        cube = Object3D(cube_mesh, position=Vector3(0, 0, 0))
        
        # Добавляем объект на сцену
        self.scene.add_object(cube)
    
    def on_key_press(self, event):
        # Управление сценой с клавиатуры
        if event.keysym == "Left":
            self.scene.camera.rotation.y -= 0.1
        elif event.keysym == "Right":
            self.scene.camera.rotation.y += 0.1
        elif event.keysym == "Up":
            self.scene.camera.rotation.x -= 0.1
        elif event.keysym == "Down":
            self.scene.camera.rotation.x += 0.1
        elif event.keysym == "w":
            self.scene.camera.position.z += 0.2
        elif event.keysym == "s":
            self.scene.camera.position.z -= 0.2
        elif event.keysym == "a":
            self.scene.camera.position.x -= 0.2
        elif event.keysym == "d":
            self.scene.camera.position.x += 0.2
    
    def render(self):
        # Очищаем холст
        self.canvas.delete("all")
        
        # Рендерим сцену
        triangles = self.scene.render()
        
        # Преобразуем 3D координаты в 2D и рисуем
        for triangle in triangles:
            # Преобразуем координаты в 2D экранные координаты
            points = []
            for vertex in triangle:
                # Преобразуем нормализованные координаты в экранные
                x = int((vertex.x + 1) * self.width / 2)
                y = int((-vertex.y + 1) * self.height / 2)  # Инвертируем Y
                points.extend([x, y])
            
            # Рисуем треугольник
            if len(points) == 6:  # Убедимся, что у нас 3 точки
                self.canvas.create_polygon(points, outline="white", fill="", width=1)
    
    def render_loop(self):
        # Обновляем вращение куба
        self.rotation_y += 0.02
        self.rotation_x += 0.01
        
        # Применяем вращение к первому объекту (кубу)
        if self.scene.objects:
            self.scene.objects[0].rotation.y = self.rotation_y
            self.scene.objects[0].rotation.x = self.rotation_x
        
        # Рендерим сцену
        self.render()
        
        # Планируем следующий кадр
        self.root.after(30, self.render_loop)  # ~33 FPS
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    renderer = Renderer()
    renderer.run()