
"""
@author: Felipe Dale Figeman

"""
import keyboard
import flask
from flask import Flask, request, redirect, render_template
import requests
import time
import pyqrcode
#download ngrok from https://ngrok.com/download
app = Flask(__name__)

def geturl():
    resp = requests.get('http://127.0.0.1:4040/api/tunnels')
    obj = resp.json()
    for i in obj['tunnels']:
        if ( not ('https' in i['public_url'])):
            global oorl
            oorl = i['public_url']
            print(oorl)
            urlqr = pyqrcode.create(oorl)
            print(urlqr.terminal())
            #urlqr.png('code.png', scale=8, module_color=[0,0,0,128], background=[0xff, 0xff, 0xcc])
            #urlqr.show() #windows only
            return oorl


oorl = geturl()

@app.route('/notatvremote/', methods = ['GET', 'POST', 'DELETE'])
def showstuff():
    global oorl
    if (request.method == 'GET'):
    	return render_template('example.html')
    if (request.method == 'POST'):
        text = request.form['text']
        key = text if text else 'space'
        print(key)
        time.sleep(0.5)
        keyboard.press_and_release(key)
        rstr = oorl + '/notatvremote/' #+ text + '/'
        return redirect(rstr, code=302)
    else:
        return "I have no idea what you're trying to do"



@app.route('/')
def rut():
    if not oorl: geturl()
    return redirect((oorl + '/notatvremote'), code=302)
        
if __name__=='__main__':
    app.run()