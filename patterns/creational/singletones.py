""" Синглтоны """


class SingletoneName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs and 'name' in kwargs:
            name = kwargs['name']

        if name not in cls.__instance:
            cls.__instance[name] = super(SingletoneName, cls).__call__(*args, **kwargs)
        return cls.__instance[name]
