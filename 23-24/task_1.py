import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError, OperationError, InputError

msgs = MESSAGES["task1"]

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
    
    if not arr1 or not arr2:
        raise DataNotSetError("Массивы не заданы или пусты")

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
        raise OperationError(f"Ошибка выполнения подсчёта: {e}") from e

    return count


def task1_fsm():
    """
    Корутина конечного автомата задачи 1.

    Управляет вводом массивов, их генерацией,
    выполнением подсчёта общих чисел с переворотом,
    выводом результата и состояниями FSM.

    Состояния:
        NO_DATA   — массивы не заданы
        HAS_DATA  — массивы заданы
        HAS_RESULT — выполнен подсчёт

    Yields
        None: Ожидание пользовательского выбора пункта меню.

    Returns:
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

        # yield соответствует приёму входного символа автомата.
        # Корутины позволяют естественным образом описывать автоматы без внешних таблиц переходов.
        # Состояние хранится локально, переходы описываются явно
        choice = yield
        logger.info(f"task1 choice={choice}, state={state}")

        if choice == "5":
            return

        # Каждая корутина инкапсулирует своё состояние
        # и самостоятельно управляет переходами между состояниями.
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
                    size1 = int(input("Размер первого массива: "))
                    size2 = int(input("Размер второго массива: "))
                    arr1 = generate_array(size1)
                    arr2 = generate_array(size2)
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
                    result = count_common_with_reverses(arr1, arr2)
                    state = "HAS_RESULT"
                    print(msgs["calculation_done"])
                    logger.info(f"Common numbers calculated: {result}")
                except Exception as e:
                    print(msgs["no_data"])
                    logger.error(f"Calculation error: {e}")
            elif choice == "4":
                if result is None:
                    print(msgs["no_data"])
                else:
                    print(f"Результат: {result}")
                    logger.info("Result displayed")
            elif choice == "6":
                logger.setLevel("CRITICAL")
                print("Логирование отключено")
                logger.critical("Logging disabled")
            else:
                print(msgs["invalid_choice"])
                logger.info("Invalid menu choice")