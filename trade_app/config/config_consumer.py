from enum import Enum


class ConfigConsumer(Enum):
    topic = 0
    bootstrap_servers = 1
    group_id = 2
