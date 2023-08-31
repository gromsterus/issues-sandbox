from case_fixed import init_app, teardown_app


def post_worker_init(worker):
    init_app()


def worker_int(worker):
    teardown_app()


def worker_abort(worker):
    teardown_app()
