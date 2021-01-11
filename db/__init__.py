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

    def get_all(self, collection):
        try:
            self.__connection()

            for result in self.__db[collection].find():
                print(result)

        except Exception as ex:
            print(ex)
        finally:
            self.__client.close()

    def delete(self, collection):
        try:
            self.__connection()

            for result in self.__db[collection].find():
                self.__db[collection].delete_one(result)

        except Exception as ex:
            print(ex)
        finally:
            self.__client.close()


if __name__ == '__main__':
    m = Mongo()
    m.get_all('Sala')
    m.delete('Sala')
