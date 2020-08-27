from .app import Consumer
import sys

if __name__ == '__main__':
    consumer = Consumer(sys.argv[1])
    consumer.star_read()
