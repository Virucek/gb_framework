""" Модели проекта """


# Пользователи -- Not used right now
from patterns.creational.prototype import PrototypeMixin


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

    def __init__(self, name, parent_category):
        self.id = Category.id_
        Category.id_ += 1
        self.name = name
        self.courses = []
        self.parent_category = parent_category
        self.child_categories = []

    def course_count(self):
        course_count = len(self.courses)
        if self.child_categories:
            for cat_ in self.child_categories:
                course_count += cat_.course_count()
        return course_count

    def add_child(self, category):
        self.child_categories.append(category)


# Курсы
class Course(PrototypeMixin):

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
    def create_category(name, parent_category=None):
        category = Category(name, parent_category)
        if parent_category is not None:
            parent_category.add_child(category)
        return category

    @staticmethod
    def create_course(type_name, name, category):
        return CourseFactory.create(type_name, name, category)

    def get_category_by_id(self, category_id):
        for cat in self.categories:
            if cat.id == category_id:
                return cat
        raise Exception(f'Категория с id {id} отсутствует')

    def get_courses_by_category(self, category_id):
        category = self.get_category_by_id(int(category_id))
        return category.courses

    @staticmethod
    def get_course_types():
        return list(CourseFactory.types.keys())

    def get_course_by_name(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        raise Exception(f'Курс с именем {name} отсутствует')
