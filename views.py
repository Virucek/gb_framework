import os
from datetime import datetime

from core.templator import render
from include.codes import *
from logger import Logger
from models import MainInterface

site = MainInterface()
logger = Logger('site')
log = logger.log
debug = logger.debug


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


#@debug
def about_view(request):
    title = 'О проекте'
    _copyright = request.get('copyright')
    context = {
        'title': title,
        '_copyright': _copyright,
    }
    return OK_200, render('about.html',
                          context=context)


#@debug
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


#@debug
def categories_view(request):
    print(site.categories)
    context = {
        'title': 'Категории',
        '_copyright': request.get('copyright'),
        'categories_list': site.get_category_tree(),
    }
    return OK_200, render('categories.html', context=context)


#@debug
def create_category_view(request):
    context = {
        'title': 'Создание категории',
        '_copyright': request.get('copyright'),
        'categories_list': site.categories,
    }

    if request['method'] == 'POST':
        data = request['data']
        log(f'Полученные данные в запросе: \n {data}')
        parent_category = None
        category_id = data.get('category_id')
        if category_id:
            parent_category = site.get_category_by_id(int(category_id))
        category = site.create_category(data['cat_name'], parent_category)
        site.categories.append(category)
        context['title'] = 'Категории'
        context['categories_list'] = site.get_category_tree()
        return CREATED_201, render('categories.html', context=context)

    return OK_200, render('create_category.html', context=context)


#@debug
def courses_view(request):
    q_params = request['query_params']
    if q_params.get('category_id'):
        courses = site.get_courses_by_category(q_params['category_id'])
    else:
        courses = site.courses
    context = {
        'text': 'Список курсов',
        '_copyright': request.get('copyright'),
        'courses_list': courses,
    }

    return OK_200, render('courses.html', context=context)


#@debug
def create_course_view(request):
    context = {
        'title': 'Создание курса',
        '_copyright': request.get('copyright'),
    }

    if request['method'] == 'POST':
        data = request['data']
        log(f'Полученные данные в запросе: \n {data}')
        category = site.get_category_by_id(int(data['category_id']))
        new_course = site.create_course(data['course_type'], data['course_name'], category)
        site.courses.append(new_course)
        context['title'] = 'Список курсов'
        context['courses_list'] = site.courses
        return CREATED_201, render('courses.html', context=context)

    context['categories_list'] = site.categories
    context['course_types'] = site.get_course_types()
    return OK_200, render('create_course.html', context=context)


#@debug
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

        return OK_200, render('courses.html', context=context)
    # Если запрос некорректный (поправлен ручонками) - переводим на страницу со списком курсов
    return NOT_FOUND_404, render('courses.html', context=context)
