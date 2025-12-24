import asyncio    # асинхронный запуск бота
from logger import logger

# aiogram — библиотека для создания Telegram-ботов
from aiogram import Bot, Dispatcher, F            #объект бота (работа с API), управляет обработчиками сообщений, фильтр для сообщени
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton  #объект входящего сообщения, для создания кнопок клавиатуры
from aiogram.fsm.context import FSMContext        #объект состояния FSM (Finite State Machine) для хранения текущих данных пользователя
from aiogram.fsm.state import State, StatesGroup  #определяют состояния конечного автомата (FSM)

from messages import MESSAGES                     #словарь с текстами меню и сообщений для всех задач
from exceptions import InputError, DataNotSetError, OperationError
from task_1 import count_common_with_reverses, generate_array as generate_array1
from task_2 import sum_and_power, generate_array as generate_array2
from task_3 import sort_and_sum_arrays, generate_array as generate_array3

bot = Bot(token='8546433771:AAHmSoxSpCEyqavHzyoBYeLX3_9bcv3IDNI') # объект бота с токеном
dp = Dispatcher() # диспетчер, который будет обрабатывать сообщения и управлять FSM


# определение состояний FSM
class MainFSM(StatesGroup):    # состояние главного меню
    menu = State()             # состояние в котором пользователь выбирает задачу

class Task1FSM(StatesGroup):   # состояние для задачи 1
    menu = State()             # пользователь находится в меню задачи 1
    input_arrays = State()     # ввод массивов вручную

class Task2FSM(StatesGroup):   # состояние для задачи 2
    menu = State()             # пользователь находится в меню задачи 2
    input_arrays = State()     # ввод массивов вручную
    input_op = State()         # ввод операции

class Task3FSM(StatesGroup):   # состояние для задачи 3
    menu = State()             # пользователь находится в меню задачи 3
    input_arrays = State()     # ввод массивов вручную


# создание интерактивной клавиатуры
main_kb = ReplyKeyboardMarkup( # показывает кнопки прямо в чате
    keyboard=[[KeyboardButton(text="Задание 1")], # список списков кнопок
              [KeyboardButton(text="Задание 2")],
              [KeyboardButton(text="Задание 3")]],
    resize_keyboard=True       # клавиатура подстраивается под экран
)

task1_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ввести массивы вручную")],
        [KeyboardButton(text="Сгенерировать массивы случайно")],
        [KeyboardButton(text="Подсчитать общие числа с учётом реверса")],
        [KeyboardButton(text="Показать результат")],
        [KeyboardButton(text="Назад в главное меню")],
    ],
    resize_keyboard=True
)

task2_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ввести массивы вручную")],
        [KeyboardButton(text="Сгенерировать массивы случайно")],
        [KeyboardButton(text="Найти индексы, где arr1+arr2==arr3, и возвести суммы в степень")],
        [KeyboardButton(text="Показать массивы и результаты")],
        [KeyboardButton(text="Назад в главное меню")],
    ],
    resize_keyboard=True
)

task3_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ввести массивы вручную")],
        [KeyboardButton(text="Сгенерировать массивы случайно")],
        [KeyboardButton(text="Выполнить подсчет")],
        [KeyboardButton(text="Показать результат")],
        [KeyboardButton(text="Назад в главное меню")],
    ],
    resize_keyboard=True
)


# обработчик команды "/start"
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    logger.info(f"{message.from_user.id} запустил бота (/start)")
    await message.answer("Выберите задание:", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)


# ------------------ Главное меню ----------------------

# обработчики выбора задач
@dp.message(MainFSM.menu, F.text == "Задание 1")
async def start_task1(message: Message, state: FSMContext):
    await message.answer(MESSAGES["task1"]["title"], reply_markup=task1_kb)
    await state.set_state(Task1FSM.menu)

@dp.message(MainFSM.menu, F.text == "Задание 2")
async def start_task2(message: Message, state: FSMContext):
    await message.answer(MESSAGES["task2"]["title"], reply_markup=task2_kb)
    await state.set_state(Task2FSM.menu)

@dp.message(MainFSM.menu, F.text == "Задание 3")
async def start_task3(message: Message, state: FSMContext):
    await message.answer(MESSAGES["task3"]["title"], reply_markup=task3_kb)
    await state.set_state(Task3FSM.menu)


# ------------------ для Задачи 1: ----------------------

# ввод массивов вручную, бот ждет, пока пользователь введёт два массива
@dp.message(Task1FSM.menu, F.text == "Ввести массивы вручную")
async def task1_input(message: Message, state: FSMContext):
    logger.info(f"{message.from_user.id} выбрал ввод массивов для Задачи 1")
    await message.answer("Введите два массива через ; (пример: 1 2 3;4 5 6)")
    await state.set_state(Task1FSM.input_arrays)

