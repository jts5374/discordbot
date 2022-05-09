import requests
from requests.auth import HTTPBasicAuth
import os
import time
import json

# uberduck API key
# Key:  pub_xazbjmtvvauyieiixy


auth = HTTPBasicAuth('pub_xazbjmtvvauyieiixy', os.environ['Secret'])
url = 'https://api.uberduck.ai/speak'




def get_audio(tts = None):
    if not tts:
        return 'No text entered'
    global auth, url    
    payload = json.dumps({'speech': f"{tts}", 'voice': "jerry-lawler", 'pace': 1}, indent=4)

    res = requests.post(url, data = payload,  auth=auth)
    uuid = res.json()


    check = f'https://api.uberduck.ai/speak-status'
    params = {'uuid': uuid['uuid']}
    checkresponse = requests.get(check, params = params,  auth=auth).json()

    while checkresponse['finished_at'] is None and checkresponse['failed_at'] is None:
        time.sleep(5)
        checkresponse = requests.get(check, params = params,  auth=auth).json()


    if checkresponse['finished_at']:
        audiourl = checkresponse['path']
        audiodata = requests.get(audiourl)
        file = open('results/audio.wav', 'wb')
        file.write(audiodata.content)
        file.close()
        return 'success'

    elif checkresponse['failed_at']:
        return 'failed'