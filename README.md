# PySpeckle
A Python Speckle Client

[![Build Status](https://travis-ci.com/speckleworks/PySpeckle.svg?branch=master)](https://travis-ci.com/speckleworks/PySpeckle)

[Speckle.Works](https://www.speckle.works)

> Speckle: open digital infrastructure for designing, making and operating the built environment.
> We reimagine the design process from the Internet up: Speckle is an open source (MIT) initiative for developing an extensible Design & AEC data communication and collaboration platform.


## Installation
PySpeckle can be installed through `pip`:
`pip install speckle`

## Disclaimer
This code is WIP and as such should be used with caution, on non-sensitive projects.

## Description

PySpeckle is a light Python wrapper / interface for the Speckle framework. It can be used independently through Python scripts, or as a base for building various plug-ins, such as [SpeckleBlender](https://github.com/speckleworks/SpeckleBlender). 

## Quick Start
Here is how you initialise a client, authenticate and start speckling:
```python
from speckle import SpeckleApiClient

client = SpeckleApiClient('hestia.speckle.works')

client.login(
    email='test@test.com',
    password='Speckle<3Python'
)

stream_id = 'HjenwS2s'

stream = client.streams.get(stream_id)

for object in stream.objects:
  print(object.dict())
```

To get a list of all available streams and find a particular one by name:
```python
streams = client.streams.list()
name = "JetStream"

try:
    stream_id = [s for s in streams if s.name == name][0].streamId
except:
    print("Stream {} not found.".format(name))
    return
```

To get all objects from a stream:

```python
for o in stream.objects:
    try:
        obj = client.objects.get(o.id)
    except:
        continue
    print("Object {} is type {}.".format(obj.name, obj.type))
```

Usage documentation can be found [here](https://pyspeckle.readthedocs.io/en/latest/).



## Maintainers
SpeckleBlender is written and maintained by [Tom Svilans](http://tomsvilans.com) ([Github](https://github.com/tsvilans)), [Izzy Lyseggen](https://github.com/izzylys) and [Antoine Dao](https://github.com/antoinedao).

## Notes
Commit formatting can be found [here](https://gist.github.com/brianclements/841ea7bffdb01346392c#type).