# Получаем текст от пользователя, разделяем на два массива
@dp.message(Task1FSM.input_arrays)
async def task1_save_arrays(message: Message, state: FSMContext):
    try:
        arr1_text, arr2_text = message.text.split(";")
        arr1 = list(map(int, arr1_text.split()))
        arr2 = list(map(int, arr2_text.split()))
        await state.update_data(arr1=arr1, arr2=arr2, result=None)
        await message.answer("Массивы сохранены", reply_markup=task1_kb)
        await state.set_state(Task1FSM.menu)
        logger.info(f"{message.from_user.id} ввел массивы для Задачи 1: A={arr1}, B={arr2}")

    except Exception as e:
        logger.error(f"{message.from_user.id} ошибка ввода массивов для Задачи 1: {e}")
        raise InputError("Некорректный ввод массивов")

# генерация массивов
@dp.message(Task1FSM.menu, F.text == "Сгенерировать массивы случайно")
async def task1_generate(message: Message, state: FSMContext):
    try:
        arr1 = generate_array1(5)
        arr2 = generate_array1(5)
        await state.update_data(arr1=arr1, arr2=arr2, result=None)
        await message.answer(f"A={arr1}\nB={arr2}", reply_markup=task1_kb)
        logger.info(f"{message.from_user.id} сгенерировал массивы для Задачи 1: A={arr1}, B={arr2}")

    except Exception as e:
        logger.error(f"{message.from_user.id} ошибка генерации массивов для Задачи 1: {e}")
        raise OperationError("Ошибка при генерации массивов")

# выполнение операции
@dp.message(Task1FSM.menu, F.text.contains("Подсчитать"))
async def task1_compute(message: Message, state: FSMContext):
    data = await state.get_data()

    if "arr1" not in data or "arr2" not in data:
        logger.warning(f"{message.from_user.id} попытка вычисления Задачи 1 без массивов")
        raise DataNotSetError("Сначала введите массивы")

    result = count_common_with_reverses(data["arr1"], data["arr2"])
    await state.update_data(result=result)
    await message.answer("Вычисления выполнены.")
    await message.answer(f"Результат: {result}")
    logger.info(f"{message.from_user.id} вычислил Задачу 1, результат={result}")


# показ результата
@dp.message(Task1FSM.menu, F.text.contains("Показать"))
async def task1_show(message: Message, state: FSMContext):
    data = await state.get_data()
    if "result" not in data or data.get("result") is None:
        logger.warning(f"{message.from_user.id} попытка просмотра результата Задачи 1 без вычислений")
        raise DataNotSetError("Сначала введите массивы")
    await message.answer(f"Результат: {data['result']}")
    logger.info(f"{message.from_user.id} просмотрел результат Задачи 1: {data['result']}")


# кнопка назад
@dp.message(Task1FSM.menu, F.text.contains("Назад"))
async def task1_back(message: Message, state: FSMContext):
    logger.info(f"{message.from_user.id} вернулся в главное меню из Задачи 1")
    await message.answer("Главное меню", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)


# ------------------ для Задачи 2: ----------------------

# ввод массивов вручную
@dp.message(Task2FSM.menu, F.text.contains("Ввести"))
async def task2_input(message: Message, state: FSMContext):
    logger.info(f"{message.from_user.id} выбрал ввод массивов для Задачи 2")
    await message.answer("Введите три массива через ; (пример: 1 2 3;4 5 6;5 7 9)")
    await state.set_state(Task2FSM.input_arrays)


# сохранение массива после вызова
@dp.message(Task2FSM.input_arrays)
async def task2_save_arrays(message: Message, state: FSMContext):
    try:
        arr1_text, arr2_text, arr3_text = message.text.split(";")

        arr1 = list(map(int, arr1_text.split()))
        arr2 = list(map(int, arr2_text.split()))
        arr3 = list(map(int, arr3_text.split()))

        await state.update_data(arr1=arr1, arr2=arr2, arr3=arr3, result=None)

        await message.answer("Массивы сохранены", reply_markup=task2_kb)
        await state.set_state(Task2FSM.menu)
        logger.info(f"{message.from_user.id} ввел массивы для Задачи 2: A={arr1}, B={arr2}, C={arr3}")

    except Exception as e:
        logger.error(f"{message.from_user.id} ошибка ввода массивов для Задачи 2: {e}")
        raise InputError("Некорректный ввод массивов")


    # генерация массивов случайно
@dp.message(Task2FSM.menu, F.text.contains("Сгенерировать"))
async def task2_generate(message: Message, state: FSMContext):
    try:
        arr1 = generate_array2(5)
        arr2 = generate_array2(5)
        arr3 = generate_array2(5)
        await state.update_data(arr1=arr1, arr2=arr2, arr3=arr3, result=None)
        await message.answer(f"A={arr1}\nB={arr2}\nC={arr3}", reply_markup=task2_kb)
        logger.info(f"{message.from_user.id} сгенерировал массивы для Задачи 2: A={arr1}, B={arr2}, C={arr3}")
    except Exception as e:
        logger.error(f"{message.from_user.id} ошибка генерации массивов для Задачи 2: {e}")
        raise OperationError("Ошибка при генерации массивов")


