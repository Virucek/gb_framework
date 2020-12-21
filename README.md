# gb_framework
GeekBrains framework for Patterns course

#### Start commands
_uwsgi --http :9050 --wsgi-file main.py_  *start app*

_uwsgi --http :9050 --wsgi-file main.py --pyargv "fake"_ *start fake app*

_uwsgi --http :9050 --wsgi-file main.py --pyargv "debug"_ *start app in debug mode*