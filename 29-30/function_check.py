import random
import timeit
from exceptions import DataNotSetError, InvalidValueError

# -------------------------------
# НЕЭФФЕКТИВНАЯ ВЕРСИЯ
# -------------------------------

def generate_array_slow(size: int, min_v: int = 0, max_v: int = 50) -> list[int]:
    if size <= 0:   # если размер неправильный
        raise InvalidValueError("Размер массива должен быть положительным")
    return [random.randint(min_v, max_v) for _ in range(size)]


def reverse_num_slow(x: int) -> int:
    return int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)


def count_common_slow(arr1: list[int], arr2: list[int]) -> int:
    if not arr1 or not arr2:
        raise DataNotSetError("Массивы не заданы или пусты")

    count = 0
    used_pairs = set()  # заменили список на set

    try:
        for a in arr1:
            rev_a = reverse_num_slow(a)  # вычисляем перевернутый один раз
            for b in arr2:
                rev_b = reverse_num_slow(b)
                if a == b or a == rev_b or rev_a == b:
                    pair = (min(a, b), max(a, b))
                    if pair not in used_pairs:
                        used_pairs.add(pair)
                        count += 1
    except Exception as e:
        raise OperationError(f"Ошибка выполнения подсчёта: {e}") from e

    return count


# -------------------------------
# ЭФФЕКТИВНАЯ ВЕРСИЯ
# -------------------------------

generate_array = lambda size, a=0, b=50: (
    size <= 0 and (_ for _ in ()).throw(InvalidValueError("Размер массива должен быть положительным"))
    or [random.randint(a, b) for _ in range(size)]
)

reverse_int = lambda x: int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)


count_common_fast = lambda arr1, arr2: (
    (not arr1 or not arr2) and (_ for _ in ()).throw(DataNotSetError("Массивы пустые"))
    or len({tuple(sorted((a, b))) for a in arr1 for b in arr2 if a == b or reverse_int(a) == b or a == reverse_int(b)})
)

# -------------------------------
# ТЕСТОВЫЕ ДАННЫЕ
# -------------------------------

N = 10000

a = generate_array(N, -99_999, 99_999)
b = generate_array(N, -99_999, 99_999)

# -------------------------------
# БЕНЧМАРК
# -------------------------------

slow_time = timeit.timeit(lambda: count_common_slow(a, b), number=10)
fast_time = timeit.timeit(lambda: count_common_fast(a, b), number=10)

print("Размер массивов:", N)
print("Медленная версия:", slow_time)
print("Быстрая версия:  ", fast_time)
print("Ускорение:", round(slow_time / fast_time, 2), "раз")
