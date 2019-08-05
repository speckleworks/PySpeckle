import requests, json, os
import sqlite3, contextlib
import struct, base64
from speckle.base.client import ClientBase

def jdumps(msg):
    return json.dumps(msg, indent=4, sort_keys=True)

class SpeckleApiClient(ClientBase):

    '''
    Utility functions
    '''

    def log(self, msg):
        print ('SpeckleClient: {}'.format(msg))

    def check_response_status_code(self, r):

        # Parse response
        if r.status_code == 200:
            self.log("Request successful: {}".format(r.reason))
            return True
        elif r.status_code == 400:
            self.log("Request failed: {}".format(r.reason))
        elif r.status_code != 200 and r.status_code != 204:
            self.log("The HTTP status code of the response was not expected: {},  {}".format(r.status_code, r.reason))
        else:
            self.log("Unknown response: {},  {}".format(r.status_code, r.reason))            
        # Debug
        if self.verbose:
            print()
            self.log(json.dumps(r.text, indent=4, sort_keys=True))            
        return False


    '''
    DEPRECATED

    def write_profile_to_file(self, profile, directory=None):
        assert ("email" in profile.keys())
        assert ("server" in profile.keys())
        assert ("server_name" in profile.keys())
        assert ("apitoken" in profile.keys())

        if directory == None:
            directory = os.path.join(os.getenv('LOCALAPPDATA'), os.path.join('SpeckleSettings', 'MigratedAccounts'))

        if os.path.isdir(directory):
            with open(os.path.join(directory, profile['email']) + ".JWT .txt", 'w') as f:
                f.write("{},{},{},{},{}\n".format(profile['email'], profile['apitoken'], profile['server_name'], profile['server'], profile['server']))
    

    def load_local_profiles(self, directory=None):
        profiles = []

        if directory == None:
            directory = os.path.join(os.getenv('LOCALAPPDATA'), os.path.join('SpeckleSettings', 'MigratedAccounts'))

        if os.path.isdir(directory):
            files = [os.path.join(directory, x) for x in os.listdir(directory) if x.endswith('.txt')]
            for file in files:
                with open(file, 'r') as f:
                    line = f.readline()
                    tokens = line.split(',')

                    if len(tokens) < 4: return None

                    profiles.append({'email':tokens[0], 'server_name': tokens[2], 'apitoken': tokens[1], 'server': tokens[3]})

        return profiles


    def set_profile(self, server, apitoken):
        self.server = server
        self.s.headers.update({'Authorization': apitoken})

    def use_existing_profile(self, email, directory=None):
        profiles = self.load_local_profiles(directory)
        profile = profiles[0] # Maybe worth implementing a retrieve by id?
        if email in profile.keys():
            self.server = profiles[email]['server']
            self.s.headers.update({'Authorization': profiles[email]['apitoken']})
            return True
        return False
    '''

    '''
    API calls
    '''

    def ClientCreateAsync(self, client):
        '''
        Create client
        '''
        url = self.server + "/clients"
        r = self.s.post(url, json.dumps(client))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ClientDeleteAsync(self, client):
        raise NotImplementedError

    def ClientGetAllAsync(self, query=""):
        '''
        Gets a user's profile
        '''
        url = self.server + "/clients?{}".format(query)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ClientGetAsync(self, client):
        raise NotImplementedError

    def ClientUpdateAsync(self, clientId, client):
        '''
        Update client
        '''
        url = self.server + "/clients/{}".format(clientId)
        r = self.s.put(url, json.dumps(client))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def CommentCreateAsync(self, resourceType, str, comment):
        raise NotImplementedError

    def CommentDeleteAsync(self, str):
        raise NotImplementedError

    def CommentGetAsync(self, str):
        raise NotImplementedError

    def CommentGetFromResourceAsync(self, resourceType, str):
        raise NotImplementedError

    def CommentUpdateAsync(self, str, comment):
        raise NotImplementedError
    '''
    def GetObjectData(System.Runtime.Serialization.SerializationInfo, System.Runtime.Serialization.StreamingContext):
        raise NotImplementedError
    
    def JoinRoom(self, str):
        raise NotImplementedError

    def LeaveRoom(self, str):
        raise NotImplementedError
    '''

    def ObjectCreateAsync(self, objectList):
        '''
        Create objects
        '''
        payload = []
        for o in objectList:
            if '_id' in o.keys():
                del o['_id']
            if 'hash' in o.keys():
                del o['hash']

            payload.append(o)

        url = self.server + "/objects"
        r = self.s.post(url, json.dumps(payload))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ObjectDeleteAsync(self, objectId):
        '''
        Delete a specific object
        '''
        url = self.server + "/objects/{}".format(objectId)
        r = self.s.delete(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ObjectGetAsync(self, objectId, query=""):
        '''
        Get a specific object
        '''
        url = self.server + "/objects/{}?{}".format(objectId, query)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ObjectGetBulkAsync(self, objectIds, query=""):
        '''
        Get a list of objects at once
        '''
        url = self.server + "/objects/getbulk?{}".format(query)
        r = self.s.post(url, data=json.dumps(objectIds))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ObjectUpdateAsync(self, objectId, speckle_object):
        '''
        Update object.
        '''
        assert objectId is not None
        url = self.server + "/objects/{}".format(objectId)
        r = self.s.put(url, json.dumps(speckle_object))

    def ObjectUpdatePropertiesAsync(self, objectId, prop):
        url = self.server + "/objects/{}/properties".format(objectId)
        r = self.s.put(url, json.dumps(prop))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ProjectCreateAsync(self, project):
        '''
        Create project
        '''
        url = self.server + "/projects"
        r = self.s.post(url, json.dumps(project))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ProjectDeleteAsync(self, projectId):
        '''
        Delete a project using the projectId
        '''
        url = self.server + "/projects/{}".format(projectId)
        r = self.s.delete(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ProjectGetAllAsync(self, query=""):
        '''
        Get all of a user's projects
        '''
        url = self.server + "/projects"
        if query:
            url += "?{}".format(query)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ProjectGetAsync(self, projectId):
        '''
        Get project by id
        '''
        url = self.server + "/projects/{}".format(projectId)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def ProjectUpdateAsync(self, projectId, project):
        '''
        Update an existing project
        '''
        url = self.server + "/projects/{}".format(projectId)
        r = self.s.put(url, json.dumps(project))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamCloneAsync(self, streamId):
        '''
        Clone an exsting stream
        '''
        url = self.server + "/streams/{}/clone".format(streamId)
        r = self.s.post(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamCreateAsync(self, stream):
        '''
        Create new stream
        '''
        url = self.server + "/streams"
        r = self.s.post(url, data=json.dumps(stream))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamDeleteAsync(self, streamId):
        '''
        Delete stream.
        '''
        assert streamId is not None
        url = self.server + "/streams/{}".format(streamId)
        r = self.s.delete(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamDiffAsync(self, streamId1, streamId2):
        '''
        Diff two streams
        '''
        url = self.server + "/streams/{}/diff/{}".format(streamId1, streamId2)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamGetAsync(self, streamId, query=""):
        '''
        Get stream
        '''
        url = self.server + "/streams/{}?{}".format(streamId, query)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamGetObjectsAsync(self, streamId, query=""):
        '''
        Get objects on stream..
        '''
        url = self.server + "/streams/{}/objects?{}".format(streamId, query)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamsGetAllAsync(self, query=""):
        '''
        Get all streams available to user.
        '''
        url = self.server + "/streams?omit=objects"
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def StreamUpdateAsync(self, streamId, stream):
        '''
        Update stream.
        '''
        assert streamId is not None
        url = self.server + "/streams/{}".format(streamId)
        r = self.s.put(url, json.dumps(stream))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def UserGetAsync(self):
        url = self.server + "/accounts"
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

    def UserGetProfileByIdAsync(self, userId):
        '''
        Get a user's profile
        '''
        url = self.server + "/accounts/{}".format(userId)
        r = self.s.get(url)

        if self.check_response_status_code(r):
            return r.json()
        return None

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

        r = self.s.post(url, data=json.dumps(user))

        if self.check_response_status_code(r):
            login_response = r.json()
            self.s.headers.update(
                {'Authorization': login_response['resource']['apitoken']})

            return login_response
        return None

    def UserRegisterAsync(self, user):
        assert ("server_name" in user.keys())
        assert ("email" in user.keys())
        assert ("password" in user.keys())
        assert ("name" in user.keys())
        assert ("surname" in user.keys())

        url = self.server + "/accounts/register"
        r = self.s.post(url, data=json.dumps(user))

        if self.check_response_status_code(r):
            return r.json()
        return None

    def UserSearchAsync(self, user):

        raise NotImplementedError

    def UserUpdateProfileAsync(self, user):
        assert ("server_name" in user.keys())
        assert ("email" in user.keys())
        assert ("password" in user.keys())
        assert ("name" in user.keys())
        assert ("surname" in user.keys())

        url = self.server + "/accounts/register"
        r = self.s.put(url, data=json.dumps(user))

        if self.check_response_status_code(r):
            return r.json()
        return None
