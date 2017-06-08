import requests
import time
import sys
from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# number of seconds between each check
delay = 3

# Credentials
payload = {
    'username': 'rvil',
    'password': '102704'
}

# A dictionary of results
d = {}
# The index used when appending to the dict
row_key = 0

app = Flask(__name__)

with requests.Session() as s:
    r = s.post('http://10.66.31.153', params=payload, allow_redirects=False)
    print(r.status_code)

    cookie = r.cookies


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/suite')
    def suite():
        return render_template('suite.html', parent_dict=d)


    @app.route('/getReadings')
    def getReadings():
        # want to modify a variable outside the scope of this route
        global row_key
        print("logging in...")
        #        print(r.cookies['PHPSESSID'])

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

        # # start automation
        # r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/setCommand?commandIndex=12',
        #           cookies=cookie)
        # print(r.url)
        # print(r.status_code)

        #get readings
        r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/getVals?from=0', cookies=cookie)
        print(r.json())
        print(r.status_code)

        # insert a new entry in the data dictionary with the results pulled from the json response
        d[row_key] = r.json()

        # print the new dictionary with the appended response
        # print(d)

        # Delay
        time.sleep(1)
        # increment for next time it is called
        row_key += 1
        # return the data dictionary as a dataframe (to be passed into the jinja templates)
        return jsonify(d)


    @app.route('/stopRig')
    def stopRig():
        r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/setCommand?commandIndex=11')
        print(r.url)
        print('Stopping Autorun - repsonse: ' + str(r.status_code))
        r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/setCommand?commandIndex=41')
        print(r.url)
        print('Setting calibration to zero - repsonse: ' + str(r.status_code))
        r = s.get('http://10.66.31.153/session/finish')
        print(r.url)
        print('Exiting Rig - repsonse: ' + str(r.status_code))
        r = s.get('http://10.66.31.153/index/logout')
        print(r.url)
        print('logging out - response' + str(r.status_code))
        return render_template('index.html')


    @app.route('/pause')
    def pause():
        r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/setCommand?commandIndex=11')
        print(r.url)
        print('Stopping Autorun - repsonse: ' + str(r.status_code))
        return render_template('suite.html', parent_dict=d)


    @app.route('/resume')
    def resume():
        r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/setCommand?commandIndex=12',
                  cookies=cookie)
        print(r.url)
        print(r.status_code)

        return ('', 204)


    if __name__ == '__main__':
        app.run(debug=False, port=3037,
                host="0.0.0.0")  # =========================================================================================================================
# This snippet, when run outside of the Flask framework, will connect to Sahara and keep pulling the readings from the rigs
# =========================================================================================================================
# with requests.Session() as s:
#     print("logging in...")
#     r = s.post('http://10.66.31.153', params=payload, allow_redirects = False)
#     print(r.status_code)
#
#     cookie = r.cookies
#     print(r.cookies['PHPSESSID'])
#
#     print("logged in!")
# #    print(r.text)
#
#     r = s.get('http://10.66.31.153/queue/info?id=24', cookies=cookie)
#     print(r.url)
#     print(r.status_code)
# #    print(r.cookies['PHPSESSID'])
#
#     r = s.get('http://10.66.31.153/queue/queue?id=24', cookies=cookie)
#     print(r.url)
#     print(r.status_code)
# #    print(r.cookies['PHPSESSID'])
#
# try:
#     while(1):
#         print("Checking...")
#         time.sleep(delay)
#         r = s.get('http://10.66.31.153/primitive/mapjson/pc/PendulumRigController/pa/getVals?from=0', cookies=cookie)
#         print(r.json())
#         print(r.status_code)
# except KeyboardInterrupt:
#     r=s.get('http://10.66.31.153/session/finish')
#     print(r.url)
#     print(r.status_code)
#     r=s.get('http://10.66.31.153/index/logout')
#     print(r.url)
#     print(r.status_code)
