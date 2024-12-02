"""
#########################################################################################
Notes:    This script will use the api to check for all packages that aren't attached a
          policy, and will return a list.
          Requires the 'requests' library
#########################################################################################
"""


import json
import jssapi


jss_url = "https://<jss_fqdn>:8443"


# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()

print("Referencing packages against policies. This can take a while...")


# Get all packages
resource = "/packages"
response = api.get_resource(resource)
json_response = json.loads(response.text)


# Create a list of package IDs
package_ids = []
for package in json_response["packages"]:
    package_ids.append(package["id"])


# Get all policies
resource = "/policies"
response = api.get_resource(resource)
json_response = json.loads(response.text)


# Create a list of policy IDs
policy_ids = []
package_ids_in_use = []
for policy in json_response["policies"]:
    policy_ids.append(policy["id"])


# Get a list of package IDs that are attached to policies
for p_id in policy_ids:
    resource = "/policies/id/" + str(p_id)
    response = api.get_resource(resource)
    json_response = json.loads(response.text)
    attached_packages = json_response["policy"]["package_configuration"]["packages"]

    if attached_packages:
        for package in attached_packages:
            package_ids_in_use.append(package["id"])


# Reference package IDs against IDs found in policies
unattached_packages = []
for p_id in package_ids:
    if p_id not in package_ids_in_use:
        unattached_packages.append(p_id)


# Retrieve the name of each package not found on the attached list
policy_names = []
for p_id in unattached_packages:
    resource = "/packages/id/" + str(p_id)
    response = api.get_resource(resource)
    json_response = json.loads(response.text)
    package_name = json_response["package"]["name"]
    policy_names.append(package_name)


print("Packages that are not attached to policies are:")
for p in policy_names:
    print(p)


# Cleanup, invalidate the token
api.invalidate_token()
