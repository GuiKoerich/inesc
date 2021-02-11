from csv import DictReader
from datetime import datetime
from .utils import CSVHeadersEnum, CSVNamesEnum, names_csv, CSVDataEnum, \
    joint_topic_position_by_name, joint_topic_velocity_by_name, positions_or_velocities_by_joint
from mqtt.callbacks import get_topic_by_value, insert


class ImportCSV:
    __slots__ = ['__file_path', '__data_file', '__now']

    __STR_DATE_FORMAT = '%Y/%m/%d/%H:%M:%S.%f'

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__data_file = []
        self.__now = datetime.now()

        self.__open_file()

    def sync(self):
        self.__import_csv_data_by_type()

    def __open_file(self):
        with open(self.__file_path, newline='') as csv_file:
            for row in DictReader(csv_file):
                self.__data_file.append(row)

    def __import_csv_data_by_type(self):
        data = names_csv.get(self.__file_path.split('-')[-1].replace('.csv', ''))

        if data == CSVNamesEnum.TOOL_CARTESIAN.value:
            self.__import_tool_cartesian()

        elif data == CSVNamesEnum.JOINT_STATES.value:
            self.__import_joint_states()

    def __import_joint_states(self):
        for row in self.__data_file:
            payload = {
                'timestamp': self.__adjust_time(row.get(CSVHeadersEnum.TIME.value)),
                'names': self.__eval_type(row.get(CSVHeadersEnum.NAME.value)),
                'positions': self.__eval_type(row.get(CSVHeadersEnum.POSITION.value)),
                'velocities': self.__eval_type(row.get(CSVHeadersEnum.VELOCITY.value)),
            }

            payloads = self.__create_joint_state_payloads(payload)

            # print(payload)
            break

    def __create_joint_state_payloads(self, payload):
        payload_list = []

        for name in payload.get('names'):
            position_topic = joint_topic_position_by_name.get(name)
            index = positions_or_velocities_by_joint.get(position_topic)
            topic = get_topic_by_value(position_topic)

            payload_list.append({
                'timestamp': payload.get('timestamp'),
                position_topic: payload.get('positions')[index],
                'topic': get_topic_by_value(position_topic),
            })

            velocity_topic = joint_topic_velocity_by_name.get(name)
            payload_list.append({
                'timestamp': payload.get('timestamp'),
                velocity_topic: payload.get('velocities')[index],
                'topic': get_topic_by_value(velocity_topic),
            })

        print(payload_list)

    def __import_tool_cartesian(self):
        for row in self.__data_file:
            payload = {
                'timestamp': self.__adjust_time(row.get(CSVHeadersEnum.TIME.value)),
                'positions':  self.__get_cartesian_positions(row.get(CSVHeadersEnum.DATA.value))
            }
            payloads = self.__create_tool_cartesian_payloads(payload)

            self.__persist_payloads(payloads)
            break

    @staticmethod
    def __eval_type(type_parameter):
        return eval(type_parameter)

    @staticmethod
    def __create_tool_cartesian_payloads(payload):
        payload_list = []

        for position in payload.get('positions').keys():
            payload_list.append({
                'timestamp': payload.get('timestamp'),
                position: payload.get('positions').get(position),
                'topic': get_topic_by_value(position)
            })

        return payload_list

    @staticmethod
    def __persist_payloads(payloads):
        for payload in payloads:
            insert(topic=payload.pop('topic'), payload=payload)

    @staticmethod
    def __get_cartesian_positions(positions):
        pos = eval(positions)

        return {
            'posX': pos[CSVDataEnum.POS_X.value],
            'posY': pos[CSVDataEnum.POS_Y.value],
            'posZ': pos[CSVDataEnum.POS_Z.value],
        }

    def __adjust_time(self, str_time):
        return datetime.strptime(str_time, self.__STR_DATE_FORMAT).replace(
            year=self.__now.year, month=self.__now.month, day=self.__now.day)
