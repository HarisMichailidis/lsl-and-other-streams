import json
from typing import List
import yaml


def sample_encoder(timestamp: float, sample: List[float]):
    """

    :param timestamp: float
    :param sample: List[float]
    :return: str(json)
    """
    sample_dict = dict([(i, s) for i, s in enumerate(sample)])
    sample_dict['timestamp'] = timestamp
    return json.dumps(sample_dict)


def sample_decoder(encoded_sample: str):
    """

    :param encoded_sample: str
    :return: int, List[float]
    """
    encoded_sample_dict = json.loads(encoded_sample)

    timestamp = None
    if "timestamp" in encoded_sample_dict.keys():
        timestamp = encoded_sample_dict.pop('timestamp')

    sample_keys = list(encoded_sample_dict.keys())
    sample_keys.sort(reverse=False)

    sample = []
    for k in sample_keys:
        sample.append(encoded_sample_dict[k])

    return timestamp, sample


def read_yaml_config(filepath="config.yml"):
    with open(filepath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config
