from kafka import KafkaProducer
import time
from .reader import Reader
import pickle


class Producer:
    def __init__(self, file_name, topic, freq):
        self.topic = topic
        self.freq = freq if isinstance(freq, int) else int(freq)
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                      value_serializer=lambda x: pickle.dumps(x))

        self.reader = Reader(file_name)

    def star_write(self):
        message_count = 0
        for index in range(len(self.reader.data)):
            data = self.reader.data.iloc[index, :]
            dict_data = self.reader.row_to_dict(data)
            self.producer.send(self.topic, value=dict_data)
            print(f'Message {message_count + 1}: {dict_data}')
            message_count += 1
            time.sleep(self.freq)


if __name__ == '__main__':
    pass
