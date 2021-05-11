#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#O365 teszt fájl

""" 
from O365 import Account, MSGraphProtocol


credentials = ('54f9bd25-fbaa-4e60-acc2-168fbf788ec8', 'jVoS0f-TTzllP63ClIHQ81wU..fC25Fr-5')

protocol = MSGraphProtocol()
#protocol = MSGraphProtocol(defualt_resource='mailto:sharedcalendar@domain.com')
scopes = ['Calendars.Read.Shared']
account = Account(credentials, protocol=protocol)
if account.authenticate(scopes=scopes):
    print('Authenticated!')
""" 

#Get OAUTH token
import requests
import configparser
import json

from O365 import Account, MSGraphProtocol
config = configparser.ConfigParser()

url = "https://login.microsoftonline.com/313470a7-a483-411e-863b-53f70d59dfb3/oauth2/v2.0/token"

payload = "client_id=54f9bd25-fbaa-4e60-acc2-168fbf788ec8&client_secret=jVoS0f-TTzllP63ClIHQ81wU..fC25Fr-5&grant_type=client_credentials&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&undefined="
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "502a2349-570b-4ed5-99fd-5673a9c6075d"
    }
response = requests.request("POST", url, data=payload, headers=headers)
jsonResponse = response.json()

#response = requests.request.json_pretty("POST", url, data=payload, headers=headers)
#response = json.loads(requests.post(url, data=payload, headers=headers))
#token= json.dump(response)
#json.dumps(response,
#token = response['access_token']
#print(response.text)
#print(jsonResponse)
#print(jsonResponse["access_token"])
bearer_token = (jsonResponse["access_token"])

# ez a masodik keres, ez kerdezi le a schedule-t. 
 

url = "https://graph.microsoft.com/v1.0/users/_devnet-race_stage2_targyalo@99999.hu/calendar/getSchedule"

payload = json.dumps({        
    "schedules": ["_devnet-race_stage2_targyalo@99999.hu"],
    "startTime": {
        "dateTime": "2021-04-25T09:00:00",
        "timeZone": "Europe/Budapest"
    },
    "endTime": {
        "dateTime": "2021-04-25T18:00:00",
        "timeZone": "Europe/Budapest"
    },
    "availabilityViewInterval": 60
})

#Ezzel megy, csak nagyon nem szep:

#payload = "{        \r\n    \"schedules\": [\"_devnet-race_stage2_targyalo@99999.hu\"],\r\n    \"startTime\": {\r\n        \"dateTime\": \"2021-04-25T09:00:00\",\r\n        \"timeZone\": \"Europe/Budapest\"\r\n    },\r\n    \"endTime\": {\r\n        \"dateTime\": \"2021-04-25T18:00:00\",\r\n        \"timeZone\": \"Europe/Budapest\"\r\n    },\r\n    \"availabilityViewInterval\": 60\r\n}"

headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer "+bearer_token,
    'cache-control': "no-cache",
    'Postman-Token': "d57d6b57-50d0-4de9-9d29-6e2945b506db"
    }

print(headers)
print(payload)

calendar_response = requests.request("POST", url, data=payload, headers=headers)
calendar_jsonResponse = calendar_response.json()
print(calendar_jsonResponse)
print(calendar_response.text)

#availability = response.json (calendar_response)
lofasz = calendar_jsonResponse["value"]
#["availabilityView"]
print(lofasz[0])
print((lofasz[0]))
pacifaszcsi = lofasz[0]
utalom_az_egesz_xx_szazadot = pacifaszcsi["availabilityView"]
#bearer_token = (jsonResponse["access_token"])
print(utalom_az_egesz_xx_szazadot)