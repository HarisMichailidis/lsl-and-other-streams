from lib import read_yaml_config
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from pylsl import StreamInlet, resolve_stream


class LslToKafkaAvro:
    def __init__(self):
        config = read_yaml_config("config-avro.yml")

        # Kafka Configs
        self.topic = config['kafka']['topic']
        self.callback_timeout = config['kafka']['producer']['callback_timeout']
        self.schema_registry = config['kafka']['schema_registry']
        self.schema_path = config['kafka']['schema_path']
        self.producer_conf = {
            'bootstrap.servers': config['kafka']['bootstrap_servers'],
            'client.id': config['kafka']['producer']['client_id'],
            'key.serializer': None,
            'value.serializer': self.get_avro_serializer()
        }
        self.producer = SerializingProducer(self.producer_conf)

        # LSL Configs
        self.lsl_stream_name = config['lsl']['name']
        self.lsl_pulling_timeout = config['lsl']['pulling_timeout']

    def get_avro_serializer(self):
        schema_registry_client = SchemaRegistryClient({'url': self.schema_registry})

        with open(self.schema_path, 'rt') as f:
            schema_str = f.read()

        return AvroSerializer(schema_str, schema_registry_client)

    def run(self):
        # LSL stuff
        print("Looking for our stream...")
        streams = resolve_stream('name', self.lsl_stream_name)
        if len(streams) != 1:
            print("ERROR: Multiple Streams found with the same name")
            print(streams)
            exit()

        stream = streams[0]
        print("Stream found with name: {}".format(stream))
        # create a new inlet to read from the stream
        inlet = StreamInlet(stream)

        while True:
            print("\nPulling from LSL Stream...")
            raw_sample, raw_timestamp = inlet.pull_sample(self.lsl_pulling_timeout)

            if raw_sample:
                sample = raw_sample
                timestamp = raw_timestamp
                time_correction = inlet.time_correction()
                print(timestamp, time_correction, sample[0])

                print("Sending message to Kafka with timestamp: {}".format(timestamp))
                self.producer.produce(
                    topic=self.topic,
                    key=None,
                    value={"timestamp": timestamp, "sample": sample},
                    timestamp=int(timestamp),
                    on_delivery=delivery_report
                )

                # TODO not sure if we need to wait for this
                # Wait up to <callback_timeout> second for events. Callbacks will be invoked during
                # this method call if the message is acknowledged.
                print("Waiting for the callback")
                self.producer.poll(self.callback_timeout)

                # TODO review this option
                print("Making it sync by flushing")
                self.producer.flush()


def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('Record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


if __name__ == '__main__':
    lslToKafkaAvro = LslToKafkaAvro()
    lslToKafkaAvro.run()
