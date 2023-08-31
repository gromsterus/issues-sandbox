import logging
import uuid
from datetime import datetime
from typing import Optional

from _pulsar import Result
from flask import Flask, make_response
from pulsar import Client, MessageId, Producer, schema


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)
pulsar_logger = logging.getLogger('pulsar')


class PulsarExt:
    def __init__(self, url: str) -> None:
        self._url = url
        self._client: Optional[Client] = None
        self._g_producer: Optional[Producer] = None

    def init_app(self, app_: Flask) -> None:
        app_.extensions['pulsar'] = self

    @property
    def client(self) -> Client:
        assert self._client is not None, 'Call `connect()` first'
        return self._client

    @property
    def g_producer(self) -> Producer:
        assert self._g_producer is not None, 'Call `connect()` first'
        return self._g_producer

    def connect(self) -> None:
        self._client = Client(self._url, authentication=None, logger=pulsar_logger)
        self._g_producer = self._client.create_producer(
            'non-persistent://public/default/test-gunicorn',
            producer_name=f'my-producer-{uuid.uuid4()}',
            schema=schema.StringSchema(),
        )

    def close(self) -> None:
        if self._g_producer:
            self._g_producer.close()
        if self._client:
            self._client.close()

        self._g_producer = None
        self._client = None


app = Flask(__name__)
pulsar_ext = PulsarExt('pulsar://pulsar:6650')
pulsar_ext.init_app(app)


def init_app() -> None:
    pulsar_ext.connect()


def teardown_app() -> None:
    pulsar_ext.close()


@app.post('/post-message')
def post_pulsar_message():
    logger.info(
        'Calling producer.send_async now, '
        'in the next lines there should be the callback result'
    )
    dt = datetime.now()
    pulsar_ext.g_producer.send_async(content=f'dt={dt.isoformat()}', callback=callback)
    logger.info('After producer.send_async, returning the http response')
    return '', 201


def callback(res: Result, _msg_id: MessageId):
    logger.info(f'Callback result here! Event acknowledged by the broker.')


@app.get('/')
def healthcheck():
    logger.info('API Running fine')
    return make_response({'status': 'healthy'})
