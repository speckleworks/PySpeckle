# QuickStart

Playing with a new library or API client can be daunting. We feel you! This is why we have compiled a bunch of example usage scenarios to walk you through how to use the python speckle client.

In the following set of examples we assume you don't have your own Speckle server up and running so you can test all of the steps below by connecting to the `hestia` speckle server.

First we must instantiate the `SpeckleApiClient`. You can name it whatever you want, we will use `client` for simplicity. As we are connecting to the `hestia` test server we will input the full domain name as an argument: `hestia.speckle.works`

```python
from speckle import SpeckleApiClient

client = SpeckleApiClient('hestia.speckle.works')
```

## Registering and Logging in
Before you can do anything with Speckle you need to register yourself to the server you are going to be using. If you have already registered then you can skip the first code section below and look at the one right after where we explain how to login.

.. note::

  When you register using a PySpeckle client this client is also authenticated and you can start using it to make API calls immediately without needing to login.

```python
client.register(
    email='test@test.com',
    password='Speckle<3Python',
    company='SnakeySnakes',
    name='Snakey',
    surname='Snake'
)
```

If you are already registered then you can simply login your client as follows:

```python
client.login(
    email='test@test.com',
    password='Speckle<3Python'
)
```

## Sending and Retrieving Things
At the moment the api client takes dictionary payloads as data inputs (a `Speckle Object` for example) and returns data classes in most cases (essentially a class instance). If a data class is not returned then the object return is a dictionary. 

.. warning::
    
  Whether the client returns a data class or a dictionary is not yet very well segmented. To be sure you are getting back what you expect from the python client we reccomend reading through the :doc:`API referemce </client_api_ref>`

.. attention::

  PySpeckle doesn't yet support any of the `websockets` data transfer methods that the SpeckleServer offers. We're working on it. Feel free to `contribute <https://github.com/speckleworks/PySpeckle/issues/1>`_ if you've got an idea on how to implement it.

### Common Methods
Speckle mostly follows a bog standard REST API setup where a user can `POST`, `GET`, `PUT` and `DELETE` different resources. As such the following verbs can be used to make standard REST calls to Speckle.

.. warning::

  For most resources that support a `get`, `update`, `delete` call the `id` value to use to retrieve them is the `object.id` or Mongo `ObjectId`. The exception to this rule is the `Stream` resource which can only be retrieved by using the `StreamId` property of that stream.

#### Create 
Equivalent of `POST / -d '{"key1":"value1", "key2":"value2"}'`

```python
project = {
    'name': 'test project',
    'description': 'a project made for testing purposes',
    'tags': [],
    'streams': [],
}

project = client.projects.create(data=project)

print(project.id)
```

#### List
Equivalent of `GET /`

```python
projects = client.projects.list()

for project in projects:
  print(project.dict())
```

#### Get
Equivalent of `GET /{id}`

```python
project_id = '507f1f77bcf86cd799439011'

project = client.projects.get(project_id)

print(project.dict())
```

#### Update
Equivalent of `PUT /{id} -d '{"key1":"value1", "key2":"value2"}'`

.. note::
  The update method returns a payload response dictionary rather than a resource data class. The response payload should look something like this

  .. code-block:: python

      {
        "success": True,
        "message": "Patched ['description'] for 507f1f77bcf86cd799439011"
      }


.. warning::

  The `update` method will replace all the values in the input dictionary payload even if they are `None`. Be careful if you are trying to run `upsert` commands with dictionaries that contain `None` values

```python
project_id = '507f1f77bcf86cd799439011'
project_update = {
    'description': 'a project updated for testing purposes',
}

response = client.projects.update(id=project_id, data=project_update)

assert response['success'], response['message']
```

#### Delete
Equivalent of `DELETE /{id}`

.. note::
  The delete method returns a payload response dictionary rather than a resource data class. The response payload should look something like this

  .. code-block:: python

      {
        "success": True,
        "message": "Project was deleted."
      }

```python
project_id = '507f1f77bcf86cd799439011'

response = client.projects.delete(id=project_id)

assert response['success'], response['message']
```
## API Objects
If you've made it this far down you're probably thinking to yourself:

.. epigraph::

   Great I can login and mess with a project... anything else I can do?

   -- Some Ambitious User

Glad you asked! There are a bunch of different types of Speckle objects or resources you can mess with using this python client. Here is a list of them with links to their specific documentation:

* [Accounts](./client_api_ref.html#module-speckle.resources.accounts)
* [Projects](./client_api_ref.html#module-speckle.resources.projects)
* [Streams](./client_api_ref.html#module-speckle.resources.streams)
* [API Clients](./client_api_ref.html#module-speckle.resources.api_clients)
* [Comments](./client_api_ref.html#module-speckle.resources.comments)
* [SpeckleObjects](./client_api_ref.html#module-speckle.resources.objects)

.. note::
  Each resource supports some or all of the common methods described `above <./quickstart.html#common-methods>`_. Additionally each resource might support some extra methods which are specific to that resource. A good example is the `stream` resource which supports the `clone` method

    .. code-block:: python

      streamId = 'GBexG1'

      clone_stream, parent_stream = client.streams.clone(streamId)

## Parting Notes
Hope you've found this quickstart guide useful. Please do contribute any proposed changes/improvements on the main projects [github repo](https://github.com/speckleworks/pyspeckle).