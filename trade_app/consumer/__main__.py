import time

from .app import Consumer
import sys
import threading

if __name__ == '__main__':
    read_task_event = threading.Event()
    consumer = Consumer(sys.argv[1])

    thread_one = threading.Thread(name='Blocking read Threat', target=consumer.star_read)
    thread_one.start()

    while True:
        print('Message from main threat')
        time.sleep(3)
