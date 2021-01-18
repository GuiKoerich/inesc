from datetime import datetime, timedelta
from pymongo import MongoClient


class Mongo:
    __slots__ = ['__client', '__db']

    __host = 'inescfloripa.computacaosc.com.br'
    __port = 443

    __db_name = 'IND4Fibre_2'

    def __connection(self):
        self.__connect()
        self.__get_db()

    def __close_connection(self):
        self.__client.close()

    def __connect(self):
        self.__client = MongoClient(host=self.__host, port=self.__port)

    def __get_db(self):
        self.__db = self.__client[self.__db_name]

    def insert(self, collection, payload):
        try:
            self.__connection()
            self.__db[collection].insert_one(payload)

            return None

        except Exception as ex:
            return {'message': ex, 'status': 'error'}

        finally:
            self.__client.close()

    def select_all(self, interval=None):
        try:
            self.__connection()
            result = {}
            options = None

            if interval:
                start = datetime.now() - timedelta(minutes=interval)
                options = {'timestamp': {'$gt': str(start)}}

            for data_collection in self.__db.list_collections():
                collection = data_collection.get('name')
                result.update({
                    collection: [data for data in self.__db[collection].find(options)]
                })

            return result

        except Exception as ex:
            return {'message': ex, 'status': 'error'}

        finally:
            self.__client.close()
