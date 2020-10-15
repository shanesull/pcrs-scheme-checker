import json
import requests
import sys
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    scheme_id = event.get('scheme_id')
    url = 'https://www.sspcrs.ie/portal/checker/pub/check'
    
    #r = requests.post(url, data = {'schemeId':scheme_id})
    
    client = requests.session()

    # Retrieve the CSRF token first
    c = client.get(url)  # sets cookie
    #print ('Body: ' + c.text)
    #print (c.cookies)
    
    soup = BeautifulSoup(c.text, 'html.parser')
    csrftoken = soup.find('input', {'name': '_csrf'}).get('value')
    print(csrftoken)

    data = dict(schemeId=scheme_id, _csrf=csrftoken, next='/')
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    r = client.post(url, data=data, headers=dict(Referer=url))
    soup2 = BeautifulSoup(r.text, 'html.parser')
    span = soup2.select('.lead')
    elligibilty =  span[1].getText().strip('\n').lower()
    scheme = soup2.find(text='Scheme Type:').parent.findNext('div').getText().strip('\n')
    dob = soup2.find(text='Date of Birth:').parent.findNext('div').getText().strip('\n')
    start_date = soup2.find(text='Eligibility Start Date:').parent.findNext('div').getText().strip('\n')
    end_date = soup2.find(text='Eligibility End Date:').parent.findNext('div').getText().strip('\n')
    scheme_ref = soup2.find(text='Scheme Id:').parent.findNext('div').getText().strip('\n')

    print (elligibilty,scheme, dob,start_date,end_date,scheme_ref)
    #return elligibilty.strip('\n')
    
    pcrs_response = dict(
        status=elligibilty,
        scheme=scheme,
        elligibilty_start_date=start_date,
        elligibilty_end_date=end_date,
        date_of_birth=dob
    )
    return pcrs_response