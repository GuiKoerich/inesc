from paho.mqtt.client import Client
from .callbacks import *


# host = 'inescfloripa.computacaosc.com.br'
host = '127.0.0.1'


def define_callbacks(cli: Client) -> None:
    cli.on_connect = on_connect
    cli.on_disconnect = on_disconnect
    cli.on_message = on_message


def client() -> Client:
    cli = Client(client_id='INESC-API', transport='tcp')

    define_callbacks(cli)

    cli.connect(host=host, keepalive=10)

    return cli


def run():
    client().loop_forever(retry_first_connection=True)
