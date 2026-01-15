import math
from abc import ABC, abstractmethod


# Абстрактный базовый класс для фигур
class Shape(ABC):
    @abstractmethod
    def area(self):
        """Вычисление площади"""
        pass

    @abstractmethod
    def perimeter(self):
        """Вычисление периметра"""
        pass

    def compare_area(self, other_shape):
        """Сравнение площади с другой фигурой"""
        if self.area() > other_shape.area():
            return "больше"
        elif self.area() < other_shape.area():
            return "меньше"
        else:
            return "равна"

    def compare_perimeter(self, other_shape):
        """Сравнение периметра с другой фигурой"""
        if self.perimeter() > other_shape.perimeter():
            return "больше"
        elif self.perimeter() < other_shape.perimeter():
            return "меньше"
        else:
            return "равна"


# Класс Квадрат
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side


# Класс Прямоугольник
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


# Класс Треугольник
class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        # Формула Герона
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


# Класс Круг
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


# Демонстрация работы классов фигур
if __name__ == "__main__":
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССОВ ФИГУР")
    print("=" * 50)

    # Создание фигур
    square = Square(5)
    rectangle = Rectangle(4, 6)
    triangle = Triangle(3, 4, 5)
    circle = Circle(3)

    # Вычисление площадей
    print(f"Площадь квадрата: {square.area()}")
    print(f"Площадь прямоугольника: {rectangle.area()}")
    print(f"Площадь треугольника: {triangle.area():.2f}")
    print(f"Площадь круга: {circle.area():.2f}")
    print()

    # Вычисление периметров
    print(f"Периметр квадрата: {square.perimeter()}")
    print(f"Периметр прямоугольника: {rectangle.perimeter()}")
    print(f"Периметр треугольника: {triangle.perimeter()}")
    print(f"Периметр круга: {circle.perimeter():.2f}")
    print()

    # Сравнение площадей
    print(f"Площадь квадрата {square.compare_area(rectangle)} площади прямоугольника")
    print(f"Площадь круга {circle.compare_area(triangle)} площади треугольника")
    print()

    # Сравнение периметров
    print(f"Периметр квадрата {square.compare_perimeter(rectangle)} периметра прямоугольника")
    print(f"Периметр треугольника {triangle.compare_perimeter(circle)} периметра круга")