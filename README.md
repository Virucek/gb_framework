# gb_framework
GeekBrains framework for Patterns course

#### Start commands
**start app** _uwsgi --http :9050 --wsgi-file main.py_

**start fake app** _uwsgi --http :9050 --wsgi-file main.py --pyargv "fake"_

**start app in debug mode** _uwsgi --http :9050 --wsgi-file main.py --pyargv "debug"_