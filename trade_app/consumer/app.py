from kafka import KafkaConsumer
import pickle


class Consumer:
    def __init__(self, topic):
        self.consumer = KafkaConsumer(topic,
                                      bootstrap_servers=['localhost:9092'],
                                      value_deserializer=lambda x: pickle.loads(x),
                                      group_id='netflix')

    def star_read(self):
        self.receive_message()

    def receive_message(self):
        message_count = 0
        for message in self.consumer:
            message = message.value
            print(f'Message {message_count}: {message}')
            message_count += 1


if __name__ == '__main__':
    pass
