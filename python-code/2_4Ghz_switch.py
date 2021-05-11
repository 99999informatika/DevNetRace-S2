#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Stil Consulting Ltd. very important magic app for Meraki app
#O365 megbeszélések lehívása API segítségével, pip install o365 ütemezet első meeting időpontban elindítja
#Ha meeting található, akkor a meeting időpontjában elindítja a 2,4 Ghz-es wifit Üzenet küld róla az IT staffnak Webexen
#17:59:59 után lekapcsolja a Wifit
import meraki
import configparser
import requests
import schedule
import time
from O365 import Account, MSGraphProtocol
import json
from datetime import datetime
import os
import time


config = configparser.ConfigParser()
def merakiorg_id():
    config.read("config.cfg")
    # Defining your API key as a variable in source code is not recommended
    API_KEY = config["MERAKI"]["MERAKI_DASHBOARD_API_KEY"]
    # Instead, use an environment variable as shown under the Usage section
    # @ https://github.com/meraki/dashboard-api-python/
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.organizations.getOrganizations()
    for org in response:
        org_id= org["id"]
    
    return org_id

def meraki_network(organization_id):
    config.read("config.cfg")
    # Defining your API key as a variable in source code is not recommended
    API_KEY = config["MERAKI"]["MERAKI_DASHBOARD_API_KEY"]
    # Instead, use an environment variable as shown under the Usage section
    # @ https://github.com/meraki/dashboard-api-python/

    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.organizations.getOrganizationNetworks(
        organization_id, total_pages='all'
    )
    for net in response:
        if net["name"] == config["MERAKI"]["NET_NAME"]:
            net_id= net["id"]
    
    return net_id

def meraki_rfprofile(network_id):
    config.read("config.cfg")
    # Defining your API key as a variable in source code is not recommended
    API_KEY = config["MERAKI"]["MERAKI_DASHBOARD_API_KEY"]
    # Instead, use an environment variable as shown under the Usage section
    # @ https://github.com/meraki/dashboard-api-python/
    rfp_id = ''
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.wireless.getNetworkWirelessRfProfiles(
        network_id
    )
    for rfprofile in response:
        rfp_id = rfprofile["id"]
    
    #print(rfp_id)
    
    return rfp_id

def meraki_rfpcheck(network_id, rf_profile_id):
    config.read("config.cfg")
    # Defining your API key as a variable in source code is not recommended
    API_KEY = config["MERAKI"]["MERAKI_DASHBOARD_API_KEY"]
    # Instead, use an environment variable as shown under the Usage section
    # @ https://github.com/meraki/dashboard-api-python/
    rfpbands = ''
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.wireless.getNetworkWirelessRfProfile(
    network_id, rf_profile_id
    )
    #print(response)
    rfpbands = response['apBandSettings']['bandOperationMode']
    #print(rfpbands)
    return rfpbands
#Initialize Meraki to dual mode
def set_band(band, network_id, rfp_id):
    API_KEY = config["MERAKI"]["MERAKI_DASHBOARD_API_KEY"]

    url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/rfProfiles/{rfp_id}"
    #print(url)
    payload = '''{
        "apBandSettings": { "bandOperationMode": ''' + band + ''' },
        "twoFourGhzSettings": {},
        "fiveGhzSettings": {},
        "bandSelectionType": "ap",
        "minBitrateType": "ssid"
    }'''

    #print(payload)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": API_KEY
    }

    response = requests.request('PUT', url, headers=headers, data = payload)
    #print(response)
    return response.text.encode('utf8')

def fiveghzonly():
    band = '"5ghz"'
    org_id = merakiorg_id()
    network_id = meraki_network(org_id)
    rfp_id = meraki_rfprofile(network_id)
    set_band(band, network_id , rfp_id)
    return band
def dualband():
    band = '"dual"'
    org_id = merakiorg_id()
    network_id = meraki_network(org_id)
    rfp_id = meraki_rfprofile(network_id)
    set_band(band, network_id , rfp_id)
    return band

def o365calendar_check():
    ### O365 oauth ------- BEGIN ------
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    url = "https://login.microsoftonline.com/"+config['O365']['TENANT_ID']+"/oauth2/v2.0/token"
    payload = "client_id="+config['O365']['CLIENT_ID']+"&client_secret="+config['O365']['CLIENT_SECRET']+"&grant_type=client_credentials&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&undefined="
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        #'Postman-Token': "502a2349-570b-4ed5-99fd-5673a9c6075d"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    jsonResponse = response.json()
    bearer_token = (jsonResponse["access_token"])
    ### ------- END ------
    ### O365 Calendar check ------ BEGIN ------
    url = "https://graph.microsoft.com/v1.0/users/"+config['O365']['ROOM_NAME']+"/calendar/getSchedule"
    payload = json.dumps({        
        "schedules": [config['O365']['ROOM_NAME']],
        "startTime": {
            "dateTime": date+"T09:00:00",
            "timeZone": config['O365']['TIME_ZONE']
        },
        "endTime": {
            "dateTime": date+"T18:00:00",
            "timeZone": config['O365']['TIME_ZONE']
        },
        "availabilityViewInterval": 60
    })
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+bearer_token,
        'cache-control': "no-cache",
        #'Postman-Token': "d57d6b57-50d0-4de9-9d29-6e2945b506db"
        }

    #print(headers)
    #print(payload)

    calendar_response = requests.request("POST", url, data=payload, headers=headers)
    calendar_jsonResponse = calendar_response.json()
    #print(calendar_jsonResponse)
    #print(calendar_response.text)

    #availability = response.json (calendar_response)
    calendar_list = calendar_jsonResponse["value"]
    #["availabilityView"]
    #print(lofasz[0])
    #print((lofasz[0]))
    calendar_dict = calendar_list[0]
    availabilityView_var = calendar_dict["availabilityView"]
    #bearer_token = (jsonResponse["access_token"])
    #print(utalom_az_egesz_xx_szazadot)

    #### ------ END ------
    #Very important magic
    #starttime = "09:00"
    return availabilityView_var

def hourly_check():
    org_id = merakiorg_id()
    network_id = meraki_network(org_id)
    rfp_id = meraki_rfprofile(network_id)
    bandcheck=meraki_rfpcheck(network_id, rfp_id)
    start = o365calendar_check()
    print(start)
    print(bandcheck)
    now = datetime.now()
    tt = now.strftime('%H:%M')
    print(tt)
    if bandcheck != 'dual':
        if start != '000000000':
            if tt < '18:00':
                bandcheck = dualband()
    return

hourly_check()


schedule.every(1).minute.do(hourly_check)
schedule.every().day.at("18:00").do(fiveghzonly)

while True:
    schedule.run_pending()
    time.sleep(1)