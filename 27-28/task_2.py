import random
from functools import reduce
from logger import logger
from messages import Messages
from exceptions import InputError, InvalidValueError, DataNotSetError, OperationError, AppError


# генератор случайного массива (функционально)
generate_array_fp = lambda size, min_val=0, max_val=50: (
    [random.randint(min_val, max_val) for _ in range(size)]
    if size > 0 else (_ for _ in ()).throw(InvalidValueError("Размер массива должен быть положительным"))
)


# ввод массива вручную
input_array_manual_fp = lambda size: (
    lambda raw: (
        list(map(int, raw.split()))
        if raw and all(x.lstrip("-").isdigit() for x in raw.split()) and len(raw.split()) == size
        else (_ for _ in ()).throw(InputError("Некорректный ввод"))
    )
)(input(f"Введите {size} чисел через пробел: ").strip())


# проверка суммы
check_sum_fp = lambda arr1, arr2, arr3: (
    (_ for _ in ()).throw(DataNotSetError("Массивы должны быть одинаковой длины"))
    if len(arr1) != len(arr2) or len(arr2) != len(arr3)
    else list(filter(lambda i: arr1[i] + arr2[i] == arr3[i], range(len(arr1))))
)


# вычисление (a + b + c) ** min(a, b, c)
power_of_sum_fp = lambda arr1, arr2, arr3, indexes: list(
    map(lambda i: (lambda a, b, c: (a + b + c) ** min(a, b, c))(arr1[i], arr2[i], arr3[i]), indexes)
)

def task_2_menu_fp():
    msgs = Messages["TASK2"]  # теперь словарь
    state = {"arr1": None, "arr2": None, "arr3": None, "results": None}

    actions = {
        "1": lambda: (
            (_size := int(input("Введите размер массивов: "))),
            state.update({
                "arr1": input_array_manual_fp(_size),
                "arr2": input_array_manual_fp(_size),
                "arr3": input_array_manual_fp(_size),
                "results": None
            }),
            logger.info("Массивы введены вручную")
        ),
        "2": lambda: (
            (_size := int(input("Введите размер массивов: "))),
            state.update({
                "arr1": generate_array_fp(_size),
                "arr2": generate_array_fp(_size),
                "arr3": generate_array_fp(_size),
                "results": None
            }),
            print("Первый массив:", state["arr1"]),
            print("Второй массив:", state["arr2"]),
            print("Третий массив:", state["arr3"]),
            logger.info("Массивы сгенерированы случайно")
        ),
        "3": lambda: (
            (_ for _ in ()).throw(DataNotSetError("Массивы не заданы")) if None in (state["arr1"], state["arr2"], state["arr3"]) else
            (indexes := check_sum_fp(state["arr1"], state["arr2"], state["arr3"])),
            state.update({"results": [] if not indexes else power_of_sum_fp(state["arr1"], state["arr2"], state["arr3"], indexes)}),
            print("Вычисление выполнено." if indexes else "Нет индексов, где сумма первых двух чисел равна третьему."),
            logger.info("Вычисление выполнено")
        ),
        "4": lambda: (
            print(msgs["no_data"]) if state["results"] is None else
            (
                print("Первый массив:", state["arr1"]),
                print("Второй массив:", state["arr2"]),
                print("Третий массив:", state["arr3"]),
                (indexes := check_sum_fp(state["arr1"], state["arr2"], state["arr3"])),
                print("Индексы:", indexes),
                print("Результаты:", state["results"]),
                logger.info("Результаты показаны")
            )
        ),
        "5": lambda: (_ for _ in ()).throw(SystemExit),
        "6": lambda: (logger.setLevel("CRITICAL"), print("Логирование отключено"), logger.critical("Установлен уровень CRITICAL"))
    }

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))
        choice = input(msgs["prompt"])
        logger.info(f"task2: выбран пункт {choice}")

        try:
            actions.get(choice, lambda: print(msgs["invalid_choice"]) or logger.info("Неверный пункт меню task2"))()
        except AppError as e:
            logger.error(str(e))
            print(msgs["input_error"])
        except ValueError as e:
            logger.error(str(e))
            print("Ошибка ввода числа:", e)
        except SystemExit:
            logger.info("Возврат в главное меню")
            return


def main_fp():
    main_actions = {
        "1": task_2_menu_fp,
        "0": lambda: (_ for _ in ()).throw(SystemExit)
    }

    while True:
        main_msgs = Messages["MENU_MAIN"]  # теперь словарь
        print("\n" + main_msgs["title"])
        list(map(print, main_msgs["options"]))
        choice = input(main_msgs["prompt"])
        try:
            main_actions.get(choice, lambda: print(main_msgs["invalid_choice"]))()
        except SystemExit:
            print(main_msgs["exit"])
            logger.info("Программа завершена пользователем")
            break


if __name__ == "__main__":
    main_fp()
