from csv import DictReader
from datetime import datetime
from .utils import CSVHeadersEnum, CSVNamesEnum, names_csv, CSVDataEnum, \
    joint_topic_position_by_name, joint_topic_velocity_by_name, positions_or_velocities_by_joint
from mqtt.callbacks import get_topic_by_value, insert, define_topic


class ImportCSV:
    __slots__ = ['__file_path', '__data_file', '__now']

    __STR_ROBOT_DATE_FORMAT = '%Y/%m/%d/%H:%M:%S.%f'

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
        name = self.__file_path.split('-')[-1].replace('.csv', '')
        data = names_csv.get(name)

        if data == CSVNamesEnum.TOOL_CARTESIAN.value:
            self.__import_tool_cartesian()

        elif data == CSVNamesEnum.JOINT_STATES.value:
            self.__import_joint_states()

        elif data == CSVNamesEnum.ALARM_HIGH.value:
            self.__import_alarm_high(name)

    def __import_joint_states(self):
        for row in self.__data_file:
            payload = {
                'timestamp': self.__adjust_time(row.get(CSVHeadersEnum.TIME.value)),
                'names': self.__eval_type(row.get(CSVHeadersEnum.NAME.value)),
                'positions': self.__eval_type(row.get(CSVHeadersEnum.POSITION.value)),
                'velocities': self.__eval_type(row.get(CSVHeadersEnum.VELOCITY.value)),
            }

            payloads = self.__create_joint_state_payloads(payload)

            self.__persist_payloads(payloads)

    @staticmethod
    def __create_joint_state_payloads(payload):
        payload_list = []

        for name in payload.get('names'):
            position_topic = joint_topic_position_by_name.get(name)
            index = positions_or_velocities_by_joint.get(position_topic)

            payload_list.append({
                'timestamp': payload.get('timestamp'),
                define_topic(position_topic): payload.get('positions')[index],
                'topic': get_topic_by_value(position_topic),
            })

            velocity_topic = joint_topic_velocity_by_name.get(name)
            payload_list.append({
                'timestamp': payload.get('timestamp'),
                define_topic(velocity_topic): payload.get('velocities')[index],
                'topic': get_topic_by_value(velocity_topic),
            })

        return payload_list

    def __import_tool_cartesian(self):
        for row in self.__data_file:
            payload = {
                'timestamp': self.__adjust_time(row.get(CSVHeadersEnum.TIME.value)),
                'positions':  self.__get_cartesian_positions(row.get(CSVHeadersEnum.DATA.value))
            }

            payloads = self.__create_tool_cartesian_payloads(payload)

            self.__persist_payloads(payloads)

    @staticmethod
    def __eval_type(type_parameter):
        return eval(type_parameter)

    @staticmethod
    def __create_tool_cartesian_payloads(payload):
        payload_list = []

        for position in payload.get('positions').keys():
            topic = get_topic_by_value(position)

            payload_list.append({
                'timestamp': payload.get('timestamp'),
                define_topic(topic): payload.get('positions').get(position),
                'topic': topic
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

    def __import_alarm_high(self, name):
        topic = get_topic_by_value(name, concat=False)
        payload_lists = []

        for row in self.__data_file:
            payload_lists.append({
                'timestamp': self.__adjust_time(row.get(CSVHeadersEnum.TIME.value)),
                define_topic(topic): self.__eval_type(row.get(CSVHeadersEnum.DATA.value)),
                'topic': topic,
            })

        self.__persist_payloads(payload_lists)

    def __adjust_time(self, str_time):
        return datetime.strptime(str_time, self.__STR_ROBOT_DATE_FORMAT).replace(
            year=self.__now.year, month=self.__now.month, day=self.__now.day)
