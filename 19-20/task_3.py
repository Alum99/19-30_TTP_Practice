from typing import List

# сортировка массивов по условиям
def sort_arrays(arr1: List[int], arr2: List[int]) -> tuple[List[int], List[int]]:
    """
    Сортирует два массива по заданным условиям.

    Первый массив сортируется по убыванию,
    второй массив — по возрастанию.

    Parameters:
        :param arr1: первый массив чисел
        :param arr2: второй массив чисел

    Returns:
        :return: кортеж из отсортированных массивов (arr1_sorted, arr2_sorted)

    Examples:
    >> sort_arrays([3, 1, 2], [5, 4, 6])
    ([3, 2, 1], [4, 5, 6]
    """

    logger.info("Сортировка массивов")
    return sorted(arr1, reverse=True), sorted(arr2)


# правило сложения массивов
def sum_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    Выполняет поэлементное сложение двух массивов.

    Если элементы с одинаковыми индексами равны,
    в результирующий массив добавляется 0.
    В противном случае добавляется сумма элементов.

    Parameters:
        :param arr1: первый массив чисел
        :param arr2: второй массив чисел

    Returns:
        :return: массив результатов сложения

    Raises:
        :raises ValueError: если размеры массивов различаются

    Examples:
    >> sum_arrays([1, 2, 3], [3, 2, 1])
    [4, 0, 4]
    """

    logger.info("Сложение массивов")

    if len(arr1) != len(arr2):
        raise ValueError("Массивы должны быть одинаковой длины")   # логическая проверка

    return [0 if a == b else a + b for a, b in zip(arr1, arr2)]


def process_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    Обрабатывает два массива следующим образом:
        1. Сортирует arr1 по убыванию, arr2 по возрастанию.
        2. Выполняет поэлементное сложение с правилом:
           если элементы равны, результат = 0, иначе — их сумма.
        3. Возвращает итоговый массив, отсортированный по возрастанию.

    Parameters:
        :param arr1: первый массив чисел
        :param arr2: второй массив чисел

    Returns:
        :return: итоговый отсортированный массив после сложения

    Raises:
        :raises ValueError: если массивы имеют разную длину
    """

    logger.info("Вызов process_arrays()")

    # сортировка массивов
    arr1_sorted, arr2_sorted = sort_arrays(arr1, arr2)
    logger.debug(f"Отсортированные массивы: {arr1_sorted}, {arr2_sorted}")

    # поэлементное сложение с правилом "0 при равенстве"
    summed_array = sum_arrays(arr1_sorted, arr2_sorted)
    logger.debug(f"Массив после сложения: {summed_array}")

    # сортировка итогового массива по возрастанию
    result = sorted(summed_array)
    logger.info(f"Итоговый массив после сортировки: {result}")

    return result