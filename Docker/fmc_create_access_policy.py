#!/usr/bin/env python
"""Create an FMC Access Policy and Rules.

Copyright (c) 2018-2019 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import sys
from pathlib import Path
from pprint import pformat
import requests
from crayons import blue, green
import configparser
import json
import datetime
import os
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'volume', 'config.cfg'))


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))
sys.path.insert(0, str(here))

from fmc_requests import fmc_authenticate, fmc_post, fmc_get  # noqa


# Authenticate with FMC
fmc_authenticate()


# Create an Access Policy
print(blue("\n==> Creating a new Access Policy on FMC"))

access_policy = {
    "type": "AccessPolicy",
    "name": config['FMC']['POLICY_NAME'],
    "description":"DevNet Race policy",
    "defaultAction":{"action": "BLOCK"},
}
created_policy = ''
policy_exist = ''
policycheck = fmc_get("policy/accesspolicies")
for item in policycheck['items']:
    if item['name'] == config['FMC']['POLICY_NAME']:
      policy_exist = item['name']
      policy_id = item['id']
      created_policy == fmc_get("policy/accesspolicies")['items']
            

if policy_exist == '':      
  created_policy = fmc_post("policy/accesspolicies", access_policy)

policy = fmc_get("policy/accesspolicies")
policy_id = ''
IN_zone_id = ''
OU_zone_id = ''
for item in policy['items']:
    if item['name'] == config['FMC']['POLICY_NAME']:
        policy_id = item['id']

securityzones = fmc_get("object/securityzones")
for item in securityzones['items']:
    if item['name'] == 'INSIDE':
        IN_zone_id = item['id']


print(json.dumps(securityzones,indent=4, sort_keys=True))

for item in securityzones['items']:
    if item['name'] == 'OUTSIDE':
        OU_zone_id = item['id']
        print(OU_zone_id)

print(
    green('Policy Created:'),
    pformat(access_policy),
    sep="\n",
)
# Create an Access Rule in the new policy
print(blue("\n==> Creating an Access Rule in the new policy"))
access_rule = {
  "sourceZones": {
    "objects": [
      {
        "name": "INSIDE",
        "id": IN_zone_id, #"037f5838-6412-11e8-a51d-e68d36fe956d",
        "type": "SecurityZone"
      }
    ]
  },
  "destinationZones": {
    "objects": [
      {
        "name": "OUTSIDE",
        "id": OU_zone_id, #"3abf6934-f2c4-11e6-adc9-8793d8cc0fcc",
        "type": "SecurityZone"
      }
    ]
  },
  "type": "AccessRule",
  "action": "ALLOW",
  "name": config['FMC']['POLICY_NAME'],
  "enabled": True
}
#print(created_policy['id'])
print(access_rule)
created_rule = fmc_post("policy/accesspolicies/"+policy_id+"/accessrules", access_rule)

print(
    green("Access Rule Created:"),
    pformat(created_rule),
    sep="\n",
)
#Deployment request a demo környezetünkben nincs
#json_data = {
#            "type": "DeploymentRequest",
#            "forceDeploy": True,
#            "ignoreWarning": True,
#            "version": str(int(1000000 * datetime.datetime.utcnow().timestamp())),
#            "deviceList": [],
#        }
#fmc_post("deployment/deploymentrequests",json_data)
