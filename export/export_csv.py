from datetime import date
from xlsxwriter import Workbook


class ExportCSV:
    __slots__ = ['__workbook', '__row', '__col', '__worksheet', '__output', '__filename', '__data']

    __fields = ['ID', 'TIMESTAMP', 'TOPIC', 'VALUE']
    __default_options = {'constant_memory': True, 'default_date_format': 'dd/mm/yyyy hh:mm:ss'}
    __default_keys = ['_id', 'timestamp']

    def __init__(self):
        self.__filename = f'inesc_export_{date.now()}.csv'

        self.__clear_cols_and_rows()

    def __clear_cols_and_rows(self):
        self.__row = 0
        self.__col = 0

    def __clear(self, col=False, row=False, both=False):
        if col:
            self.__col = 0

        if row:
            self.__row = 0

        if both:
            self.__clear_cols_and_rows()

    def __increment(self,  col=False, row=False):
        if col:
            self.__col += 1

        if row:
            self.__row += 1

    def __prepare(self, data, file_path):
        self.__workbook = Workbook(f'{file_path}/{self.__filename}', self.__default_options)
        self.__data = data

    def create(self, data, file_path):
        self.__prepare(data, file_path)
        self.__create()

        self.__workbook.close()

    def __create(self):
        for key in self.__data.keys():
            data_list = self.__data.get(key)

            if data_list:
                self.__create_worksheet(name=key)
                self.__write_lines(data_list=data_list)

            self.__clear_cols_and_rows()

    def __create_worksheet(self, name):
        self.__worksheet = self.__workbook.add_worksheet(name=name)

        for field in self.__fields:
            self.__worksheet.write(self.__row, self.__col, field)
            self.__increment(col=True)

        self.__increment(row=True)
        self.__clear(col=True)

    def __write_lines(self, data_list):
        for data in data_list:
            for key in data.keys():
                if self.__default_keys.__contains__(key):
                    self.__worksheet.write(self.__row, self.__col, str(data.get(key)))
                    self.__increment(col=True)

                else:
                    self.__worksheet.write(self.__row, self.__col, key)
                    self.__increment(col=True)
                    self.__worksheet.write(self.__row, self.__col, data.get(key))

            self.__clear(col=True)
            self.__increment(row=True)
