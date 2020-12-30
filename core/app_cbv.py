from core.templator import render
from include.codes import OK_200


class TemplateView:
    model = None
    template = None
    title = None
    extra_context = {}

    def get_context_data(self):
        context = {}
        title = self.get_title()
        if title:
            context['title'] = title
        extra_context = self.get_extra_context()
        if extra_context:
            context.update(extra_context)
        return context

    def get_template(self):
        return self.template

    def get_extra_context(self) -> dict:
        return self.extra_context

    def get_title(self):
        return self.title

    def render_with_context(self):
        template = self.get_template()
        context = self.get_context_data()
        return OK_200, render(template, context=context)

    def __call__(self, request):
        return self.render_with_context()


class ListView(TemplateView):
    queryset = None
    object_name_context = 'objects_list'

    def get_queryset(self):
        print('tttt', self.queryset)
        if self.queryset is not None:
            return self.queryset
        else:
            raise Exception('Queryset for List view not defined')

    def get_object_name_context(self):
        print('object', self.object_name_context)
        return self.object_name_context

    def get_context_data(self):
        context = {}
        queryset = self.get_queryset()
        print('queryset', queryset)
        object_name_context = self.get_object_name_context()
        context[object_name_context] = queryset
        context.update(super().get_context_data())
        return context


class CreateView(TemplateView):

    def get_request_data(self, request):
        return request['data']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            # todo: добавить редирект
            return self.render_with_context()
        else:
            return super().__call__(request)
