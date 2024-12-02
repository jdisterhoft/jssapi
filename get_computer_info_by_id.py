"""
#########################################################################################
Notes:    This script will get and print computer info based on ID.
          Requires the 'requests' library
#########################################################################################
"""

import json
import jssapi

jss_url = "https://<jss_fqdn>:8443"

# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()

# Retrieve computer record
# Example ID here, replace with own
computer_id = "2974"
resource = "/computers/id/" + str(computer_id)
response = api.get_resource(resource)
json_response = json.loads(response.text)

# Get name, site, and os version from system specified by 'id'
computer_name = json_response["computer"]["general"]["name"]
site = json_response["computer"]["general"]["site"]["name"]
os_version = json_response["computer"]["hardware"]["os_version"]
print(computer_name, site, os_version)

# Cleanup, invalidate the token
api.invalidate_token()
