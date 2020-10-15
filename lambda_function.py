import json
import requests
import sys

def lambda_handler(event, context):
    scheme_id = event.get('scheme_id')
    url = 'https://www.sspcrs.ie/portal/checker/pub/check'
    
    #r = requests.post(url, data = {'schemeId':scheme_id})
    
    client = requests.session()

    # Retrieve the CSRF token first
    client.get(url)  # sets cookie
    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrftoken = client.cookies['csrftoken']
    else:
        # older versions
        csrftoken = client.cookies['csrf']

    data = dict(schemeId=scheme_id, csrfmiddlewaretoken=csrftoken, next='/')
    r = client.post(URL, data=login_data, headers=dict(Referer=URL))
'
    return r.text