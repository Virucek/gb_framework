import sqlite3

from models import Student, Category, Course, OnlineCourse, OfflineCourse, CourseStudent

dbname = 'db.sqlite'
conn = sqlite3.connect(dbname)


class RecordNotFoundException(Exception):
    def __init__(self, text):
        super().__init__(f'Record not found error: {text}')


class CommitException(Exception):
    def __init__(self, text):
        super().__init__(f'DB Commit error: {text}')


class DeleteException(Exception):
    def __init__(self, text):
        super().__init__(f'DB Delete error: {text}')


class BaseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'tablename'


class StudentMapper(BaseMapper):

    def __init__(self, connection):
        super().__init__(connection)
        self.tablename = 'students'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for rec in self.cursor.fetchall():
            id, name = rec
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def get_by_id(self, id):
        statement = f'SELECT name FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            name_ = result[0]
            student = Student(name_)
            student.id = id
            return student
        else:
            raise RecordNotFoundException(f'record with id = {id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e)


class CategoryMapper(BaseMapper):

    def __init__(self, connection):
        super().__init__(connection)
        self.tablename = 'categories'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for rec in self.cursor.fetchall():
            id, name, parent_category = rec
            category = Category(name, parent_category)
            category.id = id
            result.append(category)
        return result

    def get_by_id(self, id):
        statement = f'SELECT name, parent_category FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        print('result category by id', result)
        if result:
            name, parent_category = result
            category = Category(name, parent_category)
            category.id = id
            return category
        else:
            raise RecordNotFoundException(f'record with id = {id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name, parent_category)' \
                    f' VALUES (?, ?)'
        print('obj', obj, obj.name, obj.parent_category,)
        if obj.parent_category is not None:
            self.cursor.execute(statement, (obj.name, obj.parent_category.id,))
        else:
            self.cursor.execute(statement, (obj.name, obj.parent_category,))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e)


class CourseMapper(BaseMapper):
    def __init__(self, connection, type_=None):
        super().__init__(connection)
        self.type_ = type_
        self.tablename = 'courses'
        self.cat_mapper = MapperRegistry.get_curr_mapper('categories')

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for rec in self.cursor.fetchall():
            id, name, type_, category_id = rec
            category = self.cat_mapper.get_by_id(category_id)
            if type_ == 'online':
                course = OnlineCourse(name, category)
            else:
                course = OfflineCourse(name, category)
            course.id = id
            result.append(course)
        return result

    def get_by_id(self, id):
        statement = f'SELECT name, type, category_id FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            name, type_, category_id = result
            category = self.cat_mapper.get_by_id(category_id)
            if type_ == 'online':
                course = OnlineCourse(name, category)
            else:
                course = OfflineCourse(name, category)
            course.id = id
            return course
        else:
            raise RecordNotFoundException(f'record with id = {id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name, type, category_id)' \
                        f' VALUES (?, ?, ?)'
        self.cursor.execute(statement, (obj.name, self.type_, obj.category.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e)


class CourseStudentMapper(BaseMapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.tablename = 'course_student'
        self.student_mapper = MapperRegistry.get_curr_mapper('students')

    def get_students_by_course(self, course):
        statement = f'SELECT student_id FROM {self.tablename} WHERE course_id = ?'
        self.cursor.execute(statement, (course.id,))
        result = self.cursor.fetchone()
        if result:
            student_id = result[0]
            student = self.student_mapper.get_by_id(student_id)
            return student
        else:
            raise RecordNotFoundException(f'record with course_id = {course.id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (course_id, student_id)' \
                        f' VALUES (?, ?)'
        self.cursor.execute(statement, (obj.course.id, obj.student.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e)

    def delete(self, obj):
        # todo: obj.id -- ?
        statement = f'DELETE FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e)


# class CategoryCourseMapper(BaseMapper):
#
#     def __init__(self, connection):
#         super().__init__(connection)
#         self.tablename = 'category_course'
#
#     def get_by_category_id(self, cat_id, course_mapper):
#         statement = f'SELECT course_id FROM {self.tablename} WHERE category_id = ?'
#         self.cursor.execute(statement, (cat_id,))
#         result = []
#         for course_id in self.cursor.fetchall():
#             result.append(course_mapper.get_by_id(course_id))
#         return result
#
#     def insert(self, category, course):
#         statement = f'INSERT INTO {self.tablename} (CATEGORY_ID, COURSE_ID) ' \
#                     f'VALUES (?, ?)'
#         self.cursor.execute(statement, (course.id, category.id,))
#         try:
#             self.connection.commit()
#         except Exception as e:
#             raise CommitException(e)
#
#     def delete(self, category, course):
#         statement = f'DELETE FROM {self.tablename} WHERE category_id = ? AND course_id = ?'
#         self.cursor.execute(statement, (category.id, course.id,))
#         try:
#             self.connection.commit()
#         except Exception as e:
#             raise DeleteException(e)


class MapperRegistry:
    mappers = {
        'students': StudentMapper,
        'categories': CategoryMapper,
        'courses': CourseMapper,
        'course_student': CourseStudentMapper,
        # 'category_course': CategoryCourseMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(conn)
        elif isinstance(obj, Category):
            return CategoryMapper(conn)
        elif isinstance(obj, OnlineCourse):
            return CourseMapper(conn, 'online')
        elif isinstance(obj, OfflineCourse):
            return CourseMapper(conn, 'offline')
        elif isinstance(obj, CourseStudent):
            return CourseStudentMapper(conn)

    @classmethod
    def get_curr_mapper(cls, name):
        return cls.mappers[name](conn)
