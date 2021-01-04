import os
import time
from datetime import datetime

from patterns.creational.singletones import SingletoneName

LOG_DIR = 'logs'


# Класс записи в консоль
class ConsoleWriter:
    def write(self, text):
        print(f'logger ------- {text}')


# Класс записи в файл
class FileWriter:
    def __init__(self, name):
        datetime_ = datetime.now().strftime("%d.%m.%y_%I_%M")
        self.file = os.path.join(LOG_DIR, f'{name}-{datetime_}')

    def write(self, text):
        with open(self.file, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} ------- {text}\n')


# Применение паттерна стратегии
class Logger(metaclass=SingletoneName):

    def __init__(self, name, write_strategy):
        self.name = name
        self.writer = write_strategy

    def log(self, text):
        self.writer.write(text)

    def debug(self, func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f'debug ---- call {func.__name__}, exec time = {(end - start):.3f} sec')
            return result
        return wrapper
