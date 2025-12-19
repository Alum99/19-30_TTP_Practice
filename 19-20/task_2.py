from typing import List

# Возвращает список индексов, где arr1[i] + arr2[i] == arr3[i]
def check_sum(arr1: List[int], arr2: List[int], arr3: List[int]) -> List[int]:
    """
    Находит индексы элементов массивов, для которых
    arr1[i] + arr2[i] == arr3[i]

    Все три массива должны быть одинаковой длины.

    Parameters:
        :param arr1: первый массив чисел
        :param arr2: второй массив чисел
        :param arr3: третий массив чисел

    Returns:
        :return: список индексов, удовлетворяющих условию

    Raises:
        :raises ValueError: если массивы имеют разную длину

     Examples
    --------
    >> check_sum([1, 2, 3], [4, 5, 6], [5, 7, 9])
    [0, 1, 2]

    >> check_sum([1, 2], [1, 2], [3, 3])
    []
    """

    logger.info("Вызов check_sum()")

    if len(arr1) != len(arr2) or len(arr2) != len(arr3):
        raise ValueError("Все массивы должны быть одинаковой длины")

    return [i for i in range(len(arr1)) if arr1[i] + arr2[i] == arr3[i]]


# Вычисление (a + b + c) ** min(a, b, c)
def power_of_sum(arr1: List[int], arr2: List[int], arr3: List[int], indexes: List[int]) -> List[int]:
    """
    Возводит сумму элементов по индексам в степень минимального из них.

    (Вычисляет значения (a + b + c) ** min(a, b, c)
    для элементов массивов по заданным индексам)

    Для каждого индекса i из списка indexes:
        - берутся элементы arr1[i], arr2[i], arr3[i];
        - находится их сумма;
        - сумма возводится в степень минимального из трёх чисел.

    Parameters:
        :param arr1: первый массив чисел
        :param arr2: второй массив чисел
        :param arr3: третий массив чисел
        :param indexes: список индексов, для которых выполняется вычисление

    Returns:
        :return: список результатов возведения суммы в степень

    Raises:
        :raises IndexError: если индекс выходит за границы массивов.
        :raises TypeError: если переданы некорректные типы данных.

    Examples
    --------
    >> power_of_sum([1, 2], [2, 3], [3, 4], [0, 1])
    [6, 81]
    """

    logger.info("Вызов power_of_sum()")

    results = []
    for i in indexes:                          # если i больше допустимого индекса, то IndexError
        a, b, c = arr1[i], arr2[i], arr3[i]    # если i — строка, не int, то TypeError
        results.append((a + b + c) ** min(a, b, c))

    return results


def compute_power_for_matching_sums(arr1: List[int], arr2: List[int], arr3: List[int]) -> List[int]:
    """
    Проверяет, для каких индексов arr1[i] + arr2[i] == arr3[i],
    и для этих индексов вычисляет (arr1[i] + arr2[i] + arr3[i]) ** min(arr1[i], arr2[i], arr3[i]).

    Parameters:
        :param arr1: первый массив чисел
        :param arr2: второй массив чисел
        :param arr3: третий массив чисел

    Returns:
        :return: список результатов возведения суммы в степень

    Raises:
        :raises ValueError: если массивы имеют разную длину или пустые
    """

    logger.info("Вызов compute_power_for_matching_sums()")

    if not arr1 or not arr2 or not arr3:
        logger.error("Массивы пустые или не заданы")
        raise ValueError("Массивы не могут быть пустыми")

    # Находим индексы, где сумма первых двух элементов равна третьему
    indexes = check_sum(arr1, arr2, arr3)

    if not indexes:
        logger.info("Нет индексов, где arr1[i] + arr2[i] == arr3[i]")
        return []

    # Вычисляем сумму и возводим в степень минимального числа
    results = power_of_sum(arr1, arr2, arr3, indexes)
    logger.info(f"Результаты вычислений: {results}")

    return results