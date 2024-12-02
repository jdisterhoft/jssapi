"""
#########################################################################################
Notes:    This library provides a class to interact with the Jamf Pro API using bearer token
          authentication.
          Requires the 'requests' library
#########################################################################################
"""

import base64
import json
import requests
import getpass


class JssApi:
    """
    Class is used to create a JSS connection object and make api calls
    using the information stored in attributes

    To connect, create an instance, connect, perform tasks, then invalidate the token:
    api = jssapi_obj.JssApi(jss_url)
    api.connect()
    # Perform Tasks
    api.invalidate_token()

    Attributes
    ----------
        url: str
            Stores the URL of the JSS server
        user: str
            Stores username for connection
        pword: str
            Stores password for connection
        enc_creds: str
            Stores credentials after encoding (see encode_credentials method)
        bearer_token: str
            Stores bearer token after retrieval
        token_valid: bool
            Stores boolean status on if token is known to be valid

    Methods
    ----------
        get_user_creds:
            Prompts user for credentials and assigns to attributes
        encode_credentials:
            Takes user credentials from attributes and encodes them
        get_bearer_token:
            Uses encoded credentials from attribute to retrieve bearer token
        invalidate_token:
            Invalidates the bearer token
        connect:
            Calls internal methods to get credentials, encode, and create connection
        get_resource(rsc=""):
            Accepts resource path (rsc), makes api call, and returns JSON data
    """

    def __init__(self, url):
        """
        Constructs all the necessary attributes for the JssApi object.

        Parameters
        ----------
            url : str
                The url of the JSS server
        """
        self.url = url
        self.user = ""
        self.pword = ""
        self.enc_creds = ""
        self.bearer_token = ""
        self.token_valid = False

    def get_user_creds(self):
        """Gets user credentials and assigns to attributes"""
        self.user = input("Username: ")
        self.pword = getpass.getpass("Password: ")

    def encode_credentials(self):
        """Formats and returns user/pword attributes as
        a single base64 string to be used in api auth"""
        credential_string = self.user + ":" + self.pword
        byte_string = credential_string.encode("ascii")
        encoded_string = base64.b64encode(byte_string)
        base64_string = encoded_string.decode("ascii")
        self.enc_creds = base64_string

    def get_bearer_token(self):
        """Requests bearer token and sets it as attribute"""
        hdr_line = {"Authorization": "Basic " + self.enc_creds, "Accept": "application/json"}
        resp = requests.post(self.url + "/api/v1/auth/token", headers=hdr_line)
        if resp.status_code == 401:
            print("Auth failed, wrong password?")
            exit()
        json_resp = json.loads(resp.text)
        self.bearer_token = json_resp["token"]

    def validate_token(self):
        """Checks the validity of bearer token and sets attribute accordingly"""
        hdr_line = {"Authorization": "Bearer " + self.bearer_token, "Accept": "application/json"}
        resp = requests.get(self.url + "/api/v1/auth", headers=hdr_line)
        if resp.status_code == 200:
            print("Token is valid")
            self.token_valid = True
        else:
            print("Token is invalid")
            self.token_valid = False

    def invalidate_token(self):
        """Invalidates the bearer token"""
        hdr_line = {"Authorization": "Bearer " + self.bearer_token, "Accept": "application/json"}
        resp = requests.post(self.url + "/api/v1/auth/invalidate-token", headers=hdr_line)
        if resp.status_code == 204:
            self.token_valid = False
            print("Token successfully invalidated")
        elif resp.status_code == 401:
            self.token_valid = False
            print("Token already invalid")
        else:
            print("An unknown error occurred invalidating the token")

    def connect(self):
        """Creates a connection"""
        self.get_user_creds()
        self.encode_credentials()
        self.get_bearer_token()
        self.validate_token()

    def get_resource(self, rsc):
        """Accepts resource path, formats and executes request, and returns results"""
        hdr_line = {"Authorization": "Bearer " + self.bearer_token, "Accept": "application/json"}
        resp = requests.get(self.url + "/JSSResource" + rsc, headers=hdr_line)
        return resp
