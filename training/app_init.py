import os
from redis import Redis
import rq

from training.app import app, db
import training.controllers


REDIS_URL = os.environ.get('REDIS_URL')
app.redis = Redis.from_url(REDIS_URL)
app.task_queue = rq.Queue('my-app-tasks', connection=app.redis)


def init_db():
    db.create_all()
    db.session.commit()


def main():
    init_db()
    app.run(port=8000)


if __name__ == '__main__':
    main()

