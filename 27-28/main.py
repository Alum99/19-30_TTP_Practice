from logger import logger
from task_1 import task_1_menu_fp
from task_2 import task_2_menu_fp
from task_3 import task_3_menu_fp
from messages import Messages
from functools import reduce

# Главное меню в стиле FP для словарного Messages
def main_fp(): 
    main_actions = { # словарь действий для главного меню
        "1": task_1_menu_fp,
        "2": task_2_menu_fp,
        "3": task_3_menu_fp, 
        "0": lambda: (_ for _ in ()).throw(SystemExit) # лямбда-выражение выбрасывает SystemExit
    }

    while True:
        main_msgs = Messages["MENU_MAIN"]  # словарь сообщений и пунктов главного меню из Messages
        print("\n" + main_msgs["title"])   # Печатаем заголовок главного меню
        list(map(print, main_msgs["options"]))  # Выводим все пункты меню
        choice = input(main_msgs["prompt"]) # Получаем ввод пользователя через input()
        logger.info(f"Главное меню: выбран пункт {choice}")
        try: # Через get() пытаемся найти действие для выбранного пункта меню.
            main_actions.get(choice, lambda: print(main_msgs["invalid_choice"]) or logger.info("Неверный выбор главного меню"))()
        except SystemExit: # Ловим исключение SystemExit
            print(main_msgs["exit"])
            logger.info("Программа завершена пользователем")
            break


if __name__ == "__main__":
    main_fp()
