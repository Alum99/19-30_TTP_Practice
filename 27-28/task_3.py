import random
from logger import logger
from messages import Messages
from exceptions import InvalidValueError, InputError, OperationError, AppError


# генерация случайного массива
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


# ручной ввод двух массивов
manual_input_fp = lambda: (
    (_ := int(input("Введите размер массивов: "))),
    (arr1 := input_array_manual_fp(_)),
    (arr2 := input_array_manual_fp(_)),
    (arr1, arr2)
)[-1]


# сортировка массивов
sort_arrays_fp = lambda arr1, arr2: (sorted(arr1, reverse=True), sorted(arr2))


# поэлементное сложение массивов
sum_arrays_fp = lambda arr1, arr2: (
    (_ for _ in ()).throw(OperationError("Массивы должны быть одинаковой длины")) if len(arr1) != len(arr2) else
    list(map(lambda x: 0 if x[0] == x[1] else x[0] + x[1], zip(arr1, arr2)))
)


def task_3_menu_fp():
    msgs = Messages["TASK3"]  # словарь
    state = {"arr1": None, "arr2": None, "arr1_sorted": None, "arr2_sorted": None, "result": None}

    actions = {
        "1": lambda: (
            (arr1_arr2 := manual_input_fp()),
            state.update({
                "arr1": arr1_arr2[0],
                "arr2": arr1_arr2[1],
                "arr1_sorted": sort_arrays_fp(arr1_arr2[0], arr1_arr2[1])[0],
                "arr2_sorted": sort_arrays_fp(arr1_arr2[0], arr1_arr2[1])[1],
            }),
            state.update({
                "result": sum_arrays_fp(state["arr1_sorted"], state["arr2_sorted"])
            }),
            logger.info("Массивы введены вручную и обработаны")
        ),

        "2": lambda: (
            (size := int(input("Введите размер массивов: "))),
            # Генерация массивов
            (arr1 := generate_array_fp(size)),
            (arr2 := generate_array_fp(size)),
            # Сортировка массивов
            (sorted_pair := sort_arrays_fp(arr1, arr2)),
            (arr1_sorted := sorted_pair[0]),
            (arr2_sorted := sorted_pair[1]),
            # Вычисление результата
            (result := sum_arrays_fp(arr1_sorted, arr2_sorted)),
            # Сохранение в state
            state.update({
                "arr1": arr1,
                "arr2": arr2,
                "arr1_sorted": arr1_sorted,
                "arr2_sorted": arr2_sorted,
                "result": result
            }),
            logger.info("Массивы сгенерированы и обработаны")
        ),

        "3": lambda: (
            print(msgs["no_data"]) if state["arr1"] is None or state["result"] is None else (
                print("Первый массив:", state["arr1"]),
                print("Второй массив:", state["arr2"]),
                print("Первый (убывание):", state["arr1_sorted"]),
                print("Второй (возрастание):", state["arr2_sorted"]),
                print("Результат:", sorted(state["result"])),
                logger.info("Результаты выведены")
            )
        ),

        "4": lambda: (_ for _ in ()).throw(SystemExit),
        "5": lambda: (logger.setLevel("CRITICAL"), print("Логирование отключено"), logger.critical("Установлен уровень CRITICAL"))
    }


    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))
        choice = input(msgs["prompt"])
        logger.info(f"task3: выбран пункт {choice}")
        try:
            actions.get(choice, lambda: print(msgs["invalid_choice"]) or logger.info("Неверный пункт меню task3"))()
        except AppError as e:
            logger.error(str(e))
            print(msgs["input_error"])
        except ValueError as e:
            logger.error(str(e))
            print("Ошибка ввода числа:", e)
        except SystemExit:
            logger.info("Возврат в главное меню")
            return

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))
        choice = input(msgs["prompt"])
        logger.info(f"task3: выбран пункт {choice}")
        try:
            actions.get(choice, lambda: print(msgs["invalid_choice"]) or logger.info("Неверный пункт меню task3"))()
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
        "1": task_3_menu_fp,
        "0": lambda: (_ for _ in ()).throw(SystemExit)
    }

    while True:
        main_msgs = Messages["MENU_MAIN"]  # заменено на словарь
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
