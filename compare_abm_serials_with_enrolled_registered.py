"""
#########################################################################################
Notes:    This script will take a CSV exported from ABM, and compare against all serials
          in the JSS. It will return a list of systems that are in ABM, but not in the JSS

          To use, when asked, feed this script a csv export from ABM, no header line needed.
          This will work with/for Mobile Devices as well.
#########################################################################################
"""

import json
import jssapi
import csv

jss_url = "https://<jss_fqdn>:8443"

# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()

# Get CSV
csv_file = str(input("Enter the full path of your CSV file? "))
serials_in_abm = []
with open(csv_file) as numbers:
    csv_reader = csv.reader(numbers)
    for row in enumerate(csv_reader):
        serials_in_abm.append(row[1][0])

# Var to store JSS serial numbers
serials_in_jss = []

# Get a list of computers
resource = "/computers"
response = api.get_resource(resource)
json_response = json.loads(response.text)

# Append all serials to a list
computers = json_response["computers"]
for computer in computers:
    resource = "/computers/id/" + str(computer["id"])
    response = api.get_resource(resource)
    json_response = json.loads(response.text)

    # Get serial from system specified by 'id'
    serial = json_response["computer"]["general"]["serial_number"]
    serials_in_jss.append(serial)

# Getting a mobile devices
resource = "/mobiledevices"
response = api.get_resource(resource)
json_response = json.loads(response.text)

# Append all serials to a list
mobile_devs = json_response["mobile_devices"]
for dev in mobile_devs:
    resource = "/mobiledevices/id/" + str(dev["id"])
    response = api.get_resource(resource)
    json_response = json.loads(response.text)

    # Get serial from system specified by 'id'
    serial = json_response["mobile_device"]["general"]["serial_number"]
    serials_in_jss.append(serial)

# Compare and print list
print("The following serial numbers are in ABM, but not found in the JSS:")
for num in serials_in_abm:
    if num not in serials_in_jss:
        print(num)

# Cleanup, invalidate the token
api.invalidate_token()
