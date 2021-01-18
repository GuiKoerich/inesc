from db import Mongo
from export.export_csv import ExportCSV
from export.export_json import ExportJSON


class ExportData:
    __slots__ = ['__csv', '__json', '__interval', '__file_path', '__data']

    __db = Mongo()

    def __init__(self, csv, json, interval, file_path):
        self.__csv = csv
        self.__json = json
        self.__interval = interval
        self.__file_path = file_path

    def save(self):
        self.__prepare()

        if self.__csv:
            ExportCSV().create(self.__data, self.__file_path)

        if self.__json:
            ExportJSON().create(self.__data, self.__file_path)

    def __prepare(self):
        self.__data = self.__db.select_all(self.__interval)
