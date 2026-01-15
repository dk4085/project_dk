def is_palindrome(text: str) -> bool:
    """
    Проверяет, является ли строка палиндромом.
    
    Args:
        text (str): Входная строка для проверки
        
    Returns:
        bool: True если строка палиндром, иначе False
    """
    # Убираем пробелы и приводим к нижнему регистру
    cleaned_text = ''.join(text.lower().split())
    return cleaned_text == cleaned_text[::-1]


if __name__ == "__main__":
    # Примеры использования
    test_cases = ["А роза упала на лапу Азора", "hello", "level", ""]
    for test in test_cases:
        print(f"'{test}' -> {is_palindrome(test)}")