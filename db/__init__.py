from datetime import datetime, timedelta
from pymongo import MongoClient


class Mongo:
    __slots__ = ['__client', '__db', '__bulk']

    # __host = 'inescfloripa.computacaosc.com.br'
    __host = '192.168.0.20'
    # __port = 443
    __port = 27017

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

    def bulk_insert(self, collection, payloads):
        try:
            self.__connection()
            bulk = self.__db[collection].initialize_ordered_bulk_op()

            for payload in payloads:
                payload.pop('topic')
                bulk.insert(payload)

            bulk.execute()

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
