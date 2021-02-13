from os.path import isfile
from click import command, option, Path, argument
from printer import printer

from import_file import ImportData


def check_file_path(paths: list):
    for path in paths:
        if not isfile(path):
            raise FileNotFoundError(f'O {path} não é um arquivo.')


@command('import_file', context_settings={"ignore_unknown_options": True})
@argument('files_path', nargs=-1, type=Path())
def import_file(files_path):
    if not files_path:
        printer(message=f'É preciso informar o caminho do(s) arquivo(s) para importar!\n'
                        f'Exemplo: \033[1mpython3 import.py --path=/home/user/file.csv ou '
                        f'\033[1mpython3 import.py --path=/home/user/file.csv /home/user/file1.csv /home/user/fileN.csv'
                , status='info')
        return

    try:
        check_file_path(files_path)

        for path in files_path:
            ImportData(file_path=path).save()

        printer(message='Dados sincronizados com sucesso!', status='success')

    except Exception as ex:
        printer(message=f'[IMPORT ERROR]: {ex}', status='error')
        raise ex


if __name__ == '__main__':
    import_file()
