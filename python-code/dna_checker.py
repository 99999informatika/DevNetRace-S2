#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# devnetrace_stage2
# /python-code/dna_checker.py
# Stil Consulting Ltd. very important magic app
# API kezelo szoftverrel valahogy majd kommunikal (poll vagy push) es a kapott informaciot feldolgozza
# Ha a kapott info alapjan ugy hatarozzuk meg hogy problema van akkor uzenetet kuldunk Webexen az IT staffnak
import json
import requests
from flask import Flask, request, render_template, redirect, url_for
import configparser
config = configparser.ConfigParser()

def send_message(message):
    config.read("config.cfg")
    if config["Webex"]["ACCESS_TOKEN"] != '':
        url = "https://webexapis.com/v1/webhooks/incoming/" + config["Webex"]["ACCESS_TOKEN"]
        texttowebex =  message
        payload = {
        'text': texttowebex
        }
        files = [

        ]
        headers = {
        'Accept': 'application/json'
        }
        responsewebex = requests.request("POST", url, headers=headers, data = payload, files = files)
        
        if responsewebex.status_code == 204:
            webex_status = str(responsewebex.status_code) + '\t ' + 'OK'
        else:
            webex_status = str(responsewebex.status_code) + '\t' + 'Error'

        return
    else:
        webex_status = 'Not Provided'
        
        return

def dna_ngrok_url():
    config.read("config.cfg")
    request_headers = {
            "Content-Type" : "application/json",
            "Accept" : "application/json",
            'Authorization': 'Basic OTk5OTk6dmIzNDFi'
        }
    host = config["STIL_CENTER"]["STIL_CENTER_URL"]
    ngrok_url = config["STIL_CENTER"]["NGROK_URL"]
    request_body = "{\n    \"webhook\": \"https://"+ngrok_url+"\"\n}"
    print(request_body)
    if host != '':
        url = f"https://{host}" + "/stil-dnac/api/webhook"
        #print(url)
        try:
            response = requests.put(url, headers=request_headers, data=request_body, verify=False)
            #print(response)
            API_CENTER = 200
        except:
            API_CENTER = 404
    return API_CENTER

app = Flask(__name__)
state=dna_ngrok_url()
print(state)

@app.route('/', methods=['POST'])
def form_post():
    request_data = request.get_json()
    #print(request_data)
    eventId = request_data['eventId']
    #print(eventId)
    description = request_data['description']
    #print(description)
    name = request_data['name']
    #print(name)
    details_issue = request_data['details']['Assurance Issue Details']
    #print(details_issue)
    details_ip = request_data['details']['Device']
    #print(details_ip)
    details_status = request_data['details']['Assurance Issue Status']
    #print(details_status)
    result = str(eventId) + '\n' + str(description) + '\n' + str(name) + '\n' + str(details_issue) + '\n' + str(details_ip) + '\n' + details_status
    print(result)
    send_message(result)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0' , port=8081 )