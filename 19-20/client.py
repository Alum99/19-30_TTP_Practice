import threading                # нужен для запуска каждого клиента в отдельном потоке
import time                     # для пауз между отправкой запросов, чтобы эмулировать реальные задержки
import random
from datetime import datetime   # для печати текущего времени

# возвращает текущее время в формате чч:мм:сс
def ts():
    return datetime.now().strftime("%H:%M:%S")

# Определение класса клиента
class ClientThread(threading.Thread):
    """
    Поток-клиент, который генерирует/отправляет запросы серверу и получает
    результаты через callback.

    Parameters:
    name : str - Читабельное имя клиента, используемое в логах.
    request_queue : queue.Queue - Очередь для отправки запросов на сервер.
    actions : list of dict - Список действий (сценарий) для данного клиента.

    Каждый элемент — словарь со следующими ключами:
    - 'task' : str
    Имя задачи (reverse, common, sort и т.д.).
    - 'generate' : bool, optional
    Если True — клиент сам сгенерирует данные (массивы).
    - 'params' : dict, optional
    Дополнительные параметры задачи (например, длина массива, индексы и т.д.).
    - 'data' : any, optional
    Явно указанные данные для отправки (если не генерировать).

    Methods:
    run()
    Переопределённый метод потока; генерирует/отправляет запросы и завершает работу.
    _callback(client_name, task, result, input_data)
    Метод, вызываемый сервером при завершении обработки запроса; печатает
    входные данные и результат и сохраняет их в `self.results`.
    """

    def __init__(self, name: str, request_queue, actions):
        super().__init__(daemon=True)         # поток будет автоматически завершаться при закрытии главного потока программы
        self.name = name                      # читаемое имя клиента
        self.request_queue = request_queue    # общая очередь, в которую клиент кладёт запросы для сервера
        self.actions = actions                # список действий/задач, которые клиент должен выполнить
        self.results = []                     # результаты всех выполненных задач

    # запускается при старте потока(t.start())
    def run(self):
        print(f"{ts()} {self.name}: клиент запущен")  # старт клиента с текущим временем
        time.sleep(random.uniform(0.05, 0.25))  # пауза эмулирует запуск нескольких клиентов не одновременно

        # Проходим по всем действиям клиента
        for action in self.actions:
            task = action['task']               # имя задачи (reverse, common, sort и т.д.)
            params = action.get('params', {})   # дополнительные параметры для задачи
            data = action.get('data')           # данные для задачи (массивы, числа и т.д.)

            # генерация данных
            if action.get('generate', False):  # если флаг generate=True, клиент сам создаёт данные для задачи
                if task == 'common':
                    la = params.get('len_a', 7)
                    lb = params.get('len_b', 6)
                    a = [random.randint(0, 99) for _ in range(la)]
                    b = [random.randint(0, 99) for _ in range(lb)]
                    data = {'arr1': a, 'arr2': b}
                    print(f"{ts()} {self.name}: сгенерированы массивы для find_common_numbers")
                    print("A =", a)
                    print("B =", b)
                    print()
                elif task in ('process',):
                    la = lb = params.get('len_a', 5)
                    a = [random.randint(0, 9) for _ in range(la)]
                    b = [random.randint(0, 9) for _ in range(lb)]
                    data = {'arr1': a, 'arr2': b}
                    print(f"{ts()} {self.name}: сгенерированы массивы для process_arrays")
                    print("A =", a)
                    print("B =", b)
                    print()
                elif task in ('compute',):
                    la = lb = lc = params.get('len', 4)
                    a = [random.randint(0, 9) for _ in range(la)]
                    b = [random.randint(0, 9) for _ in range(lb)]
                    c = [random.randint(0, 9) for _ in range(lc)]
                    data = {'arr1': a, 'arr2': b, 'arr3': c}
                    print(f"{ts()} {self.name}: сгенерированы массивы для compute_power_for_matching_sums")
                    print("A =", a)
                    print("B =", b)
                    print("C =", c)
                    print()

            # Отправка запроса на сервер
            print(f"{ts()} {self.name}: отправлен запрос на {self._task_name(task)}")
            # словарь запроса, который помещается в очередь для сервера
            request = {
                'client': self.name,         # имя клиента
                'task': task,                # ключ задачи
                'data': data,                # входные данные для задачи
                'params': params,            # словарь с дополнительными параметрами задачи
                'callback': self._callback   # функция _callback, чтобы вернуть результат клиенту
            }
            self.request_queue.put(request)  # отправка запроса в очередь

            time.sleep(random.uniform(0.2, 0.9))

        print(f"{ts()} {self.name}: выполнение завершено")

    # Метод _callback, вызывается после выполнения задачи
    def _callback(self, client_name, task, result, input_data):
        # Коллбек вызывается сервером — печатаем ясно: вход -> результат
        print(f"{ts()} {self.name}: получен результат для {self._task_name(task)}")
        # показываем входные данные (дублируем — полезно если очередь/параллельность меняют порядок)
        if task == 'common':  # find_common_numbers
            print("Массив A:", input_data['arr1'])
            print("Массив B:", input_data['arr2'])
            print("Количество общих чисел:", result)
            print()
        elif task == 'process':  # process_arrays
            print("Массив A:", input_data['arr1'])
            print("Массив B:", input_data['arr2'])
            print("Результат обработки:", result)
            print()
        elif task == 'compute':  # compute_power_for_matching_sums
            print("Массив A:", input_data['arr1'])
            print("Массив B:", input_data['arr2'])
            print("Массив C:", input_data['arr3'])
            print("Результаты вычислений:", result)
            print()
        else:
            print("Результат:", result)
            print()

        # Сохраняем результат в список
        self.results.append((task, result))

    # Метод для отображения читаемого имени задачи
    def _task_name(self, task_key):
        mapping = {
            'common': 'find_common_numbers',
            'process': 'process_arrays',
            'compute': 'compute_power_for_matching_sums'
        }
        return mapping.get(task_key, task_key)
