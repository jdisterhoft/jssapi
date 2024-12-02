"""
#########################################################################################
Notes:    This script will search for applications found on systems matching a keyword.
          It will print out the app name, computer name, site, and last checkin time.
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
user_app = str(input("What app keyword do you want to search for? ")).lower()


# Getting a list of computers
resource = "/computers"
response = api.get_resource(resource)
json_response = json.loads(response.text)
computers = json_response["computers"]


# Grab a list of all computers
computer_ids = []
for computer in computers:
    resource = "/computers/id/" + str(computer["id"])
    response = api.get_resource(resource)
    json_response = json.loads(response.text)
    applications = json_response["computer"]["software"]["applications"]
    # Loop through the computer application list
    for application in applications:
        if user_app in application["name"].lower():
            comp_id = str(computer["id"])
            computer_name = json_response["computer"]["general"]["name"]
            site = json_response["computer"]["general"]["site"]["name"]
            last_checkin = json_response["computer"]["general"]["last_contact_time"]
            print(f"App Name: " + application['name'] + ", Computer Name: " + computer_name +
                  ", Site: " + site + ", Last Checkin: " + last_checkin)


# Cleanup, invalidate the token
api.invalidate_token()
