#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Stil Consulting Ltd. very important magic app for Random guest user generator
#Készíünk egy BOT-ot ami:
#A. generál egy random usert-t és hozzá egy FMC szabályt és erről szóló infokat (guest username és password) elküldi Webex teamsen az érintett kollégának

import configparser
import requests
import json
from webexteamsbot import TeamsBot
import os
from fmc_requests import fmc_get, fmc_authenticate
import schedule
import time

config = configparser.ConfigParser()

def quick_guest(username):
    config.read( 'config.cfg')
    server = config['STIL_CENTER']['STIL_CENTER_URL']
    url = f"https://{server}/stil-ise/api/quickguest"
    print(username)
    payload = '' 
    if username != '':
        payload = '{"userName": "'+username+'"}'

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic OTk5OTk6dmIzNDFi'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    #print(response.text)
    return response.text

def do_something(incoming_msg):
    """
    Sample function to do some action.
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    guest_user = quick_guest(name)
    print(guest_user)
    gu = guest_user.split(',')
    usr = gu[0].split(':')
    user = usr[1].replace('"', '')
    pswd = gu[1].split(':')
    passwd = pswd[1].replace('"', '')
    password = passwd.replace('}', '')
    fmc_policy = 0
    fmc_authenticate()
    test_fmc = fmc_get('policy/accesspolicies')
    for item in test_fmc['items']:
        if item['name'] == config['FMC']['POLICY_NAME']:
            fmc_policy = 1

    if fmc_policy == 0:
        os.system('python3 fmc_create_access_policy.py')
        os.system('rm *.log')
        return  "I did what you said - {}".format(incoming_msg.text) + "\n Username: " + user + "\nPassword: " + password
    else:
        os.system('rm *.log')
        return  "I did what you said - {}".format(incoming_msg.text) + "\n Username: " + user + "\nPassword: " + password
    

#quick_guest(name)


config.read( 'config.cfg')
bot_email = config["Webex"]["TEAMS_BOT_EMAIL"]
teams_token = config["Webex"]["TEAMS_BOT_TOKEN"]
bot_url = config["Webex"]["TEAMS_BOT_URL"]
bot_app_name = config["Webex"]["TEAMS_BOT_APP_NAME"]


bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    webhook_resource_event=[{"resource": "messages", "event": "created"},
                            {"resource": "attachmentActions", "event": "created"}]
)
name = ''

bot.add_command("/quick_guest", "help for do something", do_something)



if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000, debug=True)
    schedule.every().day.at("18:00").do(os.system('/usr/bin/python3 fmc_clean_access_policy.py'))
    while True:
        schedule.run_pending()
        time.sleep(1)