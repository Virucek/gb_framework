import os
import sys

from controllers import *
from core.app import Application
from core.app_cbv import ListView, CreateView
from core.debug_app import DebugApplication
from core.fake_app import FakeApplication
from core.templator import render
from db.create_db import create_db
from db.mappers import MapperRegistry
from include.codes import *
from logger import Logger, FileWriter
from models import MainInterface, EmailNotifier, SmsNotifier, BaseSerializer
from patterns.orm.unit_of_work import UnitOfWork

site = MainInterface()
# Настройка логгера
logger = Logger('site', FileWriter('site'))
log = logger.log
debug = logger.debug

# Определение наблюдателей
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

# Определение Базы и мапперов
create_db()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
commit = UnitOfWork.get_current().commit


@debug
def index_view(request):
    title = 'Главная'
    _copyright = request.get('copyright')
    context = {
        'title': title,
        '_copyright': _copyright
    }
    return OK_200, render('index.html',
                          context=context)


@debug
def about_view(request):
    title = 'О проекте'
    _copyright = request.get('copyright')
    context = {
        'title': title,
        '_copyright': _copyright,
    }
    return OK_200, render('about.html',
                          context=context)


@debug
def contacts_view(request):
    title = 'Контакты'
    _copyright = request.get('copyright')
    context = {
        'title': title,
        '_copyright': _copyright,
    }
    if request['method'] == 'POST':
        data = request['data']
        f_time = datetime.now()
        # Записываем полученное сообщение в файл в директории temp_emails
        with open(os.path.join('temp_emails', f'email-{f_time.strftime("%d. %b %Y %I_%M")}'), 'w',
                  encoding='utf-8') as f:
            f.write(f"name: {data['name']}\n")
            f.write(f"theme: {data['theme']}\n")
            f.write(f"e-mail: {data['e-mail']}\n")
            f.write(f"text: {data['text']}\n")
    return OK_200, render('contacts.html',
                          context=context)


@debug
class CategoriesListView(ListView):
    title = 'Категории'
    template = 'categories.html'
    object_name_context = 'categories_list'

    def get_queryset(self):
        # return site.get_category_tree()
        mapper = MapperRegistry.get_curr_mapper('categories')
        return mapper.all()
        # todo: Вернуть древовидную структуру html документу (переписав шаблон или выдачу результатов)


@debug
class CategoryCreateView(CreateView):
    title = 'Создание категории'
    template = 'create_category.html'
    mapper = MapperRegistry.get_curr_mapper('categories')

    def get_context_data(self):
        context = super().get_context_data()
        categories = self.mapper.all()
        context['categories_list'] = categories
        return context

    def create_object(self, data):
        parent_category = None
        category_id = data.get('category_id')
        if category_id:
            parent_category = self.mapper.get_by_id(int(category_id))
        category_name = data['cat_name']
        category = site.create_category(category_name, parent_category)
        site.categories.append(category)
        category.mark_new()
        commit()


# @debug
# def create_category_view(request):
#     context = {
#         'title': 'Создание категории',
#         '_copyright': request.get('copyright'),
#         'categories_list': site.categories,
#     }
#
#     if request['method'] == 'POST':
#         data = request['data']
#         log(f'Полученные данные в запросе: \n {data}')
#         parent_category = None
#         category_id = data.get('category_id')
#         if category_id:
#             parent_category = site.get_category_by_id(int(category_id))
#         category = site.create_category(data['cat_name'], parent_category)
#         site.categories.append(category)
#         context['title'] = 'Категории'
#         context['categories_list'] = site.get_category_tree()
#         return CREATED_201, render('categories.html', context=context)
#
#     return OK_200, render('create_category.html', context=context)


@debug
class CoursesListView(ListView):
    title = 'Список курсов'
    template = 'courses.html'
    # queryset = site.courses
    object_name_context = 'courses_list'
 # todo: добавить фильтрацию по категориям

    def get_queryset(self):
        mapper = MapperRegistry.get_curr_mapper('courses')
        return mapper.all()


# def courses_view(request):
#     q_params = request['query_params']
#     if q_params.get('category_id'):
#         courses = site.get_courses_by_category(q_params['category_id'])
#     else:
#         courses = site.courses
#     context = {
#         'text': 'Список курсов',
#         '_copyright': request.get('copyright'),
#         'courses_list': courses,
#     }
#
#     return OK_200, render('courses.html', context=context)


routers = {
    '/': index_view,
    '/index/': index_view,
    '/about/': about_view,
    '/contacts/': contacts_view,
    # Категории
    '/category/': CategoriesListView(),
    '/category/create/': CategoryCreateView(),
    # Курсы
    '/course/': CoursesListView(),
}

controllers = {
    add_copyright_controller,
}

print(sys.argv)
if 'fake' in sys.argv:
    application = FakeApplication(routers, controllers)
elif 'debug' in sys.argv:
    application = DebugApplication(routers, controllers)
else:
    application = Application(routers, controllers)

app = application
log('Запущено приложение!')


@debug
@app.route('/course/create/')
class CourseCreateView(CreateView):
    title = 'Создание курса'
    template = 'create_course.html'
    # extra_context = {
    #     'categories_list': site.categories,
    #     'course_types': site.get_course_types(),
    # }
    course_mapper = MapperRegistry.get_curr_mapper('courses')
    category_mapper = MapperRegistry.get_curr_mapper('categories')

    def get_context_data(self):
        context = super().get_context_data()
        context['categories_list'] = self.category_mapper.all()
        context['course_types'] = site.get_course_types()
        return context

    def create_object(self, data):
        course_type = data['course_type']
        course_name = data['course_name']
        category = self.category_mapper.get_by_id(int(data['category_id']))
        new_course = site.create_course(course_type, course_name, category)
        site.courses.append(new_course)
        new_course.mark_new()
        commit()
        # Привязка наблюдателей к новому курсу
        new_course.attach(sms_notifier)
        new_course.attach(email_notifier)


