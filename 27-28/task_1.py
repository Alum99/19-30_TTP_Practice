# Функциональное программирование
# это подход к написанию кода, где программа строится не как список команд («сначала сделай это, потом то»), а как набор математических функций.

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
input_array_manual_fp = lambda size: ( # лямбда-функцию, которая принимает один аргумент size
    lambda raw: ( # Внутри внешней лямбды создаётся вложенная лямбда
        list(map(int, raw.split()))
        if raw and all(x.lstrip("-").isdigit() for x in raw.split()) and len(raw.split()) == size
        else (_ for _ in ()).throw(InputError(f"Нужно ввести {size} чисел"))
    )
)(input(f"Введите {size} чисел через пробел: ").strip())
# Лямбда-функция — это небольшая анонимная функция, у которой нет имени
# map() - применить определенное действие (функцию) к каждому элементу в списке (или другой коллекции) без использования циклов

# переворот числа
reverse_number = lambda n: int(str(n)[::-1])


# подсчет общих чисел с функциональным подходом
count_common_and_reversed_fp = lambda arr1, arr2: ( # лямбда-функцию, которая принимает два массива: arr1 и arr2
    (_ for _ in ()).throw(DataNotSetError("Массивы не заданы или пусты"))
    if not arr1 or not arr2
    else (
        lambda arr2_set, common_numbers: len( # Если массивы не пустые, создаём вложенную лямбду
            reduce(lambda acc, x: acc + [x] if x not in acc else acc, common_numbers, [])
        )
    )(
        set(arr2).union(set(map(reverse_number, arr2))),  # объединяем arr2 и перевёрнутые числа через union()
        list(filter(
            lambda x: x in set(arr2).union(set(map(reverse_number, arr2))) 
                      or reverse_number(x) in set(arr2).union(set(map(reverse_number, arr2))),
            arr1
        ))
    )
)
# reduce() - сворачивает целую коллекцию в одно-единственное значение.
# filter() - для отбора элементов из коллекции на основе заданного условия



def task_1_menu_fp():
    msgs = Messages["TASK1"]  # словарь сообщений для задачи 1
    state = {"arr1": None, "arr2": None, "result": None}  # словарь, где хранится текущее состояние программы

    actions = { # словарь действий
        "1": lambda: (    # ввод массива вручную
            state.update({"arr1": input_array_manual_fp(int(input("Введите размер первого массива: "))),
                          "arr2": input_array_manual_fp(int(input("Введите размер второго массива: "))) }),
            logger.info("Массивы введены вручную")
        ),
        "2": lambda: ( # генерация массивов случайно
            (_size := int(input("Введите размер массивов: "))),
            state.update({"arr1": generate_array_fp(_size),
                          "arr2": generate_array_fp(_size)}),
            print("Первый массив:", state["arr1"]),
            print("Второй массив:", state["arr2"]),
            logger.info("Массивы сгенерированы случайно")
        ),
        "3": lambda: ( # подсчёт общих чисел с учётом реверса
            (_ for _ in ()).throw(DataNotSetError("Массивы не заданы")) if None in (state["arr1"], state["arr2"]) else
            state.update({"result": count_common_and_reversed_fp(state["arr1"], state["arr2"])}),
            logger.info("Подсчёт выполнен")
        ),
        "4": lambda: ( # вывод результата
            print(msgs["no_data"]) if state["result"] is None else print(f"Результат: {state['result']}"),
            logger.info("Результат показан")
        ),
        # выход в главное меню
        "5": lambda: (_ for _ in ()).throw(SystemExit),
        
        # отключение логирования
        "6": lambda: (logger.setLevel("CRITICAL"), print("Логирование отключено"), logger.critical("Установлен уровень CRITICAL"))
    }

    while True:
        print("\n" + msgs["title"]) # Печатаем заголовок меню задачи 1
        list(map(print, msgs["menu"])) # Выводим все пункты меню
        choice = input(msgs["prompt"]) # Получаем ввод пользователя
        logger.info(f"task1: выбран пункт {choice}")

        try: # Пытаемся выполнить действие из словаря actions по выбранному пункту choice
            actions.get(choice, lambda: print(msgs["invalid_choice"]) or logger.info("Неверный пункт меню task1"))()
            # если ключа нет, вызывается лямбда, которая выводит сообщение об ошибке
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
    main_actions = { # Словарь действий главного меню
        "1": task_1_menu,
        "0": lambda: (_ for _ in ()).throw(SystemExit)
    }

    while True:
        main_msgs = Messages["MENU_MAIN"]  # словарь сообщений для главного меню
        print("\n" + main_msgs["title"])   # заголовок меню и все пункты меню
        list(map(print, main_msgs["options"])) 
        choice = input(main_msgs["prompt"]) # ввод пользователя для выбора пункта меню
        
        try: # Пытаемся выполнить действие из словаря main_actions
            main_actions.get(choice, lambda: print(main_msgs["invalid_choice"]))()
        except SystemExit:
            print(main_msgs["exit"])
            logger.info("Программа завершена пользователем")
            break

if __name__ == "__main__":
    main()
