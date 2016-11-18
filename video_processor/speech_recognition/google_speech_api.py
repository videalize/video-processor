import sys
import json
import urllib.parse
import urllib.request
import os

apikey = os.environ['GOOGLE_SPEECH_API_KEY']
endpoint = 'http://www.google.com/speech-api/v2/recognize'
query_string = {'output': 'json', 'lang': 'ja-JP', 'key': apikey}

url = '{0}?{1}'.format(endpoint, urllib.parse.urlencode(query_string))

headers = {'Content-Type': 'audio/l16; rate=16000'}
voice_data = open(sys.argv[1], 'rb').read()

request = urllib.request.Request(url, data=voice_data, headers=headers)
response = urllib.request.urlopen(request).read()

# 出力が複数行のJSONなので，不要そうなものを削除
for line in response.decode('utf-8').split():
    if not line:
        continue
    else:
        res = json.loads(line)
        if res['result'] == []:
            continue
        else:
            print(res)
