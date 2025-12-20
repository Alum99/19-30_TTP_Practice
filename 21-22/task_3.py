"""
Task 3 — работа с двумя массивами и поэлементным сложением (FSM-меню)

Модуль реализует конечный автомат с двумя состояниями:
    'NO_DATA'    — данные ещё не введены;
    'HAS_DATA'   — массивы заданы, вычисление выполнено.

Меню позволяет:
    - вводить два массива вручную;
    - генерировать два массива случайных чисел;
    - сортировать массивы (первый по убыванию, второй по возрастанию);
    - выполнять поэлементное сложение с условием (0, если элементы равны, иначе сумма);
    - показывать результат;
    - возвращаться в главное меню;
    - отключать логирование.

Публичный API:
    task3_menu() - Запускает локальный FSM-цикл задачи 3.

Вспомогательные функции:
    random_array(size, min_val, max_val)
    manual_input()
    sort_arrays(arr1, arr2)
    sum_arrays(arr1, arr2)
"""

import random
from logger import logger
from messages import MESSAGES
from exceptions import InvalidValueError, OperationError, AppError

msgs = MESSAGES["task3"]

# вспомогательные функции

def random_array(size: int, min_val: int = 0, max_val: int = 50):
    """
        Генерация двух массивов случайных чисел одинаковой длины.

        Параметры:
            size (int): размер массивов
            min_val (int): минимальное значение элементов
            max_val (int): максимальное значение элементов

        Возвращает:
            tuple[list[int], list[int]]: два массива одинаковой длины

        Исключения:
            InvalidValueError: если size <= 0
        """

    if size <= 0:
        raise InvalidValueError("Размер массива должен быть положительным")
    arr1 = [random.randint(min_val, max_val) for _ in range(size)]
    arr2 = [random.randint(min_val, max_val) for _ in range(size)]
    return arr1, arr2

def manual_input():
    """
        Ручной ввод двух массивов одинаковой длины.

        Пользователь вводит размер массивов, затем элементы массивов через пробел.

        Возвращает:
            tuple[list[int], list[int]]: два введённых массива

        Исключения:
            InvalidValueError: если size <= 0
            OperationError: если длины массивов не совпадают с заданным размером
        """

    size = int(input("Введите размер массивов: "))
    if size <= 0:
        raise InvalidValueError("Размер массива должен быть положительным")
    arr1 = [int(x) for x in input("Введите первый массив: ").split()]
    arr2 = [int(x) for x in input("Введите второй массив: ").split()]
    if len(arr1) != size or len(arr2) != size:
        raise OperationError(f"Ожидалось {size} элементов, получено {len(arr1)} и {len(arr2)}")
    return arr1, arr2

def sort_arrays(arr1, arr2):
    """
        Сортировка двух массивов.

        Первый массив сортируется по убыванию,
        второй массив — по возрастанию.

        Возвращает:
            tuple[list[int], list[int]]: два отсортированных массива
        """

    return sorted(arr1, reverse=True), sorted(arr2)

def sum_arrays(arr1, arr2):
    """
        Поэлементное сложение двух массивов с условием:
        если элементы равны, добавляется 0, иначе — их сумма.

        Возвращает:
            list[int]: результат поэлементного сложения

        Исключения:
            OperationError: если длины массивов не совпадают
        """

    if len(arr1) != len(arr2):
        raise OperationError("Массивы должны быть одинаковой длины")
    return [0 if a == b else a + b for a, b in zip(arr1, arr2)]


# -------------------------------------------------------
# ОБРАБОТЧИКИ ДЕЙСТВИЙ FSM - Finite State Machine (конечный автомат меню)
# -------------------------------------------------------

