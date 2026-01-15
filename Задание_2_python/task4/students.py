# Базовый класс Человек
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_info(self):
        """Вывести информацию о человеке"""
        print(f"ФИО: {self.name}, Возраст: {self.age}")


# Класс Студент
class Student(Person):
    def __init__(self, name, age, group_number, average_score):
        super().__init__(name, age)
        self.group_number = group_number
        self.average_score = average_score

    def calculate_scholarship(self):
        """Вычисление стипендии"""
        if self.average_score == 5:
            return 6000
        elif self.average_score < 5:
            return 4000
        else:
            return 0

    def print_scholarship(self):
        """Вывести размер стипендии"""
        print(f"Стипендия: {self.calculate_scholarship()} руб.")

    def compare_scholarship(self, other_student):
        """Сравнение стипендии с другим студентом/аспирантом"""
        scholarship1 = self.calculate_scholarship()
        scholarship2 = other_student.calculate_scholarship()

        if scholarship1 > scholarship2:
            return "больше"
        elif scholarship1 < scholarship2:
            return "меньше"
        else:
            return "равна"


# Класс Аспирант
class GraduateStudent(Student):
    def __init__(self, name, age, group_number, average_score, research_work):
        super().__init__(name, age, group_number, average_score)
        self.research_work = research_work

    def calculate_scholarship(self):
        """Вычисление стипендии для аспиранта"""
        if self.average_score == 5:
            return 8000
        elif self.average_score < 5:
            return 6000
        else:
            return 0

    def print_info(self):
        """Вывести информацию о человеке (с учетом научной работы)"""
        super().print_info()
        print(f"Научная работа: {self.research_work}")


# Демонстрация работы классов студентов
if __name__ == "__main__":
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССОВ СТУДЕНТОВ")
    print("=" * 50)

    # Создание студентов
    student1 = Student("Иванов Иван Иванович", 20, "Группа 101", 4.8)
    student2 = Student("Петров Петр Петрович", 21, "Группа 102", 5.0)
    graduate = GraduateStudent("Сидоров Алексей Сергеевич", 25, "Аспиранты", 5.0,
                               "Исследование алгоритмов машинного обучения")

    # Вывод информации о студентах
    print("Студент 1:")
    student1.print_info()
    print(f"Номер группы: {student1.group_number}, Средний балл: {student1.average_score}")
    student1.print_scholarship()
    print()

    print("Студент 2:")
    student2.print_info()
    print(f"Номер группы: {student2.group_number}, Средний балл: {student2.average_score}")
    student2.print_scholarship()
    print()

    print("Аспирант:")
    graduate.print_info()
    print(f"Номер группы: {graduate.group_number}, Средний балл: {graduate.average_score}")
    graduate.print_scholarship()
    print()

    # Сравнение стипендий
    print("Сравнение стипендий:")
    print(f"Стипендия {student1.name} {student1.compare_scholarship(student2)} стипендии {student2.name}")
    print(f"Стипендия {graduate.name} {graduate.compare_scholarship(student1)} стипендии {student1.name}")
    print(f"Стипендия {student2.name} {student2.compare_scholarship(graduate)} стипендии {graduate.name}")

    # Дополнительные примеры
    print("\n" + "=" * 30)
    print("ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ")
    print("=" * 30)
    
    # Студент с низким средним баллом
    student3 = Student("Козлов Дмитрий Сергеевич", 22, "Группа 103", 3.5)
    print("\nСтудент 3:")
    student3.print_info()
    student3.print_scholarship()
    
    # Аспирант с низким средним баллом
    graduate2 = GraduateStudent("Николаев Андрей Петрович", 26, "Аспиранты", 4.2,
                                "Анализ больших данных")
    print("\nАспирант 2:")
    graduate2.print_info()
    graduate2.print_scholarship()