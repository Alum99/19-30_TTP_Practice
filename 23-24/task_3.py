"""
Task 3 — работа с двумя массивами, их сортировкой, поэлементным сложением и FSM-управлением

Модуль реализует полноценный конечный автомат (FSM) для задачи №3,
в которой пользователь может вводить или генерировать два массива,
выполнять их обработку и видеть результат.

FSM включает следующие состояния:
    NO_DATA     — массивы ещё не заданы;
    HAS_DATA    — массивы получены (введены вручную или сгенерированы);
    HAS_RESULT  — вычисления выполнены, доступен вывод результата.

Функциональные возможности меню:
    1. Ввод двух массивов вручную (переход в HAS_DATA).
    2. Генерация двух случайных массивов одинаковой длины.
    3. Выполнение основной операции:
    4. Вывод результата (если вычисления выполнены).
    5. Выход в главное меню.
    6. Отключение логирования.

Публичный API:
    task3_fsm()  
        Запускает локальную FSM-корутину для задачи 3.
        Управляет состояниями, вводом массивов и выполнением операций.

Вспомогательные функции:
    generate_array(size, min_v, max_v)
        Генерирует массив случайных чисел указанного размера.

    sort_and_sum_arrays(arr1, arr2)
        Сортирует два массива (один по убыванию, второй по возрастанию),
        затем выполняет поэлементное условное сложение и сортирует результат.

Исключения:
    InvalidValueError — передан некорректный размер массива
    OperationError    — попытка сложить массивы разной длины
    InputError        — некорректный ввод данных пользователем
    DataNotSetError   — попытка выполнить операцию без введённых массивов

Логирование:
    Модуль активно использует логгер:
        - logger.info  — основные операции
        - logger.debug — промежуточные вычисления
        - logger.error — ошибки
        - logger.warning — предупреждения
        - logger.critical — отключение логирования

Общая структура:
    - получение массивов (ручной ввод / генерация)
    - проверка корректности
    - обработка массивов (сортировка + поэлементное сложение)
    - возможный вывод результата
    - управление через FSM-меню (корутина yield)
"""


import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError, OperationError, InputError

msgs = MESSAGES["task3"]

def generate_array(size: int, min_v: int = 0, max_v: int = 50) -> list[int]:
    """Генерирует массив случайных чисел указанного размера.

    Параметры:
        size (int): длина массива (должна быть > 0)
        min_v (int): минимальное значение
        max_v (int): максимальное значение

    Исключения:
        InvalidValueError: если size <= 0
    """

    if size <= 0:
        raise InvalidValueError("Размер массива должен быть положительным")
    logger.info("generating a random array")
    return [random.randint(min_v, max_v) for _ in range(size)]


def sort_and_sum_arrays(arr1: list[int], arr2: list[int]) -> list[int]:
    """
    Объединённая функция для двух массивов одинаковой длины:
        1. Сортирует первый массив по убыванию.
        2. Сортирует второй массив по возрастанию.
        3. Поэлементно складывает массивы:
            - если элементы равны, результат 0
            - иначе — их сумма
        4. Финальный массив сортируется по возрастанию.

    Параметры:
        arr1 (list[int]): первый массив
        arr2 (list[int]): второй массив

    Возвращает:
        list[int]: итоговый массив после сложения и сортировки

    Исключения:
        OperationError: если массивы разной длины
    """
    
    logger.info("task_3: sort_and_sum_arrays()")

    if len(arr1) != len(arr2):
        raise OperationError("Массивы должны быть одинаковой длины")

    # Сортировка массивов
    arr1_sorted = sorted(arr1, reverse=True)
    arr2_sorted = sorted(arr2)
    logger.debug(f"arr1_sorted: {arr1_sorted}")
    logger.debug(f"arr2_sorted: {arr2_sorted}")

    # Поэлементное сложение с условием
    summed = [0 if a == b else a + b for a, b in zip(arr1_sorted, arr2_sorted)]
    logger.debug(f"summed array before final sort: {summed}")

    # Финальная сортировка по возрастанию
    final_result = sorted(summed)
    logger.debug(f"final_result: {final_result}")

    return final_result

def task3_fsm():
    """
    Корутина конечного автомата задачи 3.

    Управляет вводом двух массивов, их генерацией,
    выполнением сортировки и суммирования,
    выводом результата и состояниями FSM.

    Состояния:
        NO_DATA   — массивы не заданы
        HAS_DATA  — массивы заданы
        HAS_RESULT — выполнены вычисления

    Yields
        None: Ожидание пользовательского выбора пункта меню.

    Returns
        None: Возврат в главное меню.
    """
    
    arr1 = None
    arr2 = None
    result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = yield
        logger.info(f"task3 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            if choice == "1":
                try:
                    arr1 = list(map(int, input("Первый массив: ").split()))
                    arr2 = list(map(int, input("Второй массив: ").split()))
                    state = "HAS_DATA"
                    logger.info("Arrays input manually")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "2":
                try:
                    size = int(input("Размер массивов: "))
                    arr1 = generate_array(size)
                    arr2 = generate_array(size)
                    print("Первый массив:", arr1)
                    print("Второй массив:", arr2)
                    state = "HAS_DATA"
                    logger.info("Arrays generated randomly")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Generation error: {e}")
            else:
                print(msgs["no_data"])

        elif state in ("HAS_DATA", "HAS_RESULT"):
            if choice == "3":
                try:
                    result = sort_and_sum_arrays(arr1, arr2)
                    state = "HAS_RESULT"
                    print(msgs["calculation_done"])
                    logger.info(f"Computation done, result: {result}")
                except Exception as e:
                    print(msgs["no_data"])
                    logger.error(f"Computation error: {e}")
            elif choice == "4":
                if not result:
                    print(msgs["no_data"])
                else:
                    print("Результат:", result)
                    logger.info("Result displayed")
            elif choice == "6":
                logger.setLevel("CRITICAL")
                print("Логирование отключено")
                logger.critical("Logging disabled")
            else:
                print(msgs["invalid_choice"])
                logger.info("Invalid menu choice")
