This is a library to simplify interacting with the Jamf Pro API with Python,
using bearer token auth.

For testing, this has been run in PyCharm. It should be able to work with any
version of Python3 if you have the 'requests' library installed.

The main.py file has a basic example of how to use it. 
- Import the library
- Set your JSS url/fqdn 
- Create the connection object and connect
- Perform tasks
- Invalidate the token 

```
import jssapi

jss_url = "https://<jss_fqdn>:8443"

# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()

# Enter code here

# Cleanup, invalidate the token
api.invalidate_token()
```

Connection information (username, password, bearer token, etc) get tracked as object attributes. The object has a number of methods- As of right now, these mostly relate to connection and authentication. The primary method you'll most likely want to 
use is the get_resource() method.

This is an example of the get_resource() method. Set your resource (the location after the /JSSResource/ path in the URL), and call the method with it as an argument. Optionally, you can convert the response text to JSON depending on need.

```
resource = "/computers"
response = api.get_resource(resource)
json_response = json.loads(response.text)
```

In addition to main.py and jssapi.py, the other files are examples of how to do certain tasks.

