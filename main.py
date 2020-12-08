from controllers import *
from core.app import Application
from views import *

routers = {
    '/': index_view,
    '/index/': index_view,
    '/about/': about_view,
}

controllers = {
    add_copyright_controller,
}

application = Application(routers, controllers)
