from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')
app.conf.broker_url = 'redis://localhost:6379/0'


@app.task
def add(x, y):
    return x + y


@app.task
def hello():
    return 'hello world'
