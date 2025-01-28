import time
import redis
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Replace with your project settings module
django.setup()

from main.models import GamesModel
from main.display_players import players

r = redis.Redis(host='localhost', port=6379,  password='mysecret24')

def generate_weekly_report():
    leaders=players(GamesModel, r)
    print(leaders)
    r.hmset("weekly_report", leaders)
    print(f"Task executed at {time.ctime()}")


if __name__=='__main__':
    generate_weekly_report()