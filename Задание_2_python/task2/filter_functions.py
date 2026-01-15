from typing import List, Callable


def filter_strings(filter_func: Callable[[str], bool], strings: List[str]) -> List[str]:
    """
    Фильтрует список строк с помощью функции-фильтра.
    
    Args:
        filter_func: Функция, принимающая строку и возвращающая bool
        strings: Список строк для фильтрации
        
    Returns:
        Отфильтрованный список строк
    """
    return [s for s in strings if filter_func(s)]


def main() -> None:
    """Примеры использования фильтров."""
    strings = [
        "apple", "banana", "apricot", "cherry", "blue berry",
        "kiwi", "orange", "ananas", "grapefruit"
    ]
    
    # 1. Исключить строки с пробелами
    no_spaces = filter_strings(lambda s: ' ' not in s, strings)
    print("Без пробелов:", no_spaces)
    
    # 2. Исключить строки, начинающиеся с 'a'
    no_a_start = filter_strings(lambda s: not s.lower().startswith('a'), strings)
    print("Не начинаются с 'a':", no_a_start)
    
    # 3. Исключить строки короче 5 символов
    min_length_5 = filter_strings(lambda s: len(s) >= 5, strings)
    print("Длина >= 5:", min_length_5)


if __name__ == "__main__":
    main()