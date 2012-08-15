# -*- coding: utf-8 -*-
import os
import signal

import crane_ec2

from mysqlapi.api import creator
from mysqlapi.api.models import DatabaseManager, Instance

os.environ["DJANGO_SETTINGS_MODULE"] = "mysqlapi.settings"


def huphandler(signum, frame):
    creator.reset_queue()


def termhandler(signum, frame):
    creator.close_queue()


def start():
    client = crane_ec2.Client()
    signal.signal(signal.SIGHUP, huphandler)
    signal.signal(signal.SIGTERM, termhandler)
    creator.set_model(Instance)
    creator.build_queue()
    creator.start_creator(DatabaseManager, client)

start()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
