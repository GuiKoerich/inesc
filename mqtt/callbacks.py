from datetime import datetime
from db import Mongo
from .topics import topics, topics_collections

__all__ = ['on_message', 'on_connect', 'on_disconnect']

colors = {
    'default': '\033[0m',
    'success': '\033[92m',
    'error': '\033[91m',
    'info': '\033[95m'
}

db = Mongo()


def on_connect(client, userdata, flags, rc):
    if rc.__eq__(0):
        printer(message='[MQTT CONNECTED] MQTT Broker connected with success!', status='success')
        printer(message='[MQTT] Initialize subscribe topics...', status='info')

        subscribe(client)

        printer(message='[MQTT] Listening broker...', status='info')

    else:
        printer(message=f"[MQTT ERROR] MQTT Broker couldn't connect!", status='error')


def on_message(client, userdata, message):
    payload = {'timestamp': str(datetime.now()), message.topic: message_decoded(message.payload)}
    print(message.payload)
    print(payload)

    error = db.insert(collection=collection_by_topic(message.topic), payload=payload)
    # error = None
    if error:
        printer(message=f'[DB ERROR] Error on save in collection: {collection_by_topic(message.topic)} | '
                        f'payload: {payload} | cause: {error.get("message")}', status=error.get('status'))


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
    key = topic.replace('topic_', '').split('/')[0]

    return topics_collections.get(key)


def message_decoded(payload):
    message = str(payload.decode('utf-8'))

    if message.__eq__('false'):
        return 0

    elif message.__eq__('true'):
        return 1

    return message


def printer(message, status):
    print(f'{colors.get(status)}{message}{colors.get("default")}')
