from os.path import exists
from os import mkdir
from click import command, option
from printer import printer

from export import ExportData


def check_dir(path: str):
    if not exists(path):
        mkdir(path)


@command('export')
@option('--csv', 'csv', is_flag=True, help="Cria um arquivo no formato CSV.")
@option('--json', 'json', is_flag=True, help="Cria um arquivo no formato JSON.")
@option('--interval', 'interval', type=int, default=2, show_default=True,
        help="O tempo do intervalo em minutos que será considerado na Query.")
@option('--path', 'file_path', type=str, help="Caminho onde o(s) arquivo(s) serão salvos, caso não exista, "
                                              "ele será criado.")
def export(csv, json, interval, file_path):
    if not csv and not json:
        printer(message=f'É preciso selecionar ao menos um tipo de saída!\nExemplo: export --csv --interval=2 '
                        f'--path=/home/usuario/exports', status='info')
        return

    check_dir(file_path)

    try:
        ExportData(csv=csv, json=json, interval=None, file_path=file_path).save()

        printer(message='Dados exportados com sucesso!', status='success')

    except Exception as ex:
        printer(message=f'[EXPORT ERROR]: {ex}', status='error')


if __name__ == '__main__':
    export()
