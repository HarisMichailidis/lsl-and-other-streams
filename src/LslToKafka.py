import uuid
from lib import read_yaml_config, sample_encoder
from confluent_kafka import Producer
from pylsl import StreamInlet, resolve_stream


class LslToKafka:
    def __init__(self):
        config = read_yaml_config()

        # Kafka Configs
        self.topic = config['kafka']['topic']
        self.callback_timeout = config['kafka']['producer']['callback_timeout']
        self.producer_conf = {
            'bootstrap.servers': config['kafka']['bootstrap_servers'],
            'client.id': config['kafka']['producer']['client_id']
        }
        self.producer = Producer(self.producer_conf)

        # LSL Configs
        self.lsl_stream_name = config['lsl']['name']
        self.lsl_pulling_timeout = config['lsl']['pulling_timeout']

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
                print(timestamp, time_correction, sample)

                # TODO what should be the key?
                key = str(uuid.uuid4())
                print("Sending message to Kafka with key: {}".format(key))
                self.producer.produce(
                    topic=self.topic,
                    key=key,
                    value=sample_encoder(timestamp, sample),
                    timestamp=int(timestamp),
                    callback=callback
                )

                # TODO not sure if we need to wait for this
                # Wait up to <callback_timeout> second for events. Callbacks will be invoked during
                # this method call if the message is acknowledged.
                print("Waiting for the callback")
                self.producer.poll(self.callback_timeout)

                # TODO review this option
                print("Making it sync by flushing")
                self.producer.flush()


def callback(error, msg):
    if error is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(error)))
    else:
        print("Message produced: %s" % (str(msg)))


if __name__ == '__main__':
    lslToKafka = LslToKafka()
    lslToKafka.run()
