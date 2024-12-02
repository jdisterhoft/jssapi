"""
#########################################################################################
Notes:    Running this will return a list of policies with no site assigned
          (site ID is '-1'). Is set to return 'enabled' policies. Output is
          <policy_id>, <policy_site_id>, <policy_name>

          NOTE- As of right now, it's returning lines of junk/unknown policies.
          They are named like this: "2015-07-06 at 10:44 AM | user | 1 Computer"
          Initially just ignoring.
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
    policy_site_id = json_response["policy"]["general"]["site"]["id"]
    policy_enabled = json_response["policy"]["general"]["enabled"]
    policy_name = json_response["policy"]["general"]["name"]
    if (policy_site_id == -1) and policy_enabled:
        line = str(policy["id"]) + "," + str(policy_site_id) + "," + policy_name
        print(line)


# Cleanup, invalidate the token
api.invalidate_token()
