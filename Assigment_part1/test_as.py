import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def rotate(self, a, angle):
        deltX = self.x
        deltY = self.y
        self.x = a.get_x() + (deltX - a.get_x()) * math.cos(angle) - (deltY - a.get_y()) * math.sin(angle)
        self.y = a.get_y() + (deltX - a.get_x()) * math.sin(angle) + (deltY - a.get_y()) * math.cos(angle)

    @staticmethod
    def length(a, b):
        return math.sqrt((a.get_x() - b.get_x()) ** 2 + (a.get_y() - b.get_y()) ** 2)


class Shape:
    def center(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def area(self):
        raise NotImplementedError

    def translate(self, new_center):
        raise NotImplementedError

    def rotate(self, angle):
        raise NotImplementedError

    def scale(self, coefficient):
        raise NotImplementedError


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def sides(self):
        return [self.a, self.b, self.c]

    def area(self):
        # Формула Герона для вычисления площади треугольника
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right_triangle(self):
        # Проверка, является ли треугольник прямоугольным
        sides = sorted([self.a, self.b, self.c])
        return math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2)


# Метод для вычисления площади круга по радиусу
def calculate_circle_area(radius):
    return math.pi * radius ** 2


class Ellipse(Shape):
    def __init__(self, A, B, perifocal_distance):
        self.A = A
        self.B = B
        self.perifocal_distance = perifocal_distance

    def focuses(self):
        return [self.A, self.B]

    def focal_distance(self):
        return Point.length(self.A, self.B) / 2

    def major_semi_axis(self):
        return self.focal_distance() + self.perifocal_distance

    def minor_semi_axis(self):
        return math.sqrt(self.major_semi_axis() ** 2 - self.focal_distance() ** 2)

    def eccentricity(self):
        return self.focal_distance() / self.major_semi_axis()

    def center(self):
        return Point((self.A.get_x() + self.B.get_x()) / 2, (self.A.get_y() + self.B.get_y()) / 2)

    def perimeter(self):
        a = self.major_semi_axis()
        b = self.minor_semi_axis()
        return (4 * math.pi * a * b + 4 * (a - b) * (a - b)) / (a + b)

    def area(self):
        return math.pi * self.minor_semi_axis() * self.major_semi_axis()

    def translate(self, new_center):
        moved_x = new_center.get_x() - self.center().get_x()
        moved_y = new_center.get_y() - self.center().get_y()
        self.A = Point(self.A.get_x() + moved_x, self.A.get_y() + moved_y)
        self.B = Point(self.B.get_x() + moved_x, self.B.get_y() + moved_y)

    def rotate(self, angle):
        pred_cent = self.center()
        self.B.rotate(pred_cent, angle)
        self.A.rotate(pred_cent, angle)

    def scale(self, coefficient):
        pre_centre = self.center()
        self.A = Point(pre_centre.get_x() + coefficient * (self.A.get_x() - pre_centre.get_x()),
                       pre_centre.get_y() + coefficient * (self.A.get_y() - pre_centre.get_y()))
        self.B = Point(pre_centre.get_x() + coefficient * (self.B.get_x() - pre_centre.get_x()),
                       pre_centre.get_y() + coefficient * (self.B.get_y() - pre_centre.get_y()))
        self.perifocal_distance *= abs(coefficient)


class Circle(Ellipse):
    def __init__(self, center, radius):
        super().__init__(center, center, radius)
        self.radius = radius

    def area(self):
        return calculate_circle_area(self.radius)


# Универсальный метод для вычисления площади фигуры
def calculate_area(shape):
    return shape.area()
