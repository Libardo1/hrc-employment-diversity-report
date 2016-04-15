import requests
import time
from celery import Celery
import rethinkdb as r
from ntp.data import main

APP = Celery("ntp.data.tasks")
APP.config_from_object("ntp.data.celeryconfig")

@APP.task
def check_and_fetch():
    """
    Check for an update to the HR data on the open data portal.  If one exists do.
    """
    main.run()
    
@APP.task
def test_task(a):
    """
    Stupid task for testing purposes
    """
    return a + 1

