import random
import time
from collections import OrderedDict


class CachedRange:
    def __init__(self, array, cache_size=1000):
        self.array = array
        self.cache = OrderedDict()  # Для ручного керування LRU-кешем
        self.cache_size = cache_size

    def range_sum_with_cache(self, L, R):
        key = (L, R)
        if key in self.cache:  # Якщо результат уже є в кеші
            # Оновлюємо кеш для LRU
            self.cache.move_to_end(key)
            return self.cache[key]

        # Результат не в кеші, потрібно обчислити
        result = sum(self.array[L:R + 1])
        self.cache[key] = result

        # Якщо кеш перевищує ліміт, видаляємо найстаріший елемент
        if len(self.cache) > self.cache_size:
            self.cache.popitem(last=False)

        return result

    def update_with_cache(self, index, value):
        # Оновлення значення у масиві
        self.array[index] = value
        # Видаляємо кешовані результати, які включають змінений індекс
        keys_to_delete = [
            key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_delete:
            del self.cache[key]


def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])


def update_no_cache(array, index, value):
    array[index] = value


# Налаштування для тестування
ELEMENTS = 100_000
Q = 50_000
random.seed(0)

array = [random.randint(1, 100) for _ in range(ELEMENTS)]
queries = []
for _ in range(Q):
    if random.choice(['Range', 'Update']) == 'Range':
        L = random.randint(0, ELEMENTS - 1)
        R = random.randint(L, ELEMENTS - 1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, ELEMENTS - 1)
        value = random.randint(1, 100)
        queries.append(('Update', index, value))

# Виконання запитів без кешу
start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        _, L, R = query
        range_sum_no_cache(array, L, R)
    elif query[0] == 'Update':
        _, index, value = query
        update_no_cache(array, index, value)
end_time = time.time()
no_cache_time = end_time - start_time

# Виконання запитів із кешем
cached_operations = CachedRange(array)
start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        _, L, R = query
        cached_operations.range_sum_with_cache(L, R)
    elif query[0] == 'Update':
        _, index, value = query
        cached_operations.update_with_cache(index, value)
end_time = time.time()
cache_time = end_time - start_time

# Результати
print("Час виконання без кешування:", no_cache_time, "секунд")
print("Час виконання з LRU-кешем:", cache_time, "секунд")