# def create_course_view(request):
#     context = {
#         'title': 'Создание курса',
#         '_copyright': request.get('copyright'),
#     }
#
#     if request['method'] == 'POST':
#         data = request['data']
#         log(f'Полученные данные в запросе: \n {data}')
#         category = site.get_category_by_id(int(data['category_id']))
#         new_course = site.create_course(data['course_type'], data['course_name'], category)
#         site.courses.append(new_course)
#         # Привязка наблюдателей к новому курсу
#         new_course.attach(sms_notifier)
#         new_course.attach(email_notifier)
#
#         context['title'] = 'Список курсов'
#         context['courses_list'] = site.courses
#         return CREATED_201, render('courses.html', context=context)
#
#     context['categories_list'] = site.categories
#     context['course_types'] = site.get_course_types()
#     return OK_200, render('create_course.html', context=context)


@debug
@app.route('/course/copy/')  # todo: при копировании не добавляет в общий подсчет курсов по категориям
def copy_course_view(request):
    q_params = request['query_params']
    context = {
        'title': 'Список курсов',
        '_copyright': request.get('copyright'),
        'courses_list': site.courses,
    }
    if q_params.get('course'):
        old_course = site.get_course_by_name(q_params['course'])
        if old_course:
            new_course = old_course.clone()
            new_course.name = f'{old_course.name}_copy'
            site.courses.append(new_course)
            new_course.mark_new()
            commit()
            # Привязка наблюдателей к курсу
            new_course.attach(sms_notifier)
            new_course.attach(email_notifier)

        return OK_200, render('courses.html', context=context)
    # Если запрос некорректный (поправлен ручонками) - переводим на страницу со списком курсов
    return NOT_FOUND_404, render('courses.html', context=context)


@app.route('/student/')
class StudentsListView(ListView):
    title = 'Список студентов'
    template = 'students.html'
    # queryset = site.students
    object_name_context = 'students_list'
 # todo: добавить фильтрацию студентов по курсам

    def get_queryset(self):
        mapper = MapperRegistry.get_curr_mapper('students')
        return mapper.all()

# def students_view(request):
#     q_params = request['query_params']
#     if q_params.get('course'):
#         students = site.get_students_by_course(q_params['course'])
#     else:
#         students = site.students
#     context = {
#         'title': 'Список студентов',
#         '_copyright': request.get('copyright'),
#         'students_list': students,
#     }
#     return OK_200, render('students.html', context=context)


@debug
@app.route('/student/create/')
class StudentCreateView(CreateView):
    title = 'Заведение студента'
    template = 'create_student.html'

    def create_object(self, data):
        name = data['name']
        new_student = site.create_user('student', name)
        site.students.append(new_student)
        new_student.mark_new()
        commit()


# @app.route('/student/create/')
# def create_student_view(request):
#     context = {
#         'title': 'Заведение студента',
#         '_copyright': request.get('copyright'),
#     }
#     if request['method'] == 'POST':
#         data = request['data']
#         log(f'Полученные данные на создание студента:\n{data}')
#         new_student = site.create_user('student', data['name'])
#         site.students.append(new_student)
#         context['title'] = 'Список студентов'
#         context['students_list'] = site.students
#         return CREATED_201, render('students.html', context=context)
#
#     return OK_200, render('create_student.html', context=context)

@app.route('/student/course/add/')
class AddStudentToCourseCreateView(CreateView):  # todo: перенести функционал по добавлению юзера из урла к курсу
    title = 'Добавление студента к курсу'
    template = 'add_student.html'
    student_mapper = MapperRegistry.get_curr_mapper('students')
    courses_mapper = MapperRegistry.get_curr_mapper('courses')
    # extra_context = {
    #     'students_list': site.students,
    #     'courses_list': site.courses,
    # }

    def get_context_data(self):
        context = super().get_context_data()
        context['students_list'] = self.student_mapper.all()
        context['courses_list'] = self.courses_mapper.all()
        return context

    def create_object(self, data):
        course_id = data['course_id']
        student_id = data['student_id']
        course = self.courses_mapper.get_by_id(course_id)
        student = self.student_mapper.get_by_id(student_id)
        course_student = course.add_student(student)
        course_student.mark_new()
        commit()


# @app.route('/student/course/add/')
# def add_student_to_course(request):
#     context = {
#         'title': 'Добавление студента к курсу',
#         '_copyright': request.get('copyright'),
#     }
#     if request['method'] == 'POST':
#         data = request['data']
#         log(f'Полученные данные на добавление студента к курсу:\n{data}')
#         course = site.get_course_by_name(data['course_name'])
#         student = site.get_student_by_name(data['student_name'])
#         course.add_student(student)
#         context['title'] = 'Список студентов'
#         context['students_list'] = site.students
#         return CREATED_201, render('students.html', context=context)
#
#     q_params = request['query_params']
#     student_name = q_params.get('student')
#     if student_name:
#         context['student'] = student_name
#     else:
#         context['students_list'] = site.students
#     context['courses_list'] = site.courses
#     return OK_200, render('add_student.html', context=context)


@app.route('/course/api/')
def course_api(request):
    res_dict = {}
    if site.courses:
        id_c = 0
        for course in site.courses:
            students = []
            for student in course:
                students.append(student.name)
            course_dict = {
                'name': course.name,
                'category': course.category.name,
                'students': students,
            }
            res_dict[id_c] = course_dict
            id_c += 1
    else:
        res_dict['error_text'] = 'there are no courses yet'
    res = BaseSerializer(res_dict).save()
    log(f'Вызван api курсов - {res}')
    return OK_200, res
