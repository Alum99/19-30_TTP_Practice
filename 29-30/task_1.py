import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError, OperationError

msgs = MESSAGES["task1"]  # подсловарь для задачи 1


# генерация массивов случайных чисел
generate_array = lambda size, a=0, b=50: (
    # Если size <= 0, то через генератор-throw выбрасывается InvalidValueError
    size <= 0 and (_ for _ in ()).throw(InvalidValueError("Размер массива должен быть положительным"))
    or [random.randint(a, b) for _ in range(size)]
) # list comprehension [random.randint(a, b) for _ in range(size)] быстрее; исключения — через генератор-throw
"""
Генерация массива случайных чисел

Параметры:
    size (int): длина массива (должна быть > 0)
    a (int): минимальное значение случайного числа (по умолчанию 0)
    b (int): максимальное значение случайного числа (по умолчанию 50)

Возвращает:
    list[int]: массив случайных чисел указанного размера

Исключения:
    InvalidValueError: если size <= 0

Особенности:
    - Используется list comprehension для быстрой генерации,
    - Исключение через генератор-throw вместо обычного raise.
"""


# переворот цифр в числе
reverse_int = lambda x: int(str(x)[::-1])
"""
Переворот числа

Параметры:
    x (int): исходное число

Возвращает:
    int: число, записанное в обратном порядке

Пример:
    reverse_int(123) -> 321
"""


# подсчет количества
count_common_with_reverses = lambda arr1, arr2: (
    (not arr1 or not arr2) and (_ for _ in ()).throw(DataNotSetError("Массивы пустые"))  # проверка, что массивы не пустые
    or (lambda:
        len({   # set comprehension, чтобы сохранить уникальные пары
            tuple(sorted((a, b)))  # выражение, которое добавляется в множество ((3,7) и (7,3) считаются одинаковой парой)
            for a in arr1          # циклы перебора массивов
            for b in arr2
            if a == b or reverse_int(a) == b or a == reverse_int(b)  # условие фильтрации
        })
    )()
)
# set comprehension вместо ручного массива used_pairs: быстрее, чище, без O(n^2) включений
# throw через генератор вместо множества if
"""
Подсчет уникальных общих чисел с учетом "перевёрнутых" чисел.

Параметры:
    arr1 (list[int]): первый массив чисел
    arr2 (list[int]): второй массив чисел

Возвращает:
    int: количество уникальных общих чисел

Исключения:
    DataNotSetError: если один или оба массива пустые

Особенности:
    - Используется set comprehension вместо ручного списка для ускорения.
    - Сравниваются прямые совпадения и перевёрнутые числа.
    - Используется throw через генератор вместо if/raise.
"""

# FSM

def task1_fsm():
    """
    Конечный автомат (FSM) для задачи 1.

    Реализует функциональность задачи:
        - ввод массивов вручную
        - генерация массивов случайно
        - подсчет общих чисел с учётом переворота
        - вывод результата
        - управление состояниями FSM
        - отключение логирования

    Состояния FSM:
        NO_DATA    — массивы ещё не заданы
        HAS_DATA   — массивы загружены
        HAS_RESULT — выполнен подсчет и сохранён результат

    Yields:
        None: ожидает пользовательский выбор меню

    Возврат:
        None: при выборе выхода (пункт 5)

    Исключения:
        DataNotSetError, InvalidValueError, OperationError — обрабатываются локально
    """

    arr1 = arr2 = result = None    # переменные для хранения массивов и результата
    state = "NO_DATA"              # начальное состояние автомата

    while True:  # Выводим заголовок и меню задачи
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))  # печатаем каждый пункт меню

        choice = yield  # приостанавливается на yield, ожидая ввод пользователя через send()
        logger.info(f"task1 choice={choice}, state={state}")

        if choice == "5":  # назад в главное меню
            return

        # Состояние "NO_DATA" - массивов нет

        if state == "NO_DATA":
            actions = {  # словарь действий по пунктам меню
                "1": lambda: (  # ввод массивов вручную через
                    list(map(int, input("Первый массив: ").split())),
                    list(map(int, input("Второй массив: ").split()))
                ),
                "2": lambda: (  # генерация случайных массивов
                    generate_array(int(input("Размер первого массива: "))),
                    generate_array(int(input("Размер второго массива: ")))
                ),
            }

            try:
                arr1, arr2 = actions.get(choice, lambda: (_ for _ in ()).throw(ValueError()))()
                print("Первый массив:", arr1)
                print("Второй массив:", arr2)
                state = "HAS_DATA"  # если все успещно - меняем состояние
                logger.info("Arrays loaded")
            except:
                print(msgs["input_error"])

        # Состояние "HAS_DATA" и "HAS_RESULT"

        else:
            actions = {
                "3": lambda: ( # подсчёт общих и перевёрнутых чисел
                    print(msgs["calculation_done"]),
                    count_common_with_reverses(arr1, arr2)
                )[1],

                "4": lambda: ( # вывод результата, если он есть
                    print(f"Результат: {result}") if result else print(msgs["no_data"])
                ),

                "6": lambda: ( # отключение логирования
                    logger.setLevel("CRITICAL"),
                    print("Логирование отключено")
                ),
            }

            try:
                # Выполняем действие из словаря actions
                out = actions.get(choice, lambda: print(msgs["invalid_choice"]))()

                # если это пункт 3
                if choice == "3":
                    result = out
                    state = "HAS_RESULT"

            # любые ошибки обрабатываются: выводим сообщение и логируем
            except Exception as e:
                print(msgs["input_error"])
                logger.error(f"Task1 error: {e}")
