from typing import List

# Возвращает число, записанное в обратном порядке цифр
def reverse_number(n: int) -> int:
    """
    Возвращает число, записанное в обратном порядке цифр.

    Parameters:
        :param n: исходное целое число.

    Returns:
        :return: число с перевернутым порядком цифр.

    Examples:
    >>> reverse_number(123)
    321
    >>> reverse_number(400)
    4
    """

    result = int(str(n)[::-1])
    logger.debug(f"reverse_number: {n} -> {result}")   # вспомогательная функция, не засоряет лог
    return result


# количество общих чисел в двух массивах
def count_common_and_reversed(arr1: List[int], arr2: List[int]) -> int:
    """
    Подсчитывает количество общих чисел между двумя массивами,
    учитывая также перевёрнутые значения.

    Каждая пара чисел учитывается только один раз,
    даже если такие значения встречаются несколько раз в массивах.

    Parameters:
        :param arr1: первый массив целых чисел
        :param arr2: второй массив целых чисел
        :return: количество уникальных общих чисел между массивами

    Raises
        :raises ValueError: если один или оба массива пустые

    Examples
    >>> count_common_and_reversed([12, 34, 56], [21, 43, 78])
    2

    >>> count_common_and_reversed([10, 20, 30], [1, 2, 3])
    3

    >>> count_common_and_reversed([12, 12], [21, 21])
    1
    """

    if not arr1 or not arr2:
        raise ValueError("Массивы не заданы или пусты")   # прерывает выполнение функции, если данные некорректны

    count = 0
    used_pairs = []

    for a in arr1:
        for b in arr2:
            if a == b or a == reverse_number(b) or reverse_number(a) == b:
                pair = (min(a, b), max(a, b))
                if pair not in used_pairs:
                    used_pairs.append(pair)
                    count += 1

    return count


def find_common_numbers(arr1: List[int], arr2: List[int]) -> int:
    """
    Определяет количество общих чисел между двумя массивами,
    учитывая перевёрнутые числа.

    Использует функции:
        - reverse_number(n): возвращает число с перевёрнутыми цифрами
        - count_common_and_reversed(arr1, arr2): подсчитывает общие числа

    Parameters:
        :param arr1: первый массив целых чисел
        :param arr2: второй массив целых чисел
    Returns:
        :return: количество уникальных общих чисел
    Raises:
        :raises ValueError: если один или оба массива пустые
    """

    logger.info("Вызов find_common_numbers()")

    if not arr1 or not arr2:
        logger.error("Массивы не заданы или пусты")
        raise ValueError("Массивы не заданы или пусты")

    count = count_common_and_reversed(arr1, arr2)
    logger.info(f"Количество общих чисел (с учётом перевёрнутых): {count}")
    return count