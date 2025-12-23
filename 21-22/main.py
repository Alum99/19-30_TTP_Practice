"""
Главный модуль приложения (конечный автомат главного меню).

Модуль реализует верхний уровень взаимодействия с пользователем:
    - отображает главное меню,
    - принимает ввод,
    - вызывает подпроцессы task_1, task_2, task_3,
    - завершает работу приложения.

Архитектура:
MAIN_FSM : dict
    Словарь переходов главного конечного автомата.
    Ключ — состояние ("MAIN"),
    значение — словарь соответствий: "выбор пользователя" → "действие".

ACTION_MAP : dict
    Переотображение строковых имён действий в функции-обработчики.

Основные элементы
    main(): Главная функция — запускает диалог главного меню.

Обработчики:
    do_task_1()
    do_task_2()
    do_task_3()
    do_exit()

Примечания:
    - Тексты меню берутся из MESSAGES["main_menu"].
    - task_1_menu(), task_2_menu(), task_3_menu() находятся в соответствующих модулях
      task_1.py / task_2.py / task_3.py.
"""
# main.py — это контроллер
from logger import logger
from messages import MESSAGES
from task_1 import task1_menu
from task_2 import task2_menu
from task_3 import task3_menu

# FSM главного меню (логика переходов)

MAIN_FSM = {
    "MAIN": {
        "1": {"action": "task1"},
        "2": {"action": "task2"},
        "3": {"action": "task3"},
        "0": {"action": "exit"},
    }
}

# Обработчики действий

def do_task1():
    logger.info("→ Переход в task_1")
    task1_menu()     # запуск подменю 1


def do_task2():
    logger.info("→ Переход в task_2")
    task2_menu()     # запуск подменю 2


def do_task3():
    logger.info("→ Переход в task_3")
    task3_menu()     # запуск подменю 3


def do_exit():
    print(MESSAGES["main_menu"]["exit"])
    logger.info("Приложение завершено пользователем")
    return False      # сигнал для выхода из главного цикла


# Словарь обработчиков (action → function)
# ACTION_MAP превращает строковое имя действия из FSM в конкретную вызываемую функцию

ACTION_MAP = {
    "task1": do_task1,
    "task2": do_task2,
    "task3": do_task3,
    "exit": do_exit,
}

# Главный цикл программы

def main():
    """
    Основной цикл обработки меню через конечный автомат.

    Алгоритм:
        1. Вывод главного меню.
        2. Получение ввода от пользователя.
        3. Поиск соответствующего действия в MAIN_FSM.
        4. Вызов обработчика из ACTION_MAP.
        5. Если обработчик вернул False — завершение программы.

    Исключения:
    KeyError:
        Если в FSM отсутствует действие с указанным именем
        (что указывает на ошибку конфигурации).
    """
    state = "MAIN" # текущее состояние конечного автомата
    msgs = MESSAGES["main_menu"] # Из словаря MESSAGES извлекаются текстовые сообщения

    while True: # цикл программы
        print("\n" + msgs["title"]) # вывод заголовка меню
        for opt in msgs["options"]: # проход по списку вариантов (например "1 - Task 1", "2 - Task 2", …).
            print(opt)

        choice = input(msgs["prompt"]).strip()  # Ввод пользователя
        logger.info(f"Главное меню: ввод пользователя → {choice}") # логирование ввода

        entry = MAIN_FSM[state].get(choice) # Поиск перехода в FSM
        if not entry: # проверка на неверный ввода
            print(msgs["invalid"])
            logger.warning("Main: неверный пункт меню")
            continue

        action_name = entry["action"] # Получение имени действия
        handler = ACTION_MAP[action_name] # Получение обработчика по имени

        result = handler()   # вызов обработчика
        if result is False:  # если обработчик сигнализировал выход
            break


# ------------------------------------------------------------
# Точка входа
# ------------------------------------------------------------
if __name__ == "__main__":
    main()