from pathlib import Path

from celery import Celery


_root = Path(__file__).parent.resolve().parent
_celery_data = _root.joinpath("celery_data")
_celery_q_in = _celery_data.joinpath("in")
_celery_processed = _celery_data.joinpath("processed")

for _p in (_celery_data, _celery_q_in, _celery_processed):
    _p.mkdir(exist_ok=True)

app = Celery("app")
celery_conf = {
    "broker_url": "filesystem://",
    "broker_transport_options": {
        "data_folder_in": _celery_q_in,
        "data_folder_out": _celery_q_in,
        "processed_folder": _celery_processed,
    },
}

app.config_from_object(celery_conf)
app.autodiscover_tasks(["case"])
