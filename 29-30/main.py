from messages import MESSAGES
from logger import logger
from task_1 import task1_fsm
from task_2 import task2_fsm
from task_3 import task3_fsm
from exceptions import AppError, InputError

def main_fsm():
    """
    Корутина главного меню (FSM верхнего уровня).

    Реализует логику главного меню приложения.
    Ожидает ввод пользователя через `send()` и
    выполняет переключение между вложенными автоматами.
    """
    
    msgs = MESSAGES["main_menu"] # словарь с текстами для главного меню

    while True:
        print("\n" + msgs["title"])
        for opt in msgs["options"]:
            print(opt)

        choice = yield # Ожидаем ввод пользователя через send() и сохраняем его в choice.
        logger.info(f"MAIN choice: {choice}")

        # вложенные автоматы — через yield from
        if choice == "1":
            yield from task1_fsm()
        elif choice == "2":
            yield from task2_fsm()
        elif choice == "3":
            yield from task3_fsm()
        elif choice == "0":
            print(msgs["exit"])
            return
        else:
            print(msgs["invalid"])


def main():
    """
    Точка входа приложения.

    Инициализирует главный конечный автомат и
    передаёт ему ввод пользователя.
    """
    fsm = main_fsm()
    next(fsm)  # запуск корутины

    msgs = MESSAGES["main_menu"]

    while True:
        try:
            choice = input(msgs["prompt"]).strip()
            fsm.send(choice)
        except StopIteration:
            break


if __name__ == "__main__":
    main()
