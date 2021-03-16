from lib import read_yaml_config
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer


class ReadFromKafkaAvro:
    def __init__(self):
        self.schema_path = None
        config = read_yaml_config("config-avro.yml")

        # Kafka Configs
        self.topics = [config['kafka']['topic']]
        self.poll_timeout = config['kafka']['consumer']['poll_timeout']
        self.schema_registry = config['kafka']['schema_registry']
        self.schema_path = config['kafka']['schema_path']
        self.consumer_conf = {
            'bootstrap.servers': config['kafka']['bootstrap_servers'],
            'group.id': config['kafka']['consumer']['group_id'],
            'auto.offset.reset': config['kafka']['consumer']['auto_offset_reset'],
            'key.deserializer': None,
            'value.deserializer': self.get_avro_deserializer()
        }
        self.consumer = DeserializingConsumer(self.consumer_conf)

    def get_avro_deserializer(self):
        schema_registry_client = SchemaRegistryClient({'url': self.schema_registry})

        with open(self.schema_path, 'rt') as f:
            schema_str = f.read()

        return AvroDeserializer(schema_str, schema_registry_client)

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

            print('Received message: timestamp:{}, sample[0]:{}'.format(msg.value()['timestamp'],msg.value()['sample'][0]))

        self.consumer.close()


if __name__ == '__main__':
    readFromKafkaAvro = ReadFromKafkaAvro()
    readFromKafkaAvro.run()
