"""
Task 1 — подсчёт общих и «перевёрнутых» чисел (FSM-корутина)

Модуль реализует функционал задачи 1 в двух частях:
    1) Вспомогательные функции: генерация массивов и подсчёт общих чисел.
    2) Конечный автомат, реализованный как корутина (task1_fsm).

Функциональность включает:
    - ручной ввод двух массивов;
    - генерацию массивов случайных чисел;
    - вычисление количества уникальных общих чисел и чисел, являющихся «перевёрнутыми» (reverse);
    - вывод результата вычисления;
    - переходы между состояниями FSM;
    - отключение логирования.

Состояния FSM:
    NO_DATA    — массивы ещё не заданы;
    HAS_DATA   — массивы заданы (введены или сгенерированы);
    HAS_RESULT — выполнено вычисление, результат сохранён.

Публичный API:
    task1_fsm() — запускает локальный FSM, реализованный корутинным подходом.

Вспомогательные функции:
    - generate_array(size, min_v, max_v)
        Генерирует массив случайных чисел.
    - count_common_with_reverses(arr1, arr2)
        Подсчитывает количество общих и «перевёрнутых» чисел.
"""

import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError, OperationError, InputError

msgs = MESSAGES["task1"]   # берём подсловарь, относящийся к задаче 1

def generate_array(size: int, min_v: int = 0, max_v: int = 50) -> list[int]:
    """Генерирует массив случайных чисел указанного размера.

    Параметры:
        size (int): длина массива (должна быть > 0)
        min_v (int): минимальное значение
        max_v (int): максимальное значение

    Исключения:
        InvalidValueError: если size <= 0
    """

    if size <= 0: # если размер неправильный
        raise InvalidValueError("Размер массива должен быть положительным")
    logger.info("Generating a random array")
    return [random.randint(min_v, max_v) for _ in range(size)]


def count_common_with_reverses(arr1: list[int], arr2: list[int]) -> int:
    """
    Подсчитывает количество уникальных общих чисел между двумя массивами.
    Число считается общим, если оно:
        - встречается в обоих массивах напрямую, или
        - одно число является перевёрнутой версией другого.

    Параметры:
        arr1 (list[int]): первый массив чисел
        arr2 (list[int]): второй массив чисел

    Возвращает:
        int: количество уникальных общих чисел

    Исключения:
        DataNotSetError: если один или оба массива пустые
        OperationError: при возникновении ошибки в процессе подсчёта
    """
    
    if not arr1 or not arr2: # если хоть один массив пустой
        raise DataNotSetError("Массивы не заданы или пусты") # выбрасывается ошибка

    count = 0
    used_pairs = []

    try:
        for a in arr1:
            for b in arr2:
                # проверка прямого совпадения и перевёрнутых чисел
                if a == b or a == int(str(b)[::-1]) or int(str(a)[::-1]) == b:
                    pair = (min(a, b), max(a, b))
                    if pair not in used_pairs:
                        used_pairs.append(pair)
                        count += 1
                        logger.debug(f"Pair found: {pair}, quantity: {count}")
    except Exception as e:
        raise OperationError(f"Ошибка выполнения подсчёта: {e}") from     # e любые ошибки оборачиваются в OperationError

    return count


def task1_fsm(): # Конечный автомат
    """
    Корутина конечного автомата задачи 1.

    Управляет вводом массивов, их генерацией,
    выполнением подсчёта общих чисел с переворотом,
    выводом результата и состояниями FSM.

    Состояния:
        NO_DATA   — массивы не заданы
        HAS_DATA  — массивы заданы (введени или сгенерированы)
        HAS_RESULT — выполнен подсчёт

    Yields
        None: Ожидание пользовательского выбора пункта меню.

    Returns:
        None: Возврат в главное меню.
    """
    # корутинный подход - состояние живёт внутри функции

    arr1 = None
    arr2 = None
    result = None
    state = "NO_DATA"  # начальное состояние автомата: данных нет

    while True: # основной цикл
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        # yield соответствует приёму входного символа автомата.
        # Корутины позволяют естественным образом описывать автоматы без внешних таблиц переходов.
        # Состояние хранится локально, переходы описываются явно
        choice = yield 
        logger.info(f"task1 choice={choice}, state={state}")

        if choice == "5": # выход в главное меню, завершаает корутину
            return

        # Каждая корутина инкапсулирует своё состояние
        # и самостоятельно управляет переходами между состояниями.
        # обработка состояний конечного автомата
        if state == "NO_DATA":
            if choice == "1": # ввод масисвов вручную
                try:
                    arr1 = list(map(int, input("Первый массив: ").split()))
                    arr2 = list(map(int, input("Второй массив: ").split()))
                    state = "HAS_DATA"     # меняем состояние
                    logger.info("Arrays input manually")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
                    
            elif choice == "2":  # генерация массивов
                try:
                    size1 = int(input("Размер первого массива: "))
                    size2 = int(input("Размер второго массива: "))
                    arr1 = generate_array(size1)
                    arr2 = generate_array(size2)
                    print("Первый массив:", arr1)
                    print("Второй массив:", arr2)
                    state = "HAS_DATA"  # меняем состояние
                    logger.info("Arrays generated randomly")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Generation error: {e}")
            else:
                print(msgs["no_data"])  # неверный выбор

        elif state in ("HAS_DATA", "HAS_RESULT"): # Состояния HAS_DATA и HAS_RESULT
            if choice == "3": # выполнить расчет
                try:
                    result = count_common_with_reverses(arr1, arr2)
                    state = "HAS_RESULT"
                    print(msgs["calculation_done"])
                    logger.info(f"Common numbers calculated: {result}")
                except Exception as e:
                    print(msgs["no_data"])
                    logger.error(f"Calculation error: {e}")
                    
            elif choice == "4": # показать результат
                if result is None: # если результат еще не посчитан
                    print(msgs["no_data"])
                else:
                    print(f"Результат: {result}") # если результат есть
                    logger.info("Result displayed")
                    
            elif choice == "6": # отключение логирования
                logger.setLevel("CRITICAL")
                print("Логирование отключено")
                logger.critical("Logging disabled")
            else:
                print(msgs["invalid_choice"])
                logger.info("Invalid menu choice")
