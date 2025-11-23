"""
Пример использования 3D-движка
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from engine import Engine3D
from objects.mesh import Cube
from math3d.vector3 import Vector3


def main():
    # Создаем движок
    engine = Engine3D(800, 600, "3D Engine Demo")
    
    # Создаем куб и добавляем его на сцену
    cube = Cube(Vector3(0, 0, -5), 2.0)  # Куб в позиции (0,0,-5) с размером 2
    engine.scene.add_object(cube)
    
    # Запускаем движок
    engine.run()


if __name__ == "__main__":
    main()