from kafka import KafkaProducer
import time
import pickle
import json

from .reader import Reader


class Producer:
    def __init__(self, file_name, topic, freq):
        self.topic = topic
        self.freq = freq if isinstance(freq, int) else int(freq)
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'))

        self.reader = Reader(file_name)

    def star_write(self):
        for index, value in self.reader.data.iterrows():
            dict_data = dict(value)
            self.producer.send(self.topic, value=dict_data)
            print(f'Message {index + 1}: {dict_data}')
            time.sleep(self.freq)


if __name__ == '__main__':
    pass
