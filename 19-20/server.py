import threading # модуль для работы с потоками
import queue     # потокобезопасная очередь для передачи данных между потоками (клиенты → сервер).
import time      # для задержек (sleep).
import random    # для генерации случайного времени паузы
import logging   # модуль для записи логов в файл
from datetime import datetime # для форматирования текущего времени в консоль
from task_1 import find_common_numbers
from task_2 import compute_power_for_matching_sums
from task_3 import process_arrays

# Вспомогательная функция для отметки времени
def ts():
    return datetime.now().strftime("%H:%M:%S")  # возвращает текущие часы, минуты и секунды

# Логирование
logging.basicConfig(
    filename="server.log",                                 # файл для логирования
    level=logging.INFO,                                    # уровень логирования (фильтр сообщений)
    format="%(asctime)s - %(levelname)s - %(message)s",    # формат записи логов
    encoding="utf-8"                                       # кодировка файла
)
logger = logging.getLogger("server_logger") # создание логгера с именем "server_logger"

# ---------------------------------------------------------------------

# сервер наследует threading.Thread
class TaskServer(threading.Thread):
    """
    Серверный поток, который обрабатывает запросы из общей очереди.

    Parameters
        request_queue : queue.Queue - очередь, в которую клиенты кладут словари-запросы.

    Attributes:
        running : bool - флаг, управляющий основным циклом обработки.
        processed : int - счётчик обработанных запросов.

    Request format:
    {
        'client': str,          # имя клиента
        'task': str,            # 'reverse'|'common'|'sort'|'sum'|'check'|'power'
        'data': any,            # входные данные (списки, кортежи, словари)
        'params': dict,         # дополнительные параметры (по необходимости)
        'callback': callable    # функция для уведомления клиента
    }
    """

    def __init__(self, request_queue: queue.Queue): # конструктор класса, параметры: очередь запросов от клиентов
        super().__init__(daemon=True)          # поток сервера завершается автоматически при закрытии программы
        self.request_queue = request_queue     # очередь, в которую клиенты будут помещать запросы
        self.running = True                    # флаг, управляющий основным циклом сервера
        self.processed = 0                     # счетчик обработанных запросов

    # метод, который выполняется, когда вызывается server.start()
    def run(self):
        # Логи для демонстрации работы многопоточности
        logger.info("Сервер: инициализирован и готов к обработке запросов")
        logger.info("-" * 60)
        logger.info("ДЕМОНСТРАЦИЯ МНОГОПОТОЧНОСТИ В PYTHON")
        logger.info("-" * 60)
        logger.info("Сервер: один поток")
        logger.info("Клиенты: каждый в отдельном потоке")
        logger.info("-" * 60)
        logger.info(f"Основной поток: ID {threading.get_ident()}")
        logger.info(f"Активные потоки: {threading.active_count()}\n")
        logger.info("Запуск автоматической демонстрации...")
        logger.info("Клиенты будут выполнять команды автоматически\n")

        # Основной цикл обработки запросов
        while self.running:         # проверка очереди
            try:
                request = self.request_queue.get(timeout=0.5) # ждём запрос 0.5 секунды
            except queue.Empty:     # если очередь пустая - цикл продолжается
                continue

            client = request.get('client')      # имя клиента, чтобы писать в логи и консоль
            task = request.get('task')          # какая функция будет вызвана (reverse, sort, sum, etc)
            data = request.get('data')          # входные данные для функции
            params = request.get('params', {})  # дополнительные параметры (indexes, direction, op)
            callback = request.get('callback')  # функция клиента, которая получит результат после вычисления

            logger.info(f"{client}: получен запрос на {task}")
            print(f"{ts()} {client}: отправлен запрос на {task}") # для демонстрации многопоточности

            # эмуляция длительных расчетов
            # Эмуляция — это процесс имитации работы чего-либо в программе
            time.sleep(random.uniform(1, 3)) # случайная пауза 1–3 секунды

            result = None
            # выбираем функцию по ключу task
            try:  # ловля возможных ошибок
                if task == 'common':
                    result = find_common_numbers(data['arr1'], data['arr2'])  # Результат работы функции сохраняется в result
                elif task == 'power':
                    result = compute_power_for_matching_sums(
                        data['arr1'], data['arr2'], data['arr3'], params['indexes']
                    )
                elif task == 'process_arrays':
                    result = process_arrays(data['arr1'], data['arr2'])
                else:
                    result = {"error": "unknown task"}
            except Exception as e:             # перехват ошибки
                result = {"error": str(e)}     # сохраняем результат или ошибку
                logger.exception(f"Ошибка при обработке запроса {task} от {client}")

            self.processed += 1                           # увеличиваем счётчик обработанных задач
            logger.info(f"{client}: выполнен {task}")     # успещное выполнение
            print(f"{ts()} {client}: выполнен {task}")    # печатаем в консоль с временем для наглядности

            if callable(callback): # Если клиент передал функцию обратного вызова
                try:
                    callback(client, task, result, data) # вызываем её, передаем: имя клиента, задачу, результат и входные данные
                except Exception: # перехват ошибки
                    logger.exception(f"Ошибка в callback клиента {client}")

    def stop(self):
        self.running = False                                         # Останавливает основной цикл
        logger.info(f"Сервер обработал {self.processed} запросов")   # Логирует общее количество обработанных запросов
        # logger.exception — логирования ошибок вместе с информацией о текущем исключении
