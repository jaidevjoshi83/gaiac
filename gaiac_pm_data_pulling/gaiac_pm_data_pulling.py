#!/usr/bin/env python


import argparse
import logging
from base64 import urlsafe_b64encode
from html import escape
from urllib.parse import urljoin
import requests
import urllib.request
import json

def get_file_list(ip):

    url = "%s/api/list-files"%(ip)

    with urllib.request.urlopen(url) as response:
        data = response.read()
        file_list = json.loads(data)

    return file_list


def simulate_dynamic_options(ip):
    try:
        rval = []

        api_data = {ip:{

        }}

        for i in get_file_list(ip):
            api_data[ip][i] = ip+'/api/download/'+i

        ul = []
        for dataset, url in api_data[ip].items():
  
            ul.append({
                'name': dataset,
                'value': url,
                'options': [],
                'selected': False
            })
        
        return ul
    except Exception as e:
        # Handle any potential errors
        return [{
            'name': escape(str(e)),
            'value': 'ERROR',
            'options': [],
            'selected': False
        }]

if __name__ == '__main__':

    print(simulate_dynamic_options('http://iotprojects.ddns.net'))
