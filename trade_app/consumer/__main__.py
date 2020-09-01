import time

from .app import Consumer
import threading
from trade_app.builconfigurations import BuildConfiguration
from trade_app.config import ConfigFileSection

if __name__ == '__main__':
    config_obj = BuildConfiguration()
    read_task_event = threading.Event()
    consumer = Consumer(config_obj[ConfigFileSection.consumer.name])

    thread_one = threading.Thread(name='Blocking read Threat', target=consumer.star_read)
    thread_one.start()

    while True:
        print('Message from main threat')
        time.sleep(3)
