"""
#########################################################################################
Notes:    Running this will return a list of config profiles with no site assigned
          (site ID is '-1'). Output is: <policy_id>,<policy_site_id>,<policy_name>
#########################################################################################
"""


import json
import jssapi


jss_url = "https://<jss_fqdn>:8443"


# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()


# Get list of config profiles
resource = "/osxconfigurationprofiles"
response = api.get_resource(resource)
json_response = json.loads(response.text)
profiles = json_response["os_x_configuration_profiles"]


# Loop through profiles, and grab info for each
for profile in profiles:
    resource = "/osxconfigurationprofiles/id/" + str(profile["id"])
    response = api.get_resource(resource)
    json_response = json.loads(response.text)

    profile_site_id = json_response["os_x_configuration_profile"]["general"]["site"]["id"]
    profile_name = json_response["os_x_configuration_profile"]["general"]["name"]

    # Format and print out if it isn't assigned to a site
    if profile_site_id == -1:
        line = str(profile["id"]) + "," + str(profile_site_id) + "," + profile_name
        print(line)


# Cleanup, invalidate the token
api.invalidate_token()
