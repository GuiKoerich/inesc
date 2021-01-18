from datetime import datetime
from json import dumps


class ExportJSON:
    __slots__ = ['__filename', '__data', '__full_path']

    __default_keys = ['_id', 'timestamp']

    def __init__(self):
        self.__filename = f'inesc_export_{datetime.now()}.json'

    def __prepare(self, data, file_path):
        self.__full_path = f'{file_path}/{self.__filename}'
        self.__data = data

    def create(self, data, file_path):
        self.__prepare(data, file_path)
        self.__create_custom_json()

        self.__save_file()

    def __create_custom_json(self):
        for key in self.__data.keys():
            for data in self.__data.get(key):

                topic_key = ''
                for key_data in data.keys():
                    if not self.__default_keys.__contains__(key_data):
                        topic_key = key_data
                    else:
                        data.update({key_data: str(data.get(key_data))})

                data.update({'topic': topic_key, 'value': data.get(topic_key)})
                data.pop(topic_key)

    def __save_file(self):
        with open(self.__full_path, 'w') as json_file:
            json_file.write(dumps(self.__data, indent=4))
