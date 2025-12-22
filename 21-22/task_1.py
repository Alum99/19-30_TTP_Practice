"""
Task 1 — подсчёт общих и «перевёрнутых» чисел (FSM-меню)

Модуль реализует конечный автомат с тремя состояниями:
    'NO_DATA'    — данные ещё не введены;
    'HAS_DATA'   — массивы заданы, но вычисление не выполнено;
    'HAS_RESULT' — выполнено вычисление и сохранён результат.

Меню позволяет:
    - вводить два массива вручную;
    - генерировать два массива случайных чисел;
    - выполнять подсчёт общих чисел и чисел, являющихся «перевёрнутыми» (reverse);
    - выводить результат вычисления;
    - возвращаться в главное меню;
    - отключать логирование.

Публичный API:
    task1_menu() - Запускает локальный FSM-цикл задачи 1.

Вспомогательные функции:
    - generate_array(size, min_v, max_v): Генерирует массив случайных чисел.
    - input_array_manual(): Вводит массив вручную и проверяет корректность входных данных.
    - reverse_number(n): Возвращает число, записанное в обратном порядке цифр.
    - count_common_and_reversed(arr1, arr2): Выполняет подсчёт общих и перевёрнутых чисел.
"""

import random
from logger import logger
from messages import MESSAGES
from exceptions import AppError, InputError, DataNotSetError, InvalidValueError, OperationError

msgs = MESSAGES["task1"]

# вспомогательные функции

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
    logger.info("Генерация случайного массива")
    return [random.randint(min_v, max_v) for _ in range(size)]


def input_array_manual() -> list[int]:
    """Ввод массива чисел вручную.

    Возвращает:
        list[int]: список введённых целых чисел

    Исключения:
        InputError: пустая строка или неверный формат
    """
    raw = input("Введите числа через пробел: ")
    if not raw.strip():
        raise InputError("Пустой ввод")
    try:
        logger.info("Ввод массива вручную")
        return [int(x) for x in raw.split()]
    except ValueError:
        raise InputError("Введены нецелые числа")


def reverse_number(n: int) -> int:
    """Возвращает число с цифрами в обратном порядке.

    Пример:
        123 → 321
    """
    result = int(str(n)[::-1])
    logger.debug(f"reverse_number: {n} -> {result}")
    return result


def count_common_and_reversed(arr1: list[int], arr2: list[int]) -> int:
    """
    Считает количество уникальных пар чисел, которые либо:
        - совпадают напрямую (a == b),
        - либо одно является перевёрнутым вариантом другого.

    Параметры:
        arr1, arr2 (list[int]): входные массивы

    Исключения:
        DataNotSetError: если массивы пустые
        OperationError: любая внутренняя ошибка
    """
    if not arr1 or not arr2:
        raise DataNotSetError("Массивы не заданы или пусты")

    count = 0
    used_pairs = []

    try:
        for a in arr1:
            for b in arr2:
                if a == b or a == reverse_number(b) or reverse_number(a) == b:
                    pair = (min(a, b), max(a, b))
                    if pair not in used_pairs:
                        used_pairs.append(pair)
                        count += 1
    except Exception as e:
        raise OperationError(f"Ошибка выполнения подсчёта: {e}") from e

    return count


# -------------------------------------------------------
# ОБРАБОТЧИКИ ДЕЙСТВИЙ FSM - Finite State Machine (конечный автомат меню)
# -------------------------------------------------------
# Каждому пункту меню соответствует своя функция

