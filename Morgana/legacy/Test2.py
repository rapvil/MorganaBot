##isolated bot program -- separated from Flask
##the 'ghost user' bug came from this prototype, so use with caution!

import requests
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

delay = 3

# Credentials
payload = {
    'username': 'rvil',
    'password': '102704'
}

columns = ["Length", "Watchdog", "StepPV", "ProcState", "Period", "TargetLength", "StepSP", "ProcMode"]
df = pd.DataFrame(columns=columns)
test = {'Length': 280, 'Watchdog': 0, 'StepPV': 0, 'ProcState': 2, 'Period': 0, 'TargetLength': 280, 'StepSP': 0, 'ProcMode': 1}
print('Type of test'+str(type(test)))

d={}
row_key = 0

#=========================================================================================================================
#This snippet, when run outside of the Flask framework, will connect to Sahara and keep pulling the readings from the rigs
#=========================================================================================================================
with requests.Session() as s:
    print("logging in...")
    r = s.post('http://10.66.31.153', params=payload, allow_redirects = False)
    print(r.status_code)

    cookie = r.cookies
    print(r.cookies['PHPSESSID'])

    print("logged in!")
#    print(r.text)

    r = s.get('http://10.66.31.153/queue/info?id=24', cookies=cookie)
    print(r.url)
    print(r.status_code)
#    print(r.cookies['PHPSESSID'])

    r = s.get('http://10.66.31.153/queue/queue?id=24', cookies=cookie)
    print(r.url)
    print(r.status_code)
#    print(r.cookies['PHPSESSID'])

try:
    while(1):
        print("Checking...")
        time.sleep(delay)
        r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/getVals?from=0', cookies=cookie)
        print(r.json())
        print(r.status_code)
        print('Type of response is ' + str(type(r.json())))
        json_str = r.json()
        print('Type of r.json is '+ str(type(r.json)))

        d[row_key] = r.json()
        print(d)
        row_key+=1

#        data = json.load(r.json())
except KeyboardInterrupt:
    r=s.get('http://10.66.31.153/session/finish')
    print(r.url)
    print(r.status_code)
    r=s.get('http://10.66.31.153/index/logout')
    print(r.url)
    print(r.status_code)
