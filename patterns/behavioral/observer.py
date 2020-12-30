import abc


class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None

    @abc.abstractmethod
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self)
