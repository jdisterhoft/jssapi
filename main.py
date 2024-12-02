"""
#########################################################################################
Notes:    This uses the jssapi library to assist in bearer token auth for the Jamf Pro
          api. This file is a template.
          Requires the 'requests' library
#########################################################################################
"""


import json
import requests
import jssapi


jss_url = "https://<jss_fqdn>:8443"


# Create an instance which will retrieve bearer token and create connection
api = jssapi.JssApi(jss_url)
api.connect()


# Enter code here


# Cleanup, invalidate the token
api.invalidate_token()