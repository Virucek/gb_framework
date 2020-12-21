import os
import time
from datetime import datetime

from patterns.creational.singletones import SingletoneName


class Logger(metaclass=SingletoneName):

    def __init__(self, name):
        datetime_ = datetime.now().strftime("%d.%m.%y_%I_%M")
        self.name = name
        self.logfile = os.path.join('logs', f'{self.name}-{datetime_}')

    def log(self, text):
        print(f'logger -- {text}')
        with open(self.logfile, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} ------- {text}\n')

    def debug(self, func):
        def wrapper():
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            print(f'debug ---- call {func.__name__}, exec time = {end - start} sec')
            self.log(f'debug ---- call {func.__name__}, exec time = {end - start} sec')
        return wrapper
