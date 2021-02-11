from enum import Enum

names_csv = {
    'tool_cartesian': 1,
    'joint_states': 2,
    'alarmHigh': 3,
}

joint_topic_position_by_name = {
    'elbow_joint': 'joint1',
    'robotiq_85_left_knuckle_joint': 'joint2',
    'shoulder_lift_joint': 'joint3',
    'shoulder_pan_joint': 'joint4',
    'wrist_1_joint': 'joint5',
    'wrist_2_joint': 'joint6',
    'wrist_3_joint': 'joint7',
}

joint_topic_velocity_by_name = {
    'elbow_joint': 'vel1',
    'robotiq_85_left_knuckle_joint': 'vel2',
    'shoulder_lift_joint': 'vel3',
    'shoulder_pan_joint': 'vel4',
    'wrist_1_joint': 'vel5',
    'wrist_2_joint': 'vel6',
    'wrist_3_joint': 'vel7',
}

positions_or_velocities_by_joint = {
    'joint1': 0,
    'joint2': 1,
    'joint3': 2,
    'joint4': 3,
    'joint5': 4,
    'joint6': 5,
    'joint7': 6,
}


class CSVNamesEnum(Enum):
    TOOL_CARTESIAN = 1
    JOINT_STATES = 2
    ALARM_HIGH = 3


class CSVHeadersEnum(Enum):
    TIME = 'time'
    DATA = '.data'
    NAME = '.name'
    POSITION = '.position'
    VELOCITY = '.velocity'


class CSVDataEnum(Enum):
    POS_X = 0
    POS_Y = 1
    POS_Z = 2
