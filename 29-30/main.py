from messages import MESSAGES
from logger import logger
from task_1 import task1_fsm
from task_2 import task2_fsm
from task_3 import task3_fsm
from exceptions import AppError, InputError

# FSM главного меню — функциональный стиль

def main_fsm():
    msgs = MESSAGES["main_menu"] # подсловарь для главного меню

    while True:
        print("\n" + msgs["title"])
        list(map(print, msgs["options"]))

        choice = yield
        logger.info(f"MAIN choice: {choice}")

        # словарь действий по пунктам меню
        actions = {
            "1": lambda: yield_from_safe(task1_fsm),
            "2": lambda: yield_from_safe(task2_fsm),
            "3": lambda: yield_from_safe(task3_fsm),
            "0": lambda: exit_app(msgs)
        }

        try:
            # выполнение выбранного действия или ошибка
            actions.get(choice, lambda: (_ for _ in ()).throw(InputError(f"Неверный пункт меню: {choice}")))()
        except AppError as e:
            print(f"Ошибка приложения: {e}")
            logger.error(f"AppError: {e}")
        except InputError as e:
            print(f"Некорректный ввод: {e}")
            logger.warning(f"InputError: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            logger.exception(f"Unhandled exception: {e}")


# вспомогательные функции
def yield_from_safe(fsm_func):
    """Безопасный вызов вложенной корутины через yield from"""
    try:
        yield from fsm_func()
    except AppError as e:
        print(f"Ошибка во вложенной FSM: {e}")
        logger.error(f"AppError in nested FSM: {e}")
    except Exception as e:
        print(f"Ошибка во вложенной FSM: {e}")
        logger.exception(f"Unhandled exception in nested FSM: {e}")


def exit_app(msgs):
    print(msgs["exit"])
    logger.info("Application exit")
    raise StopIteration


# Главная функция запуска

def main():
    fsm = main_fsm()
    next(fsm)  # инициализация корутины

    msgs = MESSAGES["main_menu"]
    while True:
        try:
            choice = input(msgs["prompt"]).strip()
            fsm.send(choice)
        except StopIteration:
            break
        except AppError as e:
            print(f"Ошибка приложения: {e}")
            logger.error(f"AppError in main loop: {e}")
        except ValueError:
            print("Некорректный ввод!")
            logger.warning("ValueError in main input")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            logger.exception(f"Unhandled exception in main loop: {e}")


if __name__ == "__main__":
    main()
