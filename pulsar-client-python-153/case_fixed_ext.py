import uwsgidecorators
from flask import Flask, make_response
from pulsar import Client, Producer, schema


class PulsarExt:
    def __init__(self, url: str) -> None:
        self._url = url
        self._connected = False
        self._client: Client | None = None
        self._producer: Producer | None = None

    def init_app(self, app_: Flask) -> None:
        app_.extensions['pulsar'] = self

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def client(self) -> Client:
        assert self._connected, 'Call `connect()` first'
        return self._client

    @property
    def producer(self) -> Producer:
        assert self._connected, 'Call `connect()` first'
        return self._producer

    def connect(self) -> None:
        self._client = Client(self._url)
        self._producer = self._client.create_producer(
            'non-persistent://public/default/issue-153',
            schema=schema.StringSchema(),
        )
        self._connected = True

    def close(self) -> None:
        if self._producer:
            self._producer.close()
        if self._client:
            self._client.close()

        self._producer = None
        self._client = None
        self._connected = False


app = Flask(__name__)
pulsar_ext = PulsarExt('pulsar://pulsar:6650')
pulsar_ext.init_app(app)


@uwsgidecorators.postfork
def _init_app() -> None:
    pulsar_ext.connect()


@app.get('/health')
def health():
    pulsar_ext.producer.send('1')
    return make_response({})
