from api_test.celery import app
from .utils import HackerNewsParser


@app.task
def parse_task():
    parser = HackerNewsParser()
    parser.parse()
    return 'done'