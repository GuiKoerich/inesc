from datetime import datetime
from db import Mongo
from .topics import topics, topics_collections, topic_by_values
from printer import printer


__all__ = ['on_message', 'on_connect', 'on_disconnect', 'get_topic_by_value', 'insert', 'define_topic']

db = Mongo()

error_topic = 'erro'


def on_connect(client, userdata, flags, rc):
    if rc.__eq__(0):
        printer(message='[MQTT CONNECTED] MQTT Broker connected with success!', status='success')
        printer(message='[MQTT] Initialize subscribe topics...', status='info')

        subscribe(client)

        printer(message='[MQTT] Listening broker...', status='info')

    else:
        printer(message=f"[MQTT ERROR] MQTT Broker couldn't connect!", status='error')


def on_message(client, userdata, message):
    payload = {'timestamp': str(datetime.now()), define_topic(message.topic): message_decoded(message.payload)}
    # print(message.payload)
    # print(payload)

    insert(topic=message.topic, payload=payload)


def on_disconnect(client, userdata, rc):
    if not rc.__eq__(0):
        printer(message=f'[MQTT] Unexpected disconnection from broker!', status='error')
        printer(message=f'[MQTT] Trying reconnect...', status='info')
        client.reconnect()


def subscribe(cli):
    len_topics = len(topics)

    for topic in topics:
        result, qos = cli.subscribe(topic)

        if result.__eq__(0):
            message = f' >>> [SUBSCRIBE] {topic} subscribed with success! [{qos}/{len_topics}]'
            status = 'success'

        else:
            message = f" >>> [SUBSCRIBE] {topic} couldn't subscribed [{qos}/{len_topics}]"
            status = 'error'

        printer(message, status)


def collection_by_topic(topic: str) -> str:
    key = split_topic(topic)[0]

    return topics_collections.get(key)


def split_topic(topic: str) -> list:
    return topic.replace('topic_', '').split('/')


def define_topic(topic: str) -> str:
    split = split_topic(topic)

    return compose_topic(topic_splited=split, is_error=split.__contains__(error_topic))


def compose_topic(topic_splited: list, is_error: bool) -> str:
    if not is_error:
        return f"{topic_splited[-1]}"

    return "_".join(topic_splited[topic_splited.index(error_topic) + 1:])


def message_decoded(payload):
    message = str(payload.decode('utf-8'))

    if message.__eq__('false'):
        return 0

    elif message.__eq__('true'):
        return 1

    return message


def insert(topic, payload):
    error = db.insert(collection=collection_by_topic(topic), payload=payload)

    if error:
        printer(message=f'[DB ERROR] Error on save in collection: {collection_by_topic(topic)} | '
                        f'payload: {payload} | cause: {error.get("message")}', status=error.get('status'))


def get_topic_by_value(value, concat=True):
    for key in topic_by_values.keys():
        if topic_by_values.get(key).__contains__(value):
            if concat:
                return f'{key}{value}'

            else:
                return key
