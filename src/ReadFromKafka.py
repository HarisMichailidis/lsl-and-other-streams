from lib import read_yaml_config
from confluent_kafka import Consumer, KafkaError


class ReadFromKafka:
    def __init__(self):
        config = read_yaml_config()

        # Kafka Configs
        self.topics = [config['kafka']['topic']]
        self.poll_timeout = config['kafka']['consumer']['poll_timeout']
        self.consumer_conf = {
            'bootstrap.servers': config['kafka']['bootstrap_servers'],
            'group.id': config['kafka']['consumer']['group_id'],
            'auto.offset.reset': config['kafka']['consumer']['auto_offset_reset'],
            'error_cb': error_cb
        }
        self.consumer = Consumer(self.consumer_conf)

    def run(self):
        self.consumer.subscribe(self.topics)

        while True:
            msg = self.consumer.poll(self.poll_timeout)

            if msg is None:
                print("Poll timeout reached, continuing")
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print('Received message: key:{}  |value:{}'.format(msg.key().decode('utf-8'), msg.value().decode('utf-8')))

        self.consumer.close()


def error_cb(error):
    print("Callback error: {}".format(error))


if __name__ == '__main__':
    readFromKafka = ReadFromKafka()
    readFromKafka.run()