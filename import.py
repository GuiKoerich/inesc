from os.path import isfile
from click import command, option
from printer import printer

from import_file import ImportData


def check_file_path(path: str):
    if not isfile(path):
        raise FileNotFoundError(f'O {path} não é um arquivo.')


@command('import_file')
@option('--path', 'file_path', type=str, help="Caminho do arquivo que deseja importar.")
def import_file(file_path):
    if not file_path:
        printer(message=f'É preciso informar o caminho do arquivo para importar!\n'
                        f'Exemplo: python3 import.py --path=/home/usuario/file.csv', status='info')
        return

    try:
        check_file_path(file_path)

        ImportData(file_path=file_path).save()

        printer(message='Dados sincronizados com sucesso!', status='success')

    except Exception as ex:
        printer(message=f'[IMPORT ERROR]: {ex}', status='error')
        raise ex


if __name__ == '__main__':
    import_file()
