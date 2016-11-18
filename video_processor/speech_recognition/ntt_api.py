#! /usr/bin/python
# coding:utf-8

import urllib
import sys
import requests
import os

if len(sys.argv) != 2:
        print("error:argv is not 1")
        exit(1)

apikey = os.environ['NTT_SPEECH_API_KEY']
url = 'https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={0}'.format(apikey)
f = open(sys.argv[1], 'rb')
data = f.read()
f.close()

files = {"a": open(sys.argv[1], 'rb'), "v":"on"}
r = requests.post(url, files=files)
print(r.json()['text'])
