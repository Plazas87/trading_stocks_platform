from kafka import KafkaConsumer
import pickle
from trade_app.config import ConfigConsumer


class Consumer:
    def __init__(self, config_obj):
        self._consumer = KafkaConsumer(config_obj[ConfigConsumer.topic.name],
                                       bootstrap_servers=[config_obj[ConfigConsumer.bootstrap_servers.name]],
                                       value_deserializer=lambda x: pickle.loads(x),
                                       group_id=config_obj[ConfigConsumer.group_id.name])

    @property
    def consumer(self):
        return self._consumer

    @consumer.setter
    def consumer(self, value):
        if isinstance(value, KafkaConsumer):
            self._consumer = value

    def star_read(self):
        self.receive_message()

    def receive_message(self):
        message_count = 0
        for message in self._consumer:
            message = message.value
            print(f'Message {message_count}: {message}')
            message_count += 1


if __name__ == '__main__':
    pass
