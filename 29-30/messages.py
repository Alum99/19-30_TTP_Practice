"""
Централизованный словарь сообщений для всего приложения.
Сообщения сгруппированы по задачам: main_menu, task1, task2, task3.
"""

class Messages:
    """
    Централизованное хранение всех сообщений для меню и FSM.

    Используется для:
        - Заголовков меню
        - Подпунктов меню
        - Сообщений об ошибках
        - Сообщений об успешном выполнении операций
        - Подсказок для ввода пользователя

    Каждое задание и главное меню реализованы как вложенные классы.
    """

    class MENU_MAIN:
        """Сообщения для главного меню приложения."""
        title = "=== ГЛАВНОЕ МЕНЮ ==="
        options = [
            "1. Задание 1 ",
            "2. Задание 2 ",
            "3. Задание 3 ",
            "0. Выход"
        ]
        prompt = "Выберите пункт: "          # приглашение для ввода
        invalid = "Неверный пункт!"          # сообщение при неверном выборе
        exit_msg = "Выход из программы..."   # сообщение при завершении


    class TASK1:
        """Сообщения для меню задачи 1."""
        title = "=== ЗАДАНИЕ 1 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Подсчитать общие числа с учётом реверса",
            "4. Показать результат",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        calculation_done = "Подсчёт выполнен."
        no_data = "Сначала введите массивы!"
        invalid_choice = "Неверный пункт!"

    class TASK2:
        """Сообщения для меню задачи 2."""
        title = "=== ЗАДАНИЕ 2 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Найти индексы, где arr1+arr2==arr3, и возвести суммы в степень",
            "4. Показать массивы и результаты",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        calculation_done = "Вычисления выполнены."
        no_data = "Сначала введите массивы!"
        invalid_choice = "Неверный пункт!"

    class TASK3:
        """Сообщения для меню задачи 3."""
        title = "=== ЗАДАНИЕ 3 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Выполнить подсчет",
            "4. Показать результат",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        calculation_done = "Операция выполнена."
        no_data = "Массивы ещё не введены или не сгенерированы!"
        invalid_choice = "Неверный пункт!"


# Словарь MESSAGES для совместимости с существующими FSM
MESSAGES = {
    "main_menu": {
        "title": Messages.MENU_MAIN.title,
        "options": Messages.MENU_MAIN.options,
        "prompt": Messages.MENU_MAIN.prompt,
        "invalid": Messages.MENU_MAIN.invalid,
        "exit": Messages.MENU_MAIN.exit_msg
    },
    "task1": {
        "title": Messages.TASK1.title,
        "menu": Messages.TASK1.menu,
        "prompt": Messages.TASK1.prompt,
        "input_error": Messages.TASK1.input_error,
        "calculation_done": Messages.TASK1.calculation_done,
        "no_data": Messages.TASK1.no_data,
        "invalid_choice": Messages.TASK1.invalid_choice
    },
    "task2": {
        "title": Messages.TASK2.title,
        "menu": Messages.TASK2.menu,
        "prompt": Messages.TASK2.prompt,
        "input_error": Messages.TASK2.input_error,
        "calculation_done": Messages.TASK2.calculation_done,
        "no_data": Messages.TASK2.no_data,
        "invalid_choice": Messages.TASK2.invalid_choice
    },
    "task3": {
        "title": Messages.TASK3.title,
        "menu": Messages.TASK3.menu,
        "prompt": Messages.TASK3.prompt,
        "input_error": Messages.TASK3.input_error,
        "calculation_done": Messages.TASK3.calculation_done,
        "no_data": Messages.TASK3.no_data,
        "invalid_choice": Messages.TASK3.invalid_choice
    }
}
