import time
from typing import Callable, Any


def measure_time(func: Callable) -> Callable:
    """
    Декоратор для измерения времени выполнения функции.
    
    Args:
        func: Декорируемая функция
        
    Returns:
        Обёрнутая функция, которая выводит время выполнения
    """
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()  # Засекаем начальное время
        result = func(*args, **kwargs)  # Выполняем декорируемую функцию
        end_time = time.time()  # Засекаем конечное время
        
        # Выводим время выполнения в консоль
        execution_time = end_time - start_time
        if execution_time < 0.000001:
            time_str = f"{execution_time:.6f}"
        else:
            time_str = f"{execution_time:.6f}"
        print(f"Функция '{func.__name__}' выполнилась за {time_str} секунд")
        return result
    return wrapper


@measure_time
def sum_and_print(a: int, b: int) -> int:
    """
    Функция вычисляет сумму двух чисел и выводит результат в консоль.
    
    Args:
        a: Первое число
        b: Второе число
        
    Returns:
        Сумма a и b
    """
    result = a + b
    print(f"Сумма {a} и {b} равна {result}")
    return result


@measure_time
def read_from_file_and_write() -> None:
    """
    Функция читает два числа из файла input.txt,
    вычисляет их сумму и записывает результат в файл output.txt
    """
    try:
        # Чтение чисел из файла
        with open('input.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # Фильтрация пустых строк
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            
            if len(non_empty_lines) < 2:
                raise ValueError(f"Файл должен содержать как минимум два числа. Найдено: {len(non_empty_lines)}")
            
            # Берем первые два непустых значения
            a_str = non_empty_lines[0]
            b_str = non_empty_lines[1]
            
            # Пробуем преобразовать в числа
            try:
                a = int(a_str)
            except ValueError:
                print(f"Ошибка: Первое значение '{a_str}' не является целым числом")
                return
                
            try:
                b = int(b_str)
            except ValueError:
                print(f"Ошибка: Второе значение '{b_str}' не является целым числом")
                return
        
        # Вычисление суммы
        result = a + b
        
        # Запись результата в файл
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(str(result))
        
        print(f"Результат {a} + {b} = {result} записан в output.txt")
    
    except FileNotFoundError:
        print("Ошибка: Файл input.txt не найден")
        print("Пожалуйста, создайте файл input.txt с двумя числами (по одному на строку)")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


# Дополнительная функция для демонстрации декоратора
@measure_time
def complex_calculation() -> float:
    """
    Функция выполняет сложные вычисления для демонстрации работы декоратора
    """
    print("Выполнение сложных вычислений...")
    time.sleep(0.1)  # Имитация долгой работы
    result = 0.0
    for i in range(10000):
        result += i * 0.01
    print(f"    Результат: {result:.4f}")
    return result


def create_example_input_file() -> None:
    """
    Создание примера файла input.txt с корректными данными
    """
    try:
        with open('input.txt', 'w', encoding='utf-8') as file:
            file.write("10\n")
            file.write("20\n")
        print("Создан пример файла input.txt с числами 10 и 20")
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")


if __name__ == "__main__":
    # Создаем пример файла если его нет
    try:
        with open('input.txt', 'r', encoding='utf-8'):
            pass
    except FileNotFoundError:
        create_example_input_file()
    
    print("=" * 50)
    print("Демонстрация работы декоратора на сложной функции:")
    complex_calculation()
    print()
    
    print("=" * 50)
    print("Тест 1: Сумма двух чисел")
    sum_and_print(5, 3)
    print()
    
    print("=" * 50)
    print("Тест 2: Чтение из файла и запись в файл")
    read_from_file_and_write()
    print()
    
    # Показываем содержимое output.txt если он существует
    try:
        with open('output.txt', 'r', encoding='utf-8') as file:
            result = file.read()
            print(f"Содержимое output.txt: {result}")
    except FileNotFoundError:
        print("Файл output.txt не создан")