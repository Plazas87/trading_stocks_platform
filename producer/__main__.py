from .app import Producer
import sys


if __name__ == '__main__':
    producer = Producer(sys.argv[1])
    producer.star_write()
