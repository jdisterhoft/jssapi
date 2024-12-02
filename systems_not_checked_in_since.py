"""
#########################################################################################
Notes:    This script will search all computers for last check in dates and
          print a list of systems that haven't checked in since the number
          of days specified by the user.
          Output is currently: Name, Serial, Site, Last Checkin Day, Num days since checkin
          Requires the 'requests' library
#########################################################################################
"""


import json
import jssapi
from datetime import datetime


jss_url = "https://<jss_fqdn>:8443"


# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()


# Get user keyword
print("This script will check for systems that haven't checked in since a certain number "
      "of days.")
num_days = int(input("How many days since last check in? "))


# Get current date and define list to store results
now = datetime.now()
resulting_list = []


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

    computer_name = json_response["computer"]["general"]["name"]
    serial_number = json_response["computer"]["general"]["serial_number"]
    site = json_response["computer"]["general"]["site"]["name"]
    last_checkin = json_response["computer"]["general"]["last_contact_time"]

    if not last_checkin:
        system = computer_name + "," + site + "," + "PROBLEM RECORD,No Checkin"
        resulting_list.append(system)
    else:
        strip_date = last_checkin.split(" ")
        checkin_date = datetime.strptime(strip_date[0], "%Y-%m-%d")
        delta = now - checkin_date

        if delta.days >= num_days:
            system = computer_name + "," + serial_number + "," \
                     + site + "," + strip_date[0] + "," + str(delta.days)
            resulting_list.append(system)


# Print out the matching list
for item in resulting_list:
    print(item)
print(f"{len(resulting_list)} systems found")


# Cleanup, invalidate the token
api.invalidate_token()
