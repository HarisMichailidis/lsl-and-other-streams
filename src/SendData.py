import sys
import time
from random import random as rand
from pylsl import StreamInfo, StreamOutlet, local_clock
from lib import read_yaml_config


def main(argv):
    config = read_yaml_config()['lsl']
    srate = config['srate']
    name = config['name']
    type = config['type']
    n_channels = config['n_channels']
    stream_id = config['stream_id']
    producer_sleep = config['producer_sleep']

    # Create the Stream
    info = StreamInfo(name, type, n_channels, srate, 'float32', stream_id)

    # next make an outlet
    outlet = StreamOutlet(info)

    print("Starting sending data at {}Hz...".format(srate))
    start_time = local_clock()
    sent_samples = 0
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
            # make a new random n_channels sample; this is converted into a
            # pylsl.vectorf (the data type that is expected by push_sample)
            mysample = [sent_samples + sample_ix]
            mysample.extend([rand() for _ in range(n_channels - 1)])
            # now send it with the current timestamp
            outlet.push_sample(mysample, timestamp=time.time())
            print("Sent Sample: {}".format(mysample[0]))
        sent_samples += required_samples
        # wait for a bit before trying again.
        time.sleep(producer_sleep)


if __name__ == '__main__':
    main(sys.argv[1:])
