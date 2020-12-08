from core.templator import render
from include.codes import OK_200


def index_view(request):
    # context = {
    #     'title': 'Главная'
    # }
    title = 'Главная'
    _copyright = request.get('copyright')
    return OK_200, render('index.html',
                          title=title,
                          _copyright=_copyright)


def about_view(request):
    # context = {
    #     'title': 'О проекте'
    # }
    title = 'О проекте'
    _copyright = request.get('copyright')
    return OK_200, render('about.html',
                          title=title,
                          _copyright=_copyright)