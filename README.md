# lsl-and-other-streams
A repository containing ideas and implementations of LSL (Lab Streaming Layer) integration with other streaming services

# Versions
- Python: `3.9.1`
- Kafka: `2.5.1`
- For Python packages see the `requirements.txt`


# LSL - Lab Streaming Layer
https://github.com/labstreaminglayer

https://github.com/sccn/labstreaminglayer


## PyLSL - Python interface to LSL
https://github.com/labstreaminglayer/liblsl-Python


## App-LabRecorder
https://github.com/labstreaminglayer/App-LabRecorder/

To use LabRecorded download the latest release from here: https://github.com/labstreaminglayer/App-LabRecorder/releases

### macOS - troubleshooting

In my case, with macOS Big Sur (11.2.1), it wasn't working out of the box and needed to do the following:

- install Qt `brew install qt`
- download the [LabRecorder-1.14.0-OSX_amd64.tar.bz2](https://github.com/labstreaminglayer/App-LabRecorder/releases/download/v1.14.0/LabRecorder-1.14.0-OSX_amd64.tar.bz2)
- unzip it and go into the `LabRecorder/` dir
- use the following command to see the linked libs `otool -L LabRecorder.app/Contents/MacOS/LabRecorder` *
```bash
@rpath/QtWidgets.framework/Versions/5/QtWidgets
@rpath/QtNetwork.framework/Versions/5/QtNetwork
...
```
- manually link the ones that were not linked (`@rpath`) using the `install_name_tool` like this:
```bash
install_name_tool -change @rpath/QtWidgets.framework/Versions/5/QtWidgets \
  /usr/local/Cellar/qt/5.15.2/lib/QtWidgets.framework/Versions/5/QtWidgets \
  LabRecorder.app/Contents/MacOS/LabRecorder
```
- same for the rest until all have been replaced, like:
```bash
/usr/local/Cellar/qt/5.15.2/lib/QtWidgets.framework/Versions/5/QtWidgets
/usr/local/Cellar/qt/5.15.2/lib/QtNetwork.framework/Versions/5/QtNetwork
...
```

**The otool/install_name_tool solution is inspired by a stackoverflow post which I can't recover*


# Python

## Choosing Python Kafka Library

Summary: We'll go with the `Confluent-Kafka` as it seems to be the most performant
of the two actively maintained libraries. See below for more details. 

A useful read (2020):
<br> https://towardsdatascience.com/3-libraries-you-should-know-to-master-apache-kafka-in-python-c95fdf8700f2


### Kafka-Python
`pip install kafka-python`
<br> https://kafka-python.readthedocs.io/en/master/index.html
<br> https://github.com/dpkp/kafka-python

**Actively maintained**
- Stars: `4.2k`
- Forks: `1.1k`
- Latest Kafka version: `2.6`
- Latest Python version: `3.8`


### Confluent-Kafka-Python
`pip install confluent-kafka`
<br> https://docs.confluent.io/platform/current/clients/confluent-kafka-python/index.html#
<br> https://github.com/confluentinc/confluent-kafka-python

**Actively maintained**
- Stars: `2.2k`
- Forks: `579`
- Latest Kafka version: `all broker versions >= 0.8`
- Latest Python version: `3.8`


### PyKafka
`pip install pykafka`
<br> https://pykafka.readthedocs.io/en/latest/index.html
<br> https://github.com/Parsely/pykafka

**Hasn't been updated since 2019**
- Stars: `1.1k`
- Forks: `232`
- Latest Kafka version: `supports versions of Kafka 0.8.2 and newer`
- Latest Python version: `3.6`


## Python-AVRO
https://www.perfectlyrandom.org/2019/11/29/handling-avro-files-in-python/

### Description
The official library `avro`/`avro-python3` seems that it's much slower than the 3rd party `fastavro` which is widely adopted.



## Troubleshooting

To install the venv kernel to the jupyter notebook execute the following while having activated your venv:
```bash
python -m ipykernel install --name "lsl-and-other-streams" --user
```
Then launch the jupyter notebook and the kernel should be there:
```bash
python -m jupyter notebook 
```

