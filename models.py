""" Модели проекта """
import json

from patterns.behavioral.observer import Observer, Subject
from patterns.creational.prototype import PrototypeMixin


class User:
    def __init__(self, name):
        self.name = name


class Student(User):
    def __init__(self, name):
        self.courses = []
        super(Student, self).__init__(name)


class Teacher(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_name, name):
        return cls.types[type_name](name)


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

    def __getitem__(self, item):
        return self.courses[item]

    @property
    def course_count(self):
        res = len(self.courses)
        if self.child_categories:
            for cat_ in self.child_categories:
                res += cat_.course_count
        return res

    def add_child(self, category):
        self.child_categories.append(category)


# Курсы
class Course(PrototypeMixin, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)
        self._subject_state = student
        self._notify()

    @property
    def new_student(self):
        return self._subject_state


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


class SmsNotifier(Observer):
    def update(self, subject):
        print(f'SMS: студент {subject.new_student.name} присоединился к курсу {subject.name}')


class EmailNotifier(Observer):
    def update(self, subject):
        print(f'EMAIL: студент {subject.new_student.name} присоединился к курсу {subject.name}')


class BaseSerializer:
    def __init__(self, object):
        self.object = object

    def save(self):
        return json.dumps(self.object)

    def load(self):
        return json.loads(self.object)


# Основной интерфейс
class MainInterface:

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_name, name):
        return UserFactory.create(type_name, name)

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

    def get_category_tree(self):
        categories_list = []
        if self.categories:
            for cat in self.categories:
                if cat.parent_category is None:
                    categories_list.append(cat)
        return categories_list

    def get_students_by_course(self, course):
        course = self.get_course_by_name(course)
        return course.students

    def get_student_by_name(self, name):
        for student in self.students:
            if student.name == name:
                return student
        raise Exception(f'Студент с именем {name} отсутствует')
