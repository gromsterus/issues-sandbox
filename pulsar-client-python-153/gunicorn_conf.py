from case_gunicorn import get_pulsar, close_pulsar


bind = '0.0.0.0:8000'
max_requests = 1
workers = 2
errorlog = '-'
accesslog = '-'


def post_worker_init(_):
    get_pulsar()


def worker_int(_):
    close_pulsar()


def worker_abort(_):
    close_pulsar()
