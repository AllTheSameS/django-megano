import random
import datetime


def timing():
        current_datetime = datetime.datetime.now()
        return current_datetime + datetime.timedelta(days=random.randint(1, 30))