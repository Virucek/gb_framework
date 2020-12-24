from core.app import Application
from include.codes import OK_200


class FakeApplication(Application):
    def __init__(self, routers, controllers):
        self.application = Application(routers, controllers)
        super().__init__(routers, controllers)

    def __call__(self, env, start_response):
        start_response(OK_200, [('Content-Type', 'text/html')])
        return [b"Hello from Fake"]
