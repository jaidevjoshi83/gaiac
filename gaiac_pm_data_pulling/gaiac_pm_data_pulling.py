#!/usr/bin/env python


import argparse
import logging
from base64 import urlsafe_b64encode
from html import escape
from urllib.parse import urljoin
import requests

log = logging.getLogger("tools.iuc.data_managers.data_manager_refgenie_pull")

import urllib.request
import json

def get_file_list(ip):

    url = "%s/list-files"%(ip)

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
            # print("http://"+ip+'/download/'+i)
            api_data[ip][i] = ip+'/download/'+i


        ul = []
        for dataset, url in api_data[ip].items():
  
            ul.append({
                'name': dataset,
                'value': url,
                'options': [],
                'selected': False
            })
        
        # for urlname, genomes in api_data.items():
        #     # URL-safe base64 encoding for the URL name
        #     urlname_64 = urlname
        #     ul = []
        #     for genome, assets in genomes.items():
        #         al = []

        #         ul.append({
        #             'name': genome,
        #             'value': genome,
        #             'options': [],
        #             'selected': False
        #         })

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

    simulate_dynamic_options('http://192.168.1.202:8080')

#    for i in simulate_dynamic_options('192.168.1.202:8080')[0]['options']:
#        print(i)
    #    print(i)
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-n', '--names', dest='names', action='store', default=None, help='Table names to reload')
    # parser.add_argument('-u', '--url', dest='url', action='store', default=None, help='Base url for reload')
    # parser.add_argument('-k', '--key', dest='key', action='store', default=None, help='Galaxy API Key')
    # parser.add_argument('-g', '--graceful', dest='graceful', action='store_true', help='Fail gracefully')

    # args = parser.parse_args()
    # try:
    #     if not args.names:
    #         tables = requests.get(urljoin(args.url, "api/tool_data"), params={'key': args.key}).json()
    #         args.names = [d.get('name') for d in tables]
    #     for name in args.names:
    #         print(requests.get(urljoin(args.url, "api/tool_data/%s/reload" % (name)), params={'key': args.key}).json())
    # except Exception as e:
    #     if args.graceful:
    #         print("Failed to reload data tables:\n%s" % (e))
    #     else:
    #         raise e
