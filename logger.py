import os
from datetime import datetime

from patterns.creational.singletones import SingletoneName


class Logger(metaclass=SingletoneName):

    def __init__(self, name):
        datetime_ = datetime.now().strftime("%d.%m.%y_%I:%M")
        self.name = name
        self.logfile = os.path.join('logs', f'{self.name}-{datetime_}')

    def log(self, text):
        print(f'logger -- {text}')
        with open(self.logfile, 'w', encoding='utf-8') as f:
            f.write(f'{datetime.now()} ------- {text}')
