"""
Task 2 — работа с тремя массивами (FSM-меню)

Модуль реализует конечный автомат с тремя состояниями:
    'NO_DATA'    — данные ещё не введены;
    'HAS_DATA'   — массивы заданы, но вычисление не выполнено;
    'HAS_RESULT' — выполнено вычисление и сохранён результат.

Меню позволяет:
    - вводить три массива вручную;
    - генерировать три массива случайных чисел;
    - выполнять вычисления (индексы, где arr1+arr2=arr3 и возведение суммы в степень минимального элемента);
    - показывать результат;
    - возвращаться в главное меню;
    - отключать логирование.

Публичный API:
    task_2_menu(): Запускает локальный FSM-цикл задачи 2.

Вспомогательные функции:
    generate_array(size, min_val, max_val)
    input_array_manual(size)
    check_sum(arr1, arr2, arr3)
    power_of_sum(arr1, arr2, arr3, indexes)
"""

import random
from logger import logger
from messages import MESSAGES
from exceptions import AppError, InputError, InvalidValueError, DataNotSetError, OperationError

msgs = MESSAGES["task2"]

# вспомогательные функции

def generate_array(size: int, min_val: int = 0, max_val: int = 50) -> list[int]:
    """
    Генерирует массив случайных целых чисел.

    Параметры:
        size (int):
            Количество элементов массива.
        min_val (int):
            Минимально возможное значение элемента (включительно).
        max_val (int):
            Максимально возможное значение элемента (включительно).

    Возвращает:
        list:
            Новый список длины size, заполненный случайными числами
            от min_val до max_val.

    Использование:
        Применяется в пункте меню "генерация данных" для создания
        трёх массивов одинаковой длины.
    """

    logger.info("task2: генерация случайного массива")
    if size <= 0:
        raise InvalidValueError("Размер массива должен быть положительным")
    return [random.randint(min_val, max_val) for _ in range(size)]


def input_array_manual(size: int) -> list[int]:
    """
    Выполняет ручной ввод массива фиксированной длины.

    Параметры:
        size (int):
            Требуемое количество элементов массива.

    Возвращает:
        list:
            Список из size целых чисел, введённых пользователем.

    Исключения:
        ValueError:
            Если пользователь вводит некорректное значение.

    Использование:
        Применяется при выборе ручного ввода данных в меню задачи 2.
    """

    logger.info("task2: ввод массива вручную")
    raw = input(f"Введите {size} чисел через пробел: ").strip()
    if not raw:
        raise InputError("Пустой ввод")
    try:
        arr = [int(x) for x in raw.split()]
        if len(arr) != size:
            raise InputError(f"Количество введённых чисел ({len(arr)}) не совпадает с заданным ({size})")
        return arr
    except ValueError:
        raise InputError("Введены нецелые числа")


def check_sum(arr1: list[int], arr2: list[int], arr3: list[int]) -> list[int]:
    """
    Находит индексы, где выполняется равенство:
        arr1[i] + arr2[i] == arr3[i].

    Параметры:
        arr1 (list): Первый массив одинаковой длины.
        arr2 (list): Второй массив.
        arr3 (list): Третий массив.

    Возвращает:
        list:
            Список индексов i, удовлетворяющих условию.
            Может быть пустым, если совпадений нет.

    Использование:
        Применяется на шаге вычислений перед функцией power_of_sum().
    """

    logger.info("task2: check_sum()")
    if len(arr1) != len(arr2) or len(arr2) != len(arr3):
        raise DataNotSetError("Все массивы должны быть одинаковой длины")
    return [i for i in range(len(arr1)) if arr1[i] + arr2[i] == arr3[i]]


def power_of_sum(arr1: list[int], arr2: list[int], arr3: list[int], indexes: list[int]) -> list[int]:
    """Вычисляет выражение:
        (arr1[i] + arr2[i] + arr3[i]) ** min(arr1[i], arr2[i], arr3[i])
    только для тех индексов, которые переданы в indexes.

    Параметры:
        arr1 (list): Первый массив.
        arr2 (list): Второй массив.
        arr3 (list): Третий массив.
        indexes (list):

    Возвращает:
        list of dict:
            Каждый элемент — словарь вида:
                {
                    "index": i,
                    "sum": arr1[i] + arr2[i] + arr3[i],
                    "power": (sum) ** min(arr1[i], arr2[i], arr3[i])
                }

    Использование:
        Эта функция завершающий этап вычислений — она формирует
        итоговый "результат" FSM-состояния HAS_RESULT.
    """

    logger.info("task2: power_of_sum()")
    results = []
    try:
        for i in indexes:
            a, b, c = arr1[i], arr2[i], arr3[i]
            results.append((a + b + c) ** min(a, b, c))
        return results
    except Exception as e:
        raise OperationError(f"Ошибка вычисления степени: {e}") from e


