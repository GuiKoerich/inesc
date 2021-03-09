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
@option('--collection', 'collection', type=str, help="Collection específica do MongoDB a ser exportada. "
                                                     "Para buscar todas não utilize esta opção")
@option('--interval', 'interval', type=int, default=2, show_default=True,
        help="O tempo do intervalo em minutos que será considerado na Query. O todos os registros")
@option('--path', 'file_path', type=str, help="Caminho onde o(s) arquivo(s) serão salvos, caso não exista, "
                                              "ele será criado.")
@option('--between', 'between', type=str, help="Data de início e final da busca. "
                                               "Exemplo: 2021-08-03-00:00:00 2021-08-03-23:59:59")
def export(csv, json, collection, interval, file_path, between):
    if not csv and not json:
        printer(message=f'É preciso selecionar ao menos um tipo de saída!\nExemplo: export --csv --interval=2 '
                        f'--path=/home/usuario/exports\nUse o --help para auxiliar!\npython3 export.py --help',
                status='info')
        return

    if between:
        interval = None

    check_dir(file_path)

    try:
        ExportData(csv=csv, json=json, collection=collection, interval=interval, file_path=file_path,
                   between=between).save()

        printer(message='Dados exportados com sucesso!', status='success')

    except Exception as ex:
        printer(message=f'[EXPORT ERROR]: {ex}', status='error')


if __name__ == '__main__':
    export()
