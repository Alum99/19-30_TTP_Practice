import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError, OperationError

msgs = MESSAGES["task2"]  # подсловарь для задачи 2


generate_array = lambda size, a=0, b=50: (
    size <= 0 and (_ for _ in ()).throw(InvalidValueError("Размер должен быть > 0"))
    or [random.randint(a, b) for _ in range(size)]
)
# компактное условие + list comprehension


sum_and_power = lambda arr1, arr2, arr3: (
    (not arr1 or not arr2 or not arr3)
    and (_ for _ in ()).throw(DataNotSetError("Массивы пусты"))
    or len(arr1) != len(arr2) or len(arr2) != len(arr3)
    and (_ for _ in ()).throw(DataNotSetError("Длины массивов должны совпадать"))
    or [
        {
            "index": i,
            "sum": (s := a + b + c),
            "power": s ** min(a, b, c)
        }
        for i, (a, b, c) in enumerate(zip(arr1, arr2, arr3))
        if a + b == c
    ]
)

# единый comprehension вместо циклов
# оператор «морж» ускоряет вычисление суммы


# FSM

def task2_fsm():
    arr1 = arr2 = arr3 = result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))

        choice = yield
        logger.info(f"task2 choice={choice}, state={state}")

        if choice == "5":
            return

        # ========================
        # НЕТ ДАННЫХ
        # ========================
        if state == "NO_DATA":
            actions = {
                "1": lambda: (
                    list(map(int, input("Первый массив: ").split())),
                    list(map(int, input("Второй массив: ").split())),
                    list(map(int, input("Третий массив: ").split()))
                ),
                "2": lambda: (
                    lambda size:
                        (generate_array(size),
                         generate_array(size),
                         generate_array(size))
                )(int(input("Размер массивов: ")))
            }

            try:
                arr1, arr2, arr3 = actions.get(
                    choice, lambda: (_ for _ in ()).throw(ValueError())
                )()

                print("Первый:", arr1)
                print("Второй:", arr2)
                print("Третий:", arr3)

                state = "HAS_DATA"
                logger.info("Arrays set")
            except:
                print(msgs["input_error"])

        # ========================
        # ДАННЫЕ ЕСТЬ
        # ========================
        else:
            actions = {
                "3": lambda: (
                    print(msgs["calculation_done"]),
                    sum_and_power(arr1, arr2, arr3)
                )[1],

                "4": lambda: (
                    print(f"Результат: {result}") if state == "HAS_RESULT" else print(msgs["no_data"])
                ),

                "6": lambda: (
                    logger.setLevel("CRITICAL"),
                    print("Логирование отключено")
                ),
            }

            try:
                out = actions.get(choice, lambda: print(msgs["invalid_choice"]))()

                if choice == "3":
                    result = out
                    state = "HAS_RESULT"

            except Exception as e:
                print(msgs["input_error"])
                logger.error(f"task2 error: {e}")
