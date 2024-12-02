"""
#########################################################################################
Notes:    This script will print a list of disabled policies
          Requires the 'requests' library
#########################################################################################
"""

import json
import jssapi

jss_url = "https://<jss_fqdn>:8443"

# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()

# Get a list of policies
resource = "/policies"
response = api.get_resource(resource)
json_response = json.loads(response.text)
policies = json_response["policies"]

# Loop through policies and grab info for each
for policy in policies:
    resource = "/policies/id/" + str(policy["id"])
    response = api.get_resource(resource)
    json_response = json.loads(response.text)

    # Format vars, and if no site assigned, format and print out line
    policy_site = json_response["policy"]["general"]["site"]["name"]
    policy_enabled = json_response["policy"]["general"]["enabled"]
    policy_name = json_response["policy"]["general"]["name"]
    if not policy_enabled:
        line = str(policy["id"]) + "," + str(policy_site) + "," + str(policy_enabled) + "," + policy_name
        print(line)

# Cleanup, invalidate the token
api.invalidate_token()
