import sqlite3

from models import Student, Category, Course, OnlineCourse, OfflineCourse

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
        statement = f'SELECT * FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
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
        statement = f'SELECT * FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        print('result category by id', result)
        if result:
            id, name, parent_category = result
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
    def __init__(self, connection, type):
        super().__init__(connection)
        self.type = type
        self.tablename = 'courses'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for rec in self.cursor.fetchall():
            id, name, type, category = rec
            if type == 'online':
                course = OnlineCourse(name, category)
            else:
                course = OfflineCourse(name, category)
            course.id = id
            result.append(course)
        return result

    def get_by_id(self, id):
        statement = f'SELECT name, type, category FROM {self.tablename} WHERE id = ?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            name, type_, category = result
            if type_ == 'online':
                return OnlineCourse(name, category)
            else:
                return OfflineCourse(name, category)
        else:
            raise RecordNotFoundException(f'record with id = {id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (id, name)' \
                        f' VALUES (?, ?, ?)'
        self.cursor.execute(statement, (obj.id, obj.name, obj.type,))
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


class CategoryCourseMapper(BaseMapper):

    def __init__(self, connection):
        super().__init__(connection)
        self.tablename = 'category_course'

    def get_by_category_id(self, cat_id, course_mapper):
        statement = f'SELECT course_id FROM {self.tablename} WHERE category_id = ?'
        self.cursor.execute(statement, (cat_id,))
        result = []
        for course_id in self.cursor.fetchall():
            result.append(course_mapper.get_by_id(course_id))
        return result

    def insert(self, category, course):
        statement = f'INSERT INTO {self.tablename} (CATEGORY_ID, COURSE_ID) ' \
                    f'VALUES (?, ?)'
        self.cursor.execute(statement, (course.id, category.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e)

    def delete(self, category, course):
        statement = f'DELETE FROM {self.tablename} WHERE category_id = ? AND course_id = ?'
        self.cursor.execute(statement, (category.id, course.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e)


class MapperRegistry:
    mappers = {
        'students': StudentMapper,
        'categories': CategoryMapper,
        'courses': CourseMapper,
        'category_course': CategoryCourseMapper,
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

    @classmethod
    def get_curr_mapper(cls, name):
        return cls.mappers[name](conn)
