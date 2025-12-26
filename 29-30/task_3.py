import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError, OperationError

msgs = MESSAGES["task3"]  # подсловарь для задачи 3

# АЛГОРИТМЫ

# генерация массива
generate_array = lambda n, mn=0, mx=50: (
    n > 0 and [random.randint(mn, mx) for _ in range(n)]
    or (_ for _ in ()).throw(InvalidValueError("Размер должен быть > 0"))
)

# сортировка + поэлементное сложение + финальная сортировка
sort_and_sum_arrays = lambda a1, a2: (
    len(a1) == len(a2)
    and sorted(
        0 if x == y else x + y
        for x, y in zip(
            sorted(a1, reverse=True),
            sorted(a2)
        )
    )
    or (_ for _ in ()).throw(OperationError("Массивы должны быть одинаковой длины"))
)

# чтение массива
read_arr = lambda name: list(map(int, input(f"{name}: ").split()))


# FSM

def task3_fsm():
    a1 = a2 = result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))

        choice = yield
        logger.info(f"task3 choice={choice}, state={state}")

        if choice == "5":
            return

        # ============ NO_DATA ============
        if state == "NO_DATA":
            actions = {
                "1": lambda: (
                    read_arr("Первый массив"),
                    read_arr("Второй массив")
                ),
                "2": lambda: (
                    lambda n: (
                        generate_array(n),
                        generate_array(n)
                    )
                )(int(input("Размер массивов: ")))
            }

            try:
                a1, a2 = actions.get(
                    choice,
                    lambda: (_ for _ in ()).throw(ValueError())
                )()
                state = "HAS_DATA"
            except:
                print(msgs["input_error"])

        # ============ HAS_DATA / HAS_RESULT ============
        else:
            actions = {
                "3": lambda: (
                    print(msgs["calculation_done"]),
                    sort_and_sum_arrays(a1, a2)
                )[1],
                "4": lambda: print(
                    "Результат:",
                    result if result is not None else msgs["no_result"]
                ),
                "6": lambda: (
                    logger.setLevel("CRITICAL"),
                    print("Логирование отключено")
                )
            }

            try:
                ret = actions.get(
                    choice,
                    lambda: print(msgs["invalid_choice"])
                )()

                # результаты только у команды 3
                if choice == "3":
                    result = ret
                    state = "HAS_RESULT"

            except:
                print(msgs["input_error"])
