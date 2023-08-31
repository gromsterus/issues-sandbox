import time
import random
import string

from pulsar import Client, CompressionType
from pulsar.schema import AvroSchema, Record, String, Integer


def generate_random_string(length=6):
    charset = string.ascii_letters + string.digits
    random_chars = random.choices(charset, k=length)
    random_string = "".join(random_chars)
    return random_string.capitalize()


class User(Record):
    name = String()
    age = Integer


UserAvroSchema = AvroSchema(User)  # type: ignore


def gen_random_data():
    return User(user=generate_random_string(), age=random.randint(0, 100))


class PulsarDemo(object):
    def __init__(self) -> None:
        self.SERVICE_URL = "pulsar://pulsar:6650"
        self.TOPIC = "persistent://public/default/test-celery"
        client = Client(service_url=self.SERVICE_URL)
        self.producer = client.create_producer(
            topic=self.TOPIC,
            schema=UserAvroSchema,
            batching_enabled=True,
            batching_max_messages=1000,
            batching_max_publish_delay_ms=1000,
            compression_type=CompressionType.SNAPPY,  # type: ignore
        )

    def send_callback(self, send_result, msg_id):
        print("Message published: result:{}  msg_id:{}".format(send_result, msg_id))

    def async_producer(self, cnt=1000):
        while cnt >= 0:
            data = gen_random_data()
            self.producer.send_async(
                data,
                callback=self.send_callback,
            )
            time.sleep(0.01)
            cnt -= 1
        self.producer.flush()


# celery task
from celery import shared_task


@shared_task
def mock_data2pulsar(cnt=1000):
    mock = PulsarDemo()
    mock.async_producer(cnt)
