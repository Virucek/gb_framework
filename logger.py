import os
import time
from datetime import datetime

from patterns.creational.singletones import SingletoneName


# Применение здесь паттерна комманды
class Logger(metaclass=SingletoneName):

    def __init__(self, name):
        datetime_ = datetime.now().strftime("%d.%m.%y_%I_%M")
        self.name = name
        self.logfile = os.path.join('logs', f'{self.name}-{datetime_}')
        self._log_commands = []

    def add_log_method(self, method):
        self._log_commands.append(method)

    def log(self, text):
        for command in self._log_commands:
            command(text)

    def debug(self, func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            self.log(f'debug ---- call {func.__name__}, exec time = {(end - start):.3f} sec')
            return result
        return wrapper

    def write_console(self, text):
        print(f'logger -- {text}')

    def write_file(self, text):
        with open(self.logfile, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} ------- {text}\n')




