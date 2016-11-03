#! /usr/bin/python
# coding:utf-8

import urllib
import sys
import requests


if len(sys.argv) != 2:
        print("error:argv is not 1")
        exit(1)


url = 'https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY=<my api key>'
f = open(sys.argv[1], 'rb')
data = f.read()
f.close()

files = {"a": open(sys.argv[1], 'rb'), "v":"on"}
r = requests.post(url, files=files)
print(r.json()['text'])
