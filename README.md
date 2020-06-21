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

# Create a client using the appropriate server
client = SpeckleApiClient('hestia.speckle.works')

# Login with your details
client.login(
    email='test@test.com',
    password='Speckle<3Python'
)

# Stream ID to get
stream_id = 'HjenwS2s'

# Get stream data using its ID
stream = client.streams.get(stream_id)

# Print the list of placeholder objects in the stream
for object in stream.objects:
  print(object)
```

To get a list of all available streams and find a particular one by name:
```python

# Fetch the list of all available streams
streams = client.streams.list()
name = "JetStream"

# Go through the list and find the stream by name
stream = None
for s in streams:
    if s.name == name:
        stream = s
        break
        
# If the stream is found, fetch the full stream data, using an optional query dict 
# to omit some data
if stream:
    stream_data = client.streams.get(stream.streamId, {'omit':['layers','comments']})
```

To get object data from a stream:

```python
stream = client.streams.get(streamId)

# Fetch a single object using its placeholder ID
object = client.objects.get(stream.objects[0].id)

# Fetch the objects all at once using an optional query dict
objects = client.objects.get_bulk([o.id for o in stream.objects], {'omit':'base64','displayValue'})

# Print out some object info
for o in objects:
    print("Object {} is type {}".format(o.id, o.type)
```

To create some data and upload it to a stream:
```python
import speckle.schemas

# Create some mesh data
vertices = [[0,0,0],[1,0,0],[1,1,0], [0,1,0]]
faces = [[0,1,2,3]]

# Create a Speckle Mesh object
sm = speckle.schemas.Mesh()

# Add vertices
for v in vertices:
    sm.vertices.extend(v)

# Add faces
for f in faces:
    if len(f) == 3: # if it is a triangle...
        sm.faces.append(0)
    elif len(f) == 4: # if it is a quad...
        sm.faces.append(1)
    sm.faces.extend(f)

# Give it a nice name
sm.name = "FancyMesh"

# Create the object on the server and receive a list of
# placeholders in return (with only one placeholder)
placeholders = client.objects.create(sm)

# Fetch the stream that we want to update
stream = client.streams.get(streamId)

# Set the stream object list to the created object or
# extend it to add the object to the existing list
stream.objects = placeholders
#stream.objects.extend(placeholders)

# Update the stream with the new data
client.streams.update(stream.streamId, stream)
```

Usage documentation can be found [here](https://pyspeckle.readthedocs.io/en/latest/).



## Maintainers
SpeckleBlender is written and maintained by [Tom Svilans](http://tomsvilans.com) ([Github](https://github.com/tsvilans)), [Izzy Lyseggen](https://github.com/izzylys) and [Antoine Dao](https://github.com/antoinedao).

## Notes
Commit formatting can be found [here](https://gist.github.com/brianclements/841ea7bffdb01346392c#type).
