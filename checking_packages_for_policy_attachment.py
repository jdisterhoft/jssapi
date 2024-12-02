"""
#########################################################################################
Notes:    This script will use a search word to retrieve package IDs of matches. Then, you
          can enter the package ID to find out what policies it's attached to.
          Requires the 'requests' library
#########################################################################################
"""


import json
import jssapi


jss_url = "https://<jss_fqdn>:8443"


# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()


# Get user keyword
user_package = str(input("What package keyword do you want to search for? ")).lower()


# Get all packages
resource = "/packages"
response = api.get_resource(resource)
json_response = json.loads(response.text)


# Create a dict of packages that match the keyword
matching_packages = {}
for package in json_response["packages"]:
    if user_package in package["name"].lower():
        matching_packages[package["id"]] = package["name"]


# Show matching packages, ask to select one by ID
print("The matching packages were found:")
for p_key, p_value in matching_packages.items():
    print(f"ID: {p_key}   Name: {p_value}")


user_selection = int(input("Enter the ID of the package you want to search for: "))
print("Please wait, checking can take a while...")


# Get all policies
resource = "/policies"
response = api.get_resource(resource)
json_response = json.loads(response.text)


# Create a list of policy IDs
policy_ids = []
for policy in json_response["policies"]:
    policy_ids.append(policy["id"])


# Get a list of package IDs that are attached to policies
policies_with_id = []
for p_id in policy_ids:
    resource = "/policies/id/" + str(p_id)
    response = api.get_resource(resource)
    json_response = json.loads(response.text)
    attached_packages = json_response["policy"]["package_configuration"]["packages"]
    if attached_packages:
        for package in attached_packages:
            if package["id"] == user_selection:
                policies_with_id.append(json_response["policy"]["general"]["name"])


print(f"The package {matching_packages[user_selection]} has been found on {len(policies_with_id)} policies")
print(f"They are: ")
print(policies_with_id)


# Cleanup, invalidate the token
api.invalidate_token()
