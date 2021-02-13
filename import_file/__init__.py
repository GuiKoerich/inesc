from .import_csv import ImportCSV
from .import_json import ImportJSON


class ImportData:
    __slots__ = ['__file_path', '__csv', '__json']

    __LAST_INDEX = -1

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__csv = False
        self.__json = False

        self.__file_format()

    def save(self):
        if self.__csv:
            ImportCSV(file_path=self.__file_path).sync()

        if self.__json:
            ImportJSON(file_path=self.__file_path).sync()

    def __file_format(self):
        _format = self.__file_path.split('.')[self.__LAST_INDEX]

        if _format.__eq__('csv'):
            self.__csv = True

        if _format.__eq__('json'):
            self.__json = True
