import random                   # для генерации случайных чисел
from functools import reduce    # функция для свёртки списка в одно значение
from logger import logger       # объект логирования, чтобы вести журнал действий
from messages import Messages   # класс с текстами сообщений и меню для задач
from exceptions import InputError, InvalidValueError, DataNotSetError, OperationError, AppError


# генерация массива случайных чисел
generate_array_fp = lambda size, min_v=0, max_v=50: (         # анонимная функцию, которая возвращает массив случайных чисел
    [random.randint(min_v, max_v) for _ in range(size)]       # генератор списка: длиной size, случайные числа между 0 и 50
    if size > 0 else (_ for _ in ()).throw(InvalidValueError("Размер массива должен быть положительным"))
)   # если размер <= 0, выбрасываем исключение InvalidValueError.
# #list comprehension быстрее, чем ручной for + append

# ввод массива вручную через пробел
input_array_manual_fp = lambda size: (
    lambda raw: (
        list(map(int, raw.split()))
        if raw and all(x.lstrip("-").isdigit() for x in raw.split()) and len(raw.split()) == size
        else (_ for _ in ()).throw(InputError(f"Нужно ввести {size} чисел"))
    )
)(input(f"Введите {size} чисел через пробел: ").strip())

# переворот числа
reverse_number = lambda n: int(str(n)[::-1])


# подсчет общих чисел с функциональным подходом
def count_common_and_reversed_fp(arr1: list[int], arr2: list[int]) -> int:
    if not arr1 or not arr2:     # проверка, что массивы не пустые, иначе ошибка
        raise DataNotSetError("Массивы не заданы или пусты")

    try:
        # множество arr2_set, содержит: Все числа из arr2 и все перевернутые из arr2
        # map для функционального преобразования, и | объединяет множества
        arr2_set = set(arr2) | set(map(reverse_number, arr2))

        # фильтрация чисел первого массива, которые встречаются во втором (или их перевернутые)
        common_numbers = list(filter(lambda x: x in arr2_set or reverse_number(x) in arr2_set, arr1))
        # filter() — выбираем из arr1 те числа: либо есть числа в arr2_set, либо есть числа перевернутые в arr2_set
        # lambda x: — анонимная функция для условия фильтрации

        # удаление дубликатов через reduce
        unique_count = reduce(lambda acc, x: acc + [x] if x not in acc else acc, common_numbers, [])
        # reduce() — сворачиваем список common_numbers в список уникальных элементов

        return len(unique_count)  # количество уникальных общих чисел
    except Exception as e:
        raise OperationError(f"Ошибка выполнения подсчёта: {e}") from e


def task_1_menu_fp():
    msgs = Messages["TASK1"]  # теперь msgs — словарь
    state = {"arr1": None, "arr2": None, "result": None}

    actions = {
        "1": lambda: (
            state.update({"arr1": input_array_manual_fp(int(input("Введите размер первого массива: "))),
                          "arr2": input_array_manual_fp(int(input("Введите размер второго массива: "))) }),
            logger.info("Массивы введены вручную")
        ),
        "2": lambda: (
            (_size := int(input("Введите размер массивов: "))),
            state.update({"arr1": generate_array_fp(_size),
                          "arr2": generate_array_fp(_size)}),
            print("Первый массив:", state["arr1"]),
            print("Второй массив:", state["arr2"]),
            logger.info("Массивы сгенерированы случайно")
        ),
        "3": lambda: (
            (_ for _ in ()).throw(DataNotSetError("Массивы не заданы")) if None in (state["arr1"], state["arr2"]) else
            state.update({"result": count_common_and_reversed_fp(state["arr1"], state["arr2"])}),
            logger.info("Подсчёт выполнен")
        ),
        "4": lambda: (
            print(msgs["no_data"]) if state["result"] is None else print(f"Результат: {state['result']}"),
            logger.info("Результат показан")
        ),
        "5": lambda: (_ for _ in ()).throw(SystemExit),
        "6": lambda: (logger.setLevel("CRITICAL"), print("Логирование отключено"), logger.critical("Установлен уровень CRITICAL"))
    }

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["menu"]))
        choice = input(msgs["prompt"])
        logger.info(f"task1: выбран пункт {choice}")

        try:
            actions.get(choice, lambda: print(msgs["invalid_choice"]) or logger.info("Неверный пункт меню task1"))()
        except AppError as e:
            logger.error(str(e))
            print(msgs["input_error"])
        except ValueError as e:
            logger.error(str(e))
            print("Ошибка ввода числа:", e)
        except SystemExit:
            logger.info("Возврат в главное меню")
            return

def main():
    main_actions = {
        "1": task_1_menu,
        "0": lambda: (_ for _ in ()).throw(SystemExit)
    }

    while True:
        main_msgs = Messages["MENU_MAIN"]
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
    main()
