import os
from datetime import datetime

from core.templator import render
from include.codes import OK_200
from logger import Logger
from models import MainInterface

site = MainInterface()
logger = Logger('site')
log = logger.log


def index_view(request):
    title = 'Главная'
    _copyright = request.get('copyright')
    context = {
        'title': title,
        '_copyright': _copyright
    }
    return OK_200, render('index.html',
                          context=context)


def about_view(request):
    title = 'О проекте'
    _copyright = request.get('copyright')
    context = {
        'title': title,
        '_copyright': _copyright,
    }
    return OK_200, render('about.html',
                          context=context)


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


def categories_view(request):
    context = {
        'title': 'Категории',
        '_copyright': request.get('copyright'),
        'categories': site.categories,
    }
    return OK_200, render('categories.html', context=context)


def create_category_view(request):
    context = {
        'title': 'Создание категории',
        '_copyright': request.get('copyright'),
    }

    if request['method'] == 'POST':
        data = request['data']
        log(f'Полученные данные в запросе: \n {data}')
        category = site.create_category(data['cat_name'])
        site.categories.append(category)
        context['title'] = 'Категории'
        return OK_200, render('categories.html', context=context)

    return OK_200, render('create_category.html', context=context)
