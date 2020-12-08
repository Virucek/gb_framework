import sys

from include.codes import *

sys.path.append('../')


class Application:

    def __init__(self, routers, controllers):
        self.routers = routers
        self.controllers = controllers

    def __call__(self, env, start_response):
        uri = self.check_uri(env['REQUEST_URI'])
        if uri in self.routers:
            view = self.routers[uri]
            request = {}
            for controller in self.controllers:
                controller(request)
            code, response_body = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [response_body.encode('utf-8')]
        else:
            start_response(NOT_FOUND_404, [('Content-Type', 'text/html')])
            return [b"Page not found"]

    @staticmethod
    def check_uri(uri):
        if not uri[-1] == '/':
            uri += '/'
        return uri
