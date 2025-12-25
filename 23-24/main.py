"""
Главный модуль приложения.

Реализует верхнеуровневый конечный автомат (FSM) для всех задач.
В зависимости от выбора пользователя передаёт управление
во вложенные автоматы task_1_fsm, task2_fsm, task3_fsm через `yield from`.

Notes:
    - Каждое меню реализовано как корутина.
    - Состояние автомата хранится внутри корутины.
    - Пользовательский ввод передаётся через метод send().
"""

from messages import MESSAGES
from logger import logger
from task_1 import task1_fsm
from task_2 import task2_fsm
from task_3 import task3_fsm
from exceptions import AppError, InputError, OperationError, DataNotSetError, InvalidValueError

def main_fsm():
    """
    Корутина главного меню верхнего уровня.

    Ожидает пользовательский ввод через `send()` и
    передаёт управление в автоматы задач.

    Yields
        None: Ожидание пользовательского ввода.

    Returns
        None: Завершение работы приложения при выборе "Выход".
    """
    
    msgs = MESSAGES["main_menu"] # получение строк меню (сообщение)

    while True: 
        print("\n" + msgs["title"])
        for option in msgs["options"]:
            print(option)

        choice = yield  # Корутина приостанавливается и ждёт, ожиадние выбора пользователя
        logger.info(f"MAIN choice: {choice}")

        try:
            if choice == "1":
                yield from task1_fsm()  # yield from передаёт выполнение другой корутине
            elif choice == "2":
                yield from task2_fsm()
            elif choice == "3":
                yield from task3_fsm()
            elif choice == "0": # выход из программы
                print(msgs["exit"])
                logger.info("Application exit")
                return
            else: # неверный ввод
                print(msgs["invalid"])
                raise InputError(f"Неверный пункт меню: {choice}")

        except AppError as e: # обработка ошибок
            print(f"Ошибка приложения: {e}")
            logger.error(f"AppError: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            logger.exception(f"Unhandled exception: {e}")


def main():
    fsm = main_fsm() # fsm — это генератор, main_fsm() — это корутина
    next(fsm)  # инициализация корутины, Запускает корутину до первого yield

    msgs = MESSAGES["main_menu"]
    while True:
        try:
            choice = input(msgs["prompt"]).strip()
            fsm.send(choice)
        except StopIteration:
            # Завершение работы корутины при выходе
            break
        except AppError as e:
            print(f"Ошибка приложения: {e}")
            logger.error(f"AppError in main loop: {e}")
        except ValueError:
            print("Некорректный ввод!")
            logger.error("ValueError in main input")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            logger.exception(f"Unhandled exception in main loop: {e}")


if __name__ == "__main__":
    main()
