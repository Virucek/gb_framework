from core.app import Application


class DebugApplication(Application):
    def __init__(self, routers, controllers):
        self.application = Application(routers, controllers)
        super().__init__(routers, controllers)

    def __call__(self, env, start_response):
        print('DEBUG')
        print(env)
        return self.application(env, start_response)
