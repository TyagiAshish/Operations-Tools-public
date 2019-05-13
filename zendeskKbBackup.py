#!/usr/bin/env python2.7
import os
import datetime
import csv
import requests
from base64 import b64encode

credentials = b'<user mail id>/token:<api token>'

zendesk = 'https://support.tetrationcloud.com'
language = 'en-us'

date = datetime.date.today()
backup_path = os.path.join(str(date), language)
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []

endpoint = zendesk + '/api/v2/help_center/{locale}/articles.json'.format(locale=language.lower())
#endpoint = zendesk + '/api/v2/help_center/{locale}/categories/articles.json'.format(locale=language.lower())
#endpoint = zendesk + '/api/v2/help_center/{locale}/sections/articles.json'.format(locale=language.lower())
#endpoint = zendesk + '/api/v2/help_center/{locale}/users/{id}/articles.json'.format(locale=language.lower())
#endpoint = zendesk + '/api/v2/hc/{locale}/incremental/articles.json'.format(locale=language.lower())
# /api/v2/help_center/incremental/articles.json?start_time={start_time}
while endpoint:
    #response = requests.get(endpoint, auth=credentials)
    print(endpoint)
    credentialsin64 = b64encode(credentials).decode("ascii")
    header = { 'Authorization' : 'Basic %s' %  credentialsin64 }
    print(credentialsin64)
    response = requests.get(endpoint, headers=header)
    print(response)
    #response = requests.get(endpoint, headers={'Authorization': 'Basic '  base64.b64encode(bytes(credentials, 'utf-8'))})
    
    if response.status_code != 200:
        print('Failed to retrieve articles with error {}'.format(response.status_code))
        exit()
    data = response.json()

    for article in data['articles']:
        if article['body'] is None:
            continue
        title = '<h1>' + article['title'] + '</h1>'
        filename = '{id}.html'.format(id=article['id'])
        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
            f.write(title + '\n' + article['body'])
        print('{id} copied!'.format(id=article['id']))

        log.append((filename, article['title'], article['author_id']))

    endpoint = data['next_page']

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow( ('File', 'Title', 'Author ID') )
    for article in log:
        writer.writerow(article)
