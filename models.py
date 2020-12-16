""" Модели проекта """


# Пользователи
class User:
    pass


class Student(User):
    pass


class Teacher(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_name):
        return cls.types[type_name]()


# Категории Курсов
class Category:
    id_ = 0

    def __init__(self, name):
        self.id = Category.id_
        Category.id_ += 1
        self.name = name
        self.courses = []


# Курсы
class Course:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class OnlineCourse(Course):
    pass


class OfflineCourse(Course):
    pass


class CourseFactory:
    types = {
        'online': OnlineCourse,
        'offline': OfflineCourse,
    }

    @classmethod
    def create(cls, type_name, name, category):
        return cls.types[type_name](name, category)


# Основной интерфейс
class MainInterface:

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_name):
        return UserFactory.create(type_name)

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_course(type_name, name, category):
        return CourseFactory.create(type_name, name, category)

    def get_category_by_id(self, category_id):
        for cat in self.categories:
            if cat.id == category_id:
                return cat
        raise Exception(f'Категория с id {id} отсутствует')