# -------------------------------------------------------
# ОБРАБОТЧИКИ ДЕЙСТВИЙ FSM - Finite State Machine (конечный автомат меню)
# -------------------------------------------------------

def _input_arrays(state: dict):
    """Ввод трёх массивов вручную и сохранение в состоянии FSM."""
    try:
        size = int(input("Введите размер массивов: "))
        arr1 = input_array_manual(size)
        arr2 = input_array_manual(size)
        arr3 = input_array_manual(size)
        state.update({"arr1": arr1, "arr2": arr2, "arr3": arr3, "results": None})
        logger.info("task2: массивы введены вручную")
    except AppError as e:
        logger.error(f"task2 input error: {e}")
        print(msgs["input_error"])


def _generate_arrays(state: dict):
    """Генерация трёх массивов случайных чисел и сохранение в состоянии FSM."""
    try:
        size = int(input("Введите размер массивов: "))
        arr1 = generate_array(size)
        arr2 = generate_array(size)
        arr3 = generate_array(size)
        state.update({"arr1": arr1, "arr2": arr2, "arr3": arr3, "results": None})
        print("Первый массив:", arr1)
        print("Второй массив:", arr2)
        print("Третий массив:", arr3)
        logger.info("task2: массивы сгенерированы")
    except AppError as e:
        logger.error(f"task2 generate error: {e}")
        print(msgs["input_error"])


def _perform_calculation(state: dict):
    """Выполняет основное вычисление и сохраняет результаты в состояние FSM."""
    arr1, arr2, arr3 = state.get("arr1"), state.get("arr2"), state.get("arr3")
    if not arr1 or not arr2 or not arr3:
        print(msgs["no_data"])
        logger.warning("task2: попытка вычисления без данных")
        return
    try:
        indexes = check_sum(arr1, arr2, arr3)
        if not indexes:
            print("Нет индексов, где сумма первых двух чисел равна третьему.")
            state["results"] = []
        else:
            state["results"] = power_of_sum(arr1, arr2, arr3, indexes)
            print("Вычисление выполнено.")
            logger.info("task2: вычисление завершено")
    except AppError as e:
        logger.error(str(e))
        print(msgs["no_data"])


def _show_results(state: dict):
    """Вывод исходных массивов, индексов и результатов вычислений."""
    arr1, arr2, arr3, results = state.get("arr1"), state.get("arr2"), state.get("arr3"), state.get("results")
    if not arr1 or not arr2 or not arr3:
        print(msgs["no_data"])
        return
    print("Первый массив:", arr1)
    print("Второй массив:", arr2)
    print("Третий массив:", arr3)
    if results is not None:
        print("Индексы:", check_sum(arr1, arr2, arr3))
        print("Результаты:", results)
        logger.info("task2: результаты показаны")


def _disable_logging(state: dict):
    """Отключение логирования."""
    logger.setLevel("CRITICAL")
    print("Логирование отключено")
    logger.critical("task2: logging disabled")


def _back(state: dict):
    """Возврат в главное меню."""
    logger.info("task2: выход в главное меню")

# -------------------------------------------------------
# ACTION MAP - словарь, который связывает выбор пользователя с конкретной функцией
# -------------------------------------------------------

ACTION_MAP = {
    "input_arrays": _input_arrays,
    "generate_arrays": _generate_arrays,
    "perform_calculation": _perform_calculation,
    "show_results": _show_results,
    "disable_logging": _disable_logging,
    "back": _back
}

# -------------------------------------------------------
# FSM TRANSITIONS - переходы конечного автомата
# -------------------------------------------------------

TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"error": "no_data"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "NO_DATA"}
    },
    "HAS_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_calculation", "next": "HAS_RESULT"},
        "4": {"error": "algorithm_not_executed"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_DATA"}
    },
    "HAS_RESULT": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_calculation", "next": "HAS_RESULT"},
        "4": {"action": "show_results", "next": "HAS_RESULT"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_RESULT"}
    }
}


# --- MAIN FSM MENU ---

def task2_menu():
    """
    Запускает FSM-меню задачи 2.

    Состояние FSM хранит словарь с ключами:
    'arr1', 'arr2', 'arr3', 'results'.

    Возвращает:
        None — выход в главное меню.
    """
    state = {"arr1": None, "arr2": None, "arr3": None, "results": None}
    fsm_state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task2 choice: {choice} state={fsm_state}")

        entry = TRANSITIONS[fsm_state].get(choice)

        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task2: неверный выбор")
            continue

        if "error" in entry:
            if entry["error"] == "no_data":
                print(msgs["no_data"])
                logger.warning("task2: попытка действия без данных")
            elif entry["error"] == "algorithm_not_executed":
                print(msgs["no_data"])
                logger.warning("task2: попытка показать результат до вычисления")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", fsm_state)
        if action_name:
            ACTION_MAP[action_name](state)

        if next_state == "BACK":
            logger.info("task2: возврат в главное меню")
            return

        fsm_state = next_state
