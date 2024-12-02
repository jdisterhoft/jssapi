"""
#########################################################################################
Notes:    This script will retrieve a list of all computer IDs in the JSS.
          Requires the 'requests' library
#########################################################################################
"""

import json
import jssapi

jss_url = "https://<jss_fqdn>:8443"

# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()

# Getting a list of computers
resource = "/computers"
response = api.get_resource(resource)
json_response = json.loads(response.text)

# Print out list of computer IDs
computers = json_response["computers"]
for computer in computers:
    print(computer["id"])

# Cleanup, invalidate the token
api.invalidate_token()
