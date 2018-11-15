
import requests, json, os
import struct, base64


from .SpeckleResource import SpeckleResource


class SpeckleApiClient():

    def __init__(self):
        # Set default server
        self.server = "https://hestia.speckle.works/api/v1"

        # Create and configure requests.Session object
        self.session = requests.Session()
        self.session.headers.update({'content-type' : 'application/json', 'Authorization': ""})

        # Set verbosity
        self.verbose = False

    '''
    Utility functions
    '''

    def log(self, msg):
        print ('SpeckleClient: %s' % msg)

    def check_response_status_code(self, r):

        # Parse response
        if r.status_code == 200:
            self.log("Request successful: %s" % r.reason)
            return True
        elif r.status_code == 400:
            self.log("Request failed: %s" % r.reason)
        elif r.status_code != 200 and r.status_code != 204:
            self.log("The HTTP status code of the response was not expected: %s,  %s" % (r.status_code, r.reason))
        # Debug
        if self.verbose:
            print()
            self.log(json.dumps(r.text, indent=4, sort_keys=True))            
        return False

    def write_profile_to_file(self, profile, directory=None):
        assert ("email" in profile.keys())
        assert ("server" in profile.keys())
        assert ("server_name" in profile.keys())
        assert ("authtoken" in profile.keys())

        if directory == None:
            directory = os.path.join(os.getenv('LOCALAPPDATA'), 'SpeckleSettings')

        if os.path.isdir(directory):
            with open(os.path.join(directory, profile['email']) + ".JWT .txt", 'w') as f:
                f.write("%s,%s,%s,%s,%s\n" % (profile['email'], profile['authtoken'], profile['server_name'], profile['server'], profile['server']))


    def load_local_profiles(self, directory=None):
        profiles = {}

        if directory == None:
            directory = os.path.join(os.getenv('LOCALAPPDATA'), 'SpeckleSettings')

        if os.path.isdir(directory):
            files = [os.path.join(directory, x) for x in os.listdir(directory) if x.endswith('.txt')]
            for file in files:
                with open(file, 'r') as f:
                    line = f.readline()
                    tokens = line.split(',')

                    if len(tokens) < 4: return None

                    profiles[tokens[0]] = {'server_name': tokens[2], 'authtoken': tokens[1], 'server': tokens[3]}

        return profiles


    def use_existing_profile(self, email, directory=None):
        profiles = self.load_local_profiles(directory)
        if email in profiles.keys():
            self.server = profiles[email]['server']
            self.session.headers.update({'Authorization': profiles[email]['authtoken']})
            return True
        return False

    '''
    API calls
    '''

    def ClientCreateAsync(self, client): 
        raise NotImplmentedError

    def ClientDeleteAsync(self, client):
        raise NotImplmentedError

    def ClientGetAllAsync():
        raise NotImplmentedError

    def ClientGetAsync(self, client):
        raise NotImplmentedError

    def ClientUpdateAsync(self, str, client):
        raise NotImplmentedError

    def CommentCreateAsync(self, resourceType, str, comment):
        raise NotImplmentedError

    def CommentDeleteAsync(self, str):
        raise NotImplmentedError

    def CommentGetAsync(self, str):
        raise NotImplmentedError

    def CommentGetFromResourceAsync(self, resourceType, str):
        raise NotImplmentedError

    def CommentUpdateAsync(self, str, comment):
        raise NotImplmentedError
    '''
    def GetObjectData(System.Runtime.Serialization.SerializationInfo, System.Runtime.Serialization.StreamingContext):
        raise NotImplmentedError
    
    def JoinRoom(self, str):
        raise NotImplmentedError

    def LeaveRoom(self, str):
        raise NotImplmentedError
    '''

    def ObjectCreateAsync(self, objectList):
        '''
        Create objects
        '''
        payload = []
        for o in objectList:
            oDict = SpeckleResource.to_dict(obj)

            if '_id' in oDict.keys():
                del oDict['_id']
            if 'hash' in oDict.keys():
                del oDict['hash']

            payload.append(oDict)

        r = requests.post(url, json.dumps(payload), headers=self.CreateHeader())

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None 

    def ObjectDeleteAsync(self, objectId):
        raise NotImplmentedError

    def ObjectGetAsync(self, objectId, query=""):
        '''
        Get a specific object
        '''
        url = self.server + "/objects/%s?%s" % (objectId, query)
        r = self.session.get(url)

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    def ObjectGetBulkAsync(self, objectIds, query=""):
        '''
        Get a list of objects at once
        '''
        url = self.server + "/objects/getbulk?%s" % query
        r = self.session.post(url, data=json.dumps(objectIds))

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None    

    def ObjectUpdateAsync(self, objectId, speckle_object):
        '''
        Update object.
        '''
        assert objectId is not None
        url = self.server + "/objects/%s" % objectId
        r = self.session.put(url, SpeckleResource.to_json(speckle_object))

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    '''
    def ObjectUpdatePropertiesAsync(string, object, System.Threading.CancellationToken):
        raise NotImplmentedError

    def PrepareRequest(System.Net.Http.HttpClient, System.Net.Http.HttpRequestMessage, System.Text.StringBuilder):
        raise NotImplmentedError

    def ProcessResponse(System.Net.Http.HttpClient, System.Net.Http.HttpResponseMessage):
        raise NotImplmentedError

    def ProjectCreateAsync(SpeckleCore.Project, System.Threading.CancellationToken):
        raise NotImplmentedError

    def ProjectDeleteAsync(string, System.Threading.CancellationToken):
        raise NotImplmentedError

    def ProjectGetAllAsync(System.Threading.CancellationToken):
        raise NotImplmentedError

    def ProjectGetAsync(string, System.Threading.CancellationToken):
        raise NotImplmentedError

    def ProjectUpdateAsync(string, SpeckleCore.Project, System.Threading.CancellationToken):
        raise NotImplmentedError
    '''
    def StreamCloneAsync(self, streamId):
        raise NotImplmentedError

    def StreamCreateAsync(self, stream):
        '''
        Create new stream
        '''
        url = self.baseUrl + "/streams"
        r = requests.post(url, data=SpeckleResource.to_json(stream))

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None 

    def StreamDeleteAsync(self, streamId):
        '''
        Delete stream.
        '''
        assert streamId is not None
        url = self.server + "/streams/%s" % streamId
        r = self.session.delete(url)

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    def StreamDiffAsync(self, streamId1, streamId2):
        '''
        Diff two streams
        '''
        url = self.server + "/streams/%s/diff/%s" % (streamId1, streamId2)
        r = self.session.get(url)

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    def StreamGetAsync(self, streamId, query=""):
        '''
        Get stream
        '''
        url = self.server + "/streams/%s?%s" % (streamId, query)
        r = self.session.get(url)

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    def StreamGetObjectsAsync(self, streamId, query=""):
        '''
        Get objects on stream..
        '''
        url = self.server + "/streams/%s/objects?%s" % (streamId, query)
        r = self.session.get(url)

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    def StreamsGetAllAsync(self):
        '''
        Get all streams available to user.
        '''
        url = self.server + "/streams"
        r = self.session.get(url)

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    def StreamUpdateAsync(self, streamId, stream):
        '''
        Update stream.
        '''
        assert streamId is not None
        url = self.server + "/streams/%s" % streamId
        r = self.session.put(url, SpeckleResource.to_json(stream))

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None   

    def UserGetAsync(self):
        raise NotImplmentedError

    def UserGetProfileByIdAsync(self, userId):
        raise NotImplmentedError

    def UserLoginAsync(self, user):
        '''
        Login with email and password. 
        user - dictionary that must contain 'email' and 'password' keys
        '''
        assert ("email" in user.keys())
        assert ("password" in user.keys())

        url = self.server + "/accounts/login"

        if self.verbose:
            print(url)

        r = self.session.post(url, data=json.dumps(user))

        if self.check_response_status_code(r):
            login_response = r.json()
            self.session.headers.update({'Authorization': login_response['resource']['apitoken']})

            return login_response
        return None

    def UserRegisterAsync(self, user):
        assert ("server_name" in user.keys())
        assert ("email" in user.keys())
        assert ("password" in user.keys())
        assert ("name" in user.keys())
        assert ("surname" in user.keys())

        url = self.server + "/accounts/register"
        r = self.session.post(url, data=json.dumps(user))

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None

    def UserSearchAsync(self, user):

        raise NotImplmentedError

    def UserUpdateProfileAsync(self, user):
        assert ("server_name" in user.keys())
        assert ("email" in user.keys())
        assert ("password" in user.keys())
        assert ("name" in user.keys())
        assert ("surname" in user.keys())

        url = self.server + "/accounts/register"
        r = self.session.put(url, data=json.dumps(user))

        if self.check_response_status_code(r):
            return SpeckleResource(r.json())
        return None
    