# выполнение основной операции
@dp.message(Task2FSM.menu, F.text.contains("Найти"))
async def task2_compute(message: Message, state: FSMContext):
    data = await state.get_data()
    if "arr1" not in data or "arr2" not in data or "arr3" not in data:
        logger.warning(f"{message.from_user.id} попытка вычисления Задачи 2 без массивов")
        raise DataNotSetError("Сначала введите массивы")
    result = sum_and_power(data["arr1"], data["arr2"], data["arr3"])
    await state.update_data(result=result)
    await message.answer("Вычисления выполнены.")
    logger.info(f"{message.from_user.id} вычислил Задачу 2, результат={result}")


# показать результат
@dp.message(Task2FSM.menu, F.text.contains("Показать"))
async def task2_show(message: Message, state: FSMContext):
    data = await state.get_data()
    if "result" not in data:
        logger.warning(f"{message.from_user.id} попытка просмотра результата Задачи 2 без вычислений")
        raise DataNotSetError("Сначала введите массивы")
    result = data["result"]
    if len(result) == 0:
        await message.answer("Совпадений не найдено.\nРезультат пустой.")
        logger.info(f"{message.from_user.id} просмотрел результат Задачи 2: совпадений нет")
        return
    text = "\n".join([f"Index {r['index']}: sum={r['sum']}, power={r['power']}" for r in result])
    await message.answer(text)
    logger.info(f"{message.from_user.id} просмотрел результат Задачи 2: {result}")


# назад в главное меню
@dp.message(Task2FSM.menu, F.text.contains("Назад"))
async def task2_back(message: Message, state: FSMContext):
    await message.answer("Главное меню", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)
    logger.info(f"{message.from_user.id} вернулся в главное меню из Задачи 2")


# ------------------ для Задачи 3: ----------------------

# ввод массивов вручную
@dp.message(Task3FSM.menu, F.text == "Ввести массивы вручную")
async def task3_input(message: Message, state: FSMContext):
    logger.info(f"{message.from_user.id} выбрал ввод массивов для Задачи 3")
    await message.answer("Введите два массива через ; (пример: 1 2 3;4 5 6)")
    await state.set_state(Task3FSM.input_arrays)

# сохранение массива после вызова
@dp.message(Task3FSM.input_arrays)
async def task3_save_arrays(message: Message, state: FSMContext):
    try:
        arr1_text, arr2_text = message.text.split(";")
        arr1 = list(map(int, arr1_text.split()))
        arr2 = list(map(int, arr2_text.split()))
        await state.update_data(arr1=arr1, arr2=arr2, result=None)
        await message.answer("Массивы сохранены", reply_markup=task3_kb)
        await state.set_state(Task3FSM.menu)
        logger.info(f"{message.from_user.id} ввел массивы для Задачи 3: A={arr1}, B={arr2}")
    except Exception as e:
        logger.error(f"{message.from_user.id} ошибка ввода массивов для Задачи 3: {e}")
        raise InputError("Некорректный ввод массивов")

# генерация массивов случайно
@dp.message(Task3FSM.menu, F.text == "Сгенерировать массивы случайно")
async def task3_generate(message: Message, state: FSMContext):
    try:
        arr1 = generate_array3(5)
        arr2 = generate_array3(5)
        await state.update_data(arr1=arr1, arr2=arr2, result=None)
        await message.answer(f"A={arr1}\nB={arr2}", reply_markup=task3_kb)
        logger.info(f"{message.from_user.id} сгенерировал массивы для Задачи 3: A={arr1}, B={arr2}")
    except Exception as e:
        logger.error(f"{message.from_user.id} ошибка генерации массивов для Задачи 3: {e}")
        raise OperationError("Ошибка при генерации массивов")

# выполнение основной операции
@dp.message(Task3FSM.menu, F.text.contains("Выполнить"))
async def task3_compute(message: Message, state: FSMContext):
    data = await state.get_data()
    if "arr1" not in data or "arr2" not in data:
        logger.warning(f"{message.from_user.id} попытка вычисления Задачи 3 без массивов")
        raise DataNotSetError("Сначала введите массивы")
    result = sort_and_sum_arrays(data["arr1"], data["arr2"])
    await state.update_data(result=result)
    await message.answer(MESSAGES["task3"]["calculation_done"], reply_markup=task3_kb)
    logger.info(f"{message.from_user.id} вычислил Задачу 3, результат={result}")

# показать результат
@dp.message(Task3FSM.menu, F.text.contains("Показать"))
async def task3_show(message: Message, state: FSMContext):
    data = await state.get_data()
    if "result" not in data or data.get("result") is None:
        logger.warning(f"{message.from_user.id} попытка просмотра результата Задачи 3 без вычислений")
        raise DataNotSetError("Сначала введите массивы")
    await message.answer(f"Результат: {data['result']}")
    logger.info(f"{message.from_user.id} просмотрел результат Задачи 3: {data['result']}")

# назад в главное меню
@dp.message(Task3FSM.menu, F.text.contains("Назад"))
async def task3_back(message: Message, state: FSMContext):
    await message.answer("Главное меню", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)
    logger.info(f"{message.from_user.id} вернулся в главное меню из Задачи 3")


# запуск бота
async def main():
    logger.info("Бот запускается.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
