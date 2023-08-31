import logging
import uuid
from datetime import datetime

from _pulsar import Result
from flask import Flask, make_response
from pulsar import Client, MessageId, schema

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)
logger.info('Loading API')

app = Flask(__name__)

client = Client('pulsar://pulsar:6650', authentication=None)

producer = client.create_producer(
    'non-persistent://public/default/test-gunicorn',
    producer_name=f'my-producer-{uuid.uuid4()}',
    schema=schema.StringSchema(),
)


def callback(res: Result, _msg_id: MessageId):
    logger.info(f'Callback result here! Event acknowledged by the broker.')


@app.post('/post-message')
def post_pulsar_message():
    logger.info(
        'Calling producer.send_async now, '
        'in the next lines there should be the callback result'
    )
    dt = datetime.now()
    producer.send_async(content=f'dt={dt.isoformat()}', callback=callback)
    logger.info('After producer.send_async, returning the http response')
    return '', 201


@app.get('/')
def healthcheck():
    logger.info('API Running fine')
    return make_response({'status': 'healthy'})


logger.info('API started')