if __name__ == '__main__':


    ''' 
    Create client and login
    '''

    client = SpeckleApiClient()
    client.verbose = True

    res = client.UserLoginAsync({"email":"tom.svilans@gmail.com", "password":"hotdogjuice"})
    #print(client.session.headers)

    '''
    Get a list of all available streams
    '''

    res = client.StreamsGetAllAsync()

    if res is None:
        raise Exception

    streams = {x.name: x for x in res.resources}

    print("\nStreams:\n")
    for stream in streams.values():
        print ("%s \t(%s)" % (stream.name, stream.streamId))

    '''
    Get some objects from a stream, but only their type and name
    '''

    res = client.StreamGetObjectsAsync(streams['Kelowna'].streamId, "fields=type,name,_id")

    if res is None:
        raise Exception

    objects = {x._id: x for x in res.resources}

    print("\nObjects:\n")
    for o in objects.values():
        print ("%s \t(%s, %s)" % (o.name, o.type, o._id))

    '''
    Get specific stream data
    '''

    res = client.StreamGetAsync(streams['Kelowna'].streamId)

    if res is None:
        raise Exception

    print(SpeckleResource.to_json_pretty(res.resource))

    '''
    Get a list of some objects
    '''

    objectList = list(objects.values())
    res = client.ObjectGetBulkAsync([x._id for x in objectList[:4]], "omit=vertices,faces,properties.texture_coordinates")

    if res is None:
        raise Exception

    print(SpeckleResource.to_json_pretty(res.resources))

    res = client.ObjectGetAsync(objectList[0]._id, "fields=name,owner,private")

    if res is None:
        raise Exception

    print(SpeckleResource.to_json_pretty(res.resource))



