from datetime import datetime, timedelta
from pymongo import MongoClient


class Mongo:
    __slots__ = ['__client', '__db', '__bulk']

    # __host = 'inescfloripa.computacaosc.com.br'
    __host = '127.0.0.1'
    # __port = 443
    __port = 27017

    __db_name = 'IND4Fibre_2'

    __TIME_FORMAT = '%Y-%m-%d-%H:%M:%S'
    __initial_date = 0
    __end_date = 1

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

    def select_all(self, collection=None, interval=None, between=None):
        try:
            self.__connection()
            result = {}
            options = None

            if interval:
                start = datetime.now() - timedelta(minutes=interval)
                options = {'timestamp': {'$gt': str(start)}}

            if between:
                start, end = self.__get_between_dates(between)
                options = {'timestamp': {'$gte': str(start), '$lt': str(end)}}

            if not collection:
                for data_collection in self.__db.list_collections():
                    collection = data_collection.get('name')
                    result.update(self.__get_data_by_collection(collection, options))

            else:
                return self.__get_data_by_collection(collection, options)

            return result

        except Exception as ex:
            return {'message': ex, 'status': 'error'}

        finally:
            self.__client.close()

    def __get_data_by_collection(self, collection: str, options: dict) -> dict:
        return {
            collection: [data for data in self.__db[collection].find(options)]
        }

    def __get_between_dates(self, between: str) -> (datetime, datetime):
        dates = between.split(' ')

        return self.__get_date_by_format(dates[self.__initial_date]), self.__get_date_by_format(dates[self.__end_date])

    def __get_date_by_format(self, date_string: str) -> datetime:
        return datetime.strptime(date_string, self.__TIME_FORMAT)
