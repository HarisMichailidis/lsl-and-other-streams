# lsl-and-other-streams
A repository containing ideas and implementations of LSL (Lab Streaming Layer) integration with other streaming services


# LSL - Lab Sreaming Layer
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
