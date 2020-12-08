
import datetime


# Заменить на подшаблон потом ?
def add_copyright_controller(request):
    request['copyright'] = f'Aikin Yakov &copy; {datetime.datetime.now().year} Все права защищены'
