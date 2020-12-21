from controllers import *
from core.app import Application
from views import *

routers = {
    '/': index_view,
    '/index/': index_view,
    '/about/': about_view,
    '/contacts/': contacts_view,
    # Категории
    '/category/': categories_view,
    '/category/create/': create_category_view,
    # Курсы
    '/course/': courses_view,
    '/course/create/': create_course_view,
    '/course/copy/': copy_course_view,
}

controllers = {
    add_copyright_controller,
}

application = Application(routers, controllers)
