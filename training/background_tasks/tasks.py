import time
from rq import get_current_job
from training.app import app, mail


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


def send_email_async(msg):
    job = app.task_queue.enqueue(send_email_function, msg)
    job.get_id()
