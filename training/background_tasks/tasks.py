import time
from rq import get_current_job
from training.app import app
from training.extensions import mail


def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')


def send_email_function(msg):
    with app.app_context():
        mail.send(msg)
