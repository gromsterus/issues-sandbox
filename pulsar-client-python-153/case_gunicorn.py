import dataclasses
from typing import TypedDict

from flask import Flask, make_response
from pulsar import Client, Producer, schema


app = Flask(__name__)


@dataclasses.dataclass(frozen=True)
class Pulsar:
    client: Client
    producer: Producer


class State(TypedDict):
    pulsar: Pulsar | None


_state: State = {'pulsar': None}


def get_pulsar() -> Pulsar:
    p = _state['pulsar']
    if p is None:
        client = Client('pulsar://pulsar:6650')
        producer = client.create_producer(
            'non-persistent://public/default/issue-153',
            schema=schema.StringSchema(),
        )
        p = _state['pulsar'] = Pulsar(client=client, producer=producer)
    return p


def close_pulsar() -> None:
    p = _state['pulsar']
    if p is not None:
        p.producer.close()
        p.client.close()
        _state['pulsar'] = None


@app.get('/health')
def health():
    get_pulsar().producer.send('1')
    return make_response({})