def _input_arrays(state_container):
    """Ввод двух массивов вручную и сохранение их в состояние FSM."""
    try:
        print("Первый массив:")
        arr1 = input_array_manual()
        print("Второй массив:")
        arr2 = input_array_manual()
        state_container["arr1"], state_container["arr2"], state_container["result"] = arr1, arr2, None
        logger.info("task1: массивы введены вручную")
    except AppError as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _generate_arrays(state_container):
    """Генерация двух случайных массивов и сохранение их в состояние FSM."""
    try:
        size1 = int(input("Размер первого массива: "))
        size2 = int(input("Размер второго массива: "))
        arr1 = generate_array(size1)
        arr2 = generate_array(size2)
        state_container["arr1"], state_container["arr2"], state_container["result"] = arr1, arr2, None
        print("Первый массив:", arr1)
        print("Второй массив:", arr2)
        logger.info("task1: массивы сгенерированы")
    except AppError as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _perform_count(state_container):
    """Выполняет вычисление и сохраняет результат в состояние FSM."""
    arr1 = state_container.get("arr1")
    arr2 = state_container.get("arr2")

    if arr1 is None or arr2 is None:
        print(msgs["no_data"])
        logger.warning("task1: попытка подсчёта без данных")
        return

    try:
        result = count_common_and_reversed(arr1, arr2)
        state_container["result"] = result
        print(msgs["calculation_done"])
        logger.info("task1: подсчёт выполнен")
    except AppError as e:
        logger.error(str(e))
        print(msgs["no_data"])


def _show_result(state_container):
    """Показывает сохранённый результат, если он есть."""
    result = state_container.get("result")
    if result is None:
        print(msgs["no_data"])
        logger.warning("task1: попытка показать результат без вычислений")
    else:
        print(f"Результат: {result}")
        logger.info("task1: результат показан")


def _disable_logging(state_container):
    """Отключает логирование (переводит уровень в CRITICAL)."""
    logger.setLevel("CRITICAL")
    print("Логирование отключено")
    logger.critical("task1: логирование отключено")


def _back(state_container):
    """Возвращает выполнение в главное меню."""
    logger.info("task1: возврат в главное меню")

# -------------------------------------------------------
# ACTION MAP - словарь, который связывает выбор пользователя с конкретной функцией
# -------------------------------------------------------

# словарь, который связывает текстовое имя действия с функцией
ACTION_MAP = {
    "input_arrays": _input_arrays,
    "generate_arrays": _generate_arrays,
    "perform_count": _perform_count,
    "show_result": _show_result,
    "disable_logging": _disable_logging,
    "back": _back
}

# -------------------------------------------------------
# FSM TRANSITIONS - переходы конечного автомата
# -------------------------------------------------------
# TRANSITIONS — это словарь

TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"error": "no_data"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "NO_DATA"},
    },
    "HAS_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_count", "next": "HAS_RESULT"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_DATA"},
    },
    "HAS_RESULT": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_count", "next": "HAS_RESULT"},
        "4": {"action": "show_result", "next": "HAS_RESULT"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_RESULT"},
    }
}

# --- MAIN FSM MENU ---

def task1_menu():
    """Запускает FSM-меню задачи 1 (локальный FSM).

    Хранит состояние:
        arr1 — первый массив
        arr2 — второй массив
        result — результат вычисления

    Возвращает:
        None (возврат в главное меню)
    """
    # словарь, который хранит всё текущее состояние моей задачи (контейнер состояния)
    state_container = {"arr1": None, "arr2": None, "result": None}
    # функция работает с состоянием, но не зависит от глобальных переменных
    state = "NO_DATA" # стартовое состояние

    while True: # основной цикл меню
        print("\n" + msgs["title"]) # вывод меню
        for option in msgs["menu"]:
            print(option)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task1 choice: {choice} (state={state})") # фиксирует выбор и состояние FSM

        entry = TRANSITIONS[state].get(choice) # получение инструкции 
        if not entry: # если такого пункта нет, то сообщение, повторяем цикл
            print(msgs["invalid_choice"])
            logger.info("task1: неверный пункт меню")
            continue 

        if "error" in entry: # если действие нельзя выполнить в текущем состоянии
            # выводит сообщение и не выполняет действие
            key = entry["error"]
            if key == "no_data":
                print(msgs["no_data"])
                logger.warning("task1: попытка действия без данных")
            elif key == "algorithm_not_executed":
                print(msgs["no_data"])
                logger.warning("task1: попытка показать результат без вычислений")
            continue

        action_name = entry.get("action") # название действия (например input_arrays)
        next_state = entry.get("next", state)
        action = ACTION_MAP.get(action_name)
        if action:
            action(state_container) # функции получают state_container

        if next_state == "BACK": # если назад, то функция task1_menu завершается
            return

        state = next_state # иначе FSM переходит в следующее состояние