def _manual_input(state):
    """Ввод массивов вручную, сортировка и поэлементное сложение, сохранение в состоянии FSM."""
    try:
        arr1, arr2 = manual_input()
        arr1_sorted, arr2_sorted = sort_arrays(arr1, arr2)
        result = sum_arrays(arr1_sorted, arr2_sorted)
        state.update({"arr1": arr1, "arr2": arr2, "arr1_sorted": arr1_sorted,
                      "arr2_sorted": arr2_sorted, "result": result})
        logger.info("task3: arrays input and processed manually")
    except AppError as e:
        logger.error(str(e))
        print(msgs["input_error"])
    except ValueError as e:
        logger.error(str(e))
        print(msgs["input_error"])

def _generate_arrays(state):
    """Генерация массивов случайным образом, сортировка и поэлементное сложение, сохранение в состоянии FSM."""
    try:
        size = int(input("Введите размер массивов: "))
        arr1, arr2 = random_array(size)
        arr1_sorted, arr2_sorted = sort_arrays(arr1, arr2)
        result = sum_arrays(arr1_sorted, arr2_sorted)
        state.update({"arr1": arr1, "arr2": arr2, "arr1_sorted": arr1_sorted,
                      "arr2_sorted": arr2_sorted, "result": result})
        print("Первый массив:", arr1)
        print("Второй массив:", arr2)
        logger.info("task3: arrays generated and processed")
    except (ValueError, AppError) as e:
        logger.error(str(e))
        print(msgs["input_error"])

def _show_result(state):
    """Вывод исходных массивов, отсортированных массивов и результата поэлементного сложения."""
    if state.get("arr1") is None or state.get("result") is None:
        print(msgs["no_data"])
        return
    print("Первый массив:", state["arr1"])
    print("Второй массив:", state["arr2"])
    print("Первый (убывание):", state["arr1_sorted"])
    print("Второй (возрастание):", state["arr2_sorted"])
    print("Результат:", sorted(state["result"]))
    logger.info("task3: result shown")

def _disable_logging(state):
    """Отключение логирования."""
    logger.setLevel("CRITICAL")
    print("Логирование отключено")
    logger.critical("task3 logging disabled")

def _back(state):
    """Возврат в главное меню."""
    logger.info("task3: back requested")

# -------------------------------------------------------
# ACTION MAP - словарь, который связывает выбор пользователя с конкретной функцией
# -------------------------------------------------------

ACTION_MAP = {
    "manual_input": _manual_input,
    "generate_arrays": _generate_arrays,
    "show_result": _show_result,
    "disable_logging": _disable_logging,
    "back": _back
}

# -------------------------------------------------------
# FSM TRANSITIONS - переходы конечного автомата
# -------------------------------------------------------

TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "manual_input", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"error": "no_data"},
        "4": {"action": "back", "next": "BACK"},
        "5": {"action": "disable_logging", "next": "NO_DATA"}
    },
    "HAS_DATA": {
        "1": {"action": "manual_input", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "show_result", "next": "HAS_DATA"},
        "4": {"action": "back", "next": "BACK"},
        "5": {"action": "disable_logging", "next": "HAS_DATA"}
    }
}

# --- MAIN FSM MENU ---

def task3_menu():
    """
    Запуск FSM-меню задачи 3 (локальный FSM).

    Контейнер состояния:
        arr1, arr2 — исходные массивы
        arr1_sorted, arr2_sorted — отсортированные массивы
        result — результат поэлементного сложения

    Возвращает:
        None — при выходе в главное меню
    """
    
    state = {"arr1": None, "arr2": None, "arr1_sorted": None, "arr2_sorted": None, "result": None}
    fsm_state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["menu"]:
            print(opt)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task3 choice: {choice} (state={fsm_state})")

        entry = TRANSITIONS[fsm_state].get(choice)
        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task3 invalid choice")
            continue

        if "error" in entry:
            if entry["error"] == "no_data":
                print(msgs["no_data"])
                logger.warning("task3: no data")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", fsm_state)
        action = ACTION_MAP.get(action_name)
        if action:
            action(state)

        if next_state == "BACK":
            logger.info("task3: returning to main")
            return
        fsm_state = next_state
