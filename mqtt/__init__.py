from time import sleep
from paho.mqtt.client import Client
from .callbacks import *
from printer import printer


def define_callbacks(cli: Client) -> None:
    cli.on_connect = on_connect
    cli.on_disconnect = on_disconnect
    cli.on_message = on_message


def client() -> Client:
    cli = Client(client_id='INESC-API', transport='tcp')

    define_callbacks(cli)

    cli.connect(host='inescfloripa.computacaosc.com.br', keepalive=10)

    return cli


def serve():
    try:
        client().loop_forever()

    except Exception as ex:
        printer(message=f'[SCRIPT ERROR] {ex}', status='error')
        sleep(5)
        serve()


def run():
    serve()
