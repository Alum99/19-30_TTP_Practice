from logger import logger
from task_1 import task_1_menu_fp
from task_2 import task_2_menu_fp
from task_3 import task_3_menu_fp
from messages import Messages
from functools import reduce

# Главное меню в стиле FP для словарного Messages
def main_fp():
    main_actions = {
        "1": task_1_menu_fp,
        "2": task_2_menu_fp,
        "3": task_3_menu_fp,
        "0": lambda: (_ for _ in ()).throw(SystemExit)
    }

    while True:
        main_msgs = Messages["MENU_MAIN"]
        print("\n" + main_msgs["title"])
        list(map(print, main_msgs["options"]))
        choice = input(main_msgs["prompt"])
        logger.info(f"Главное меню: выбран пункт {choice}")
        try:
            main_actions.get(choice, lambda: print(main_msgs["invalid_choice"]) or logger.info("Неверный выбор главного меню"))()
        except SystemExit:
            print(main_msgs["exit"])
            logger.info("Программа завершена пользователем")
            break


if __name__ == "__main__":
    main_fp()