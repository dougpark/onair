import logging
# https://flask-socketio.readthedocs.io/en/latest/intro.html
from datetime import datetime
from datetime import timedelta
from threading import Thread
import dnp_util as dnp_util

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

# DotMap is a dot-access dictionary subclass
# https://pypi.org/project/dotmap/
# https://github.com/drgrib/dotmap
from dotmap import DotMap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'justasecretkeythatishouldputhere'
socketio = SocketIO(app)
refreshVal = 0
msgStatus = False

# OnAir Data
defaultSessionMessage = 'On Air'
sessionMessage = defaultSessionMessage
onAir = False
defaultSessionLength = 120
sessionLength = defaultSessionLength
sessionStartTime = datetime.now()
sessionEndTime = datetime.now()
sessionRemaining = datetime.now()
sessionStatus = DotMap()
pushBackground = 0


# logging configuration
# debug, info, warning, error, critical
logging.basicConfig(filename='./instance/server.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Started')
logging.info('running socket_server.py')


# called every n seconds to push current status to all clients
def pushStatus():
    payload = formatSessionStatus()
    socketio.emit('update', payload, broadcast=True)

# update the payload with current session status
def formatSessionStatus():
    global sessionStatus, sessionEndTime, sessionRemaining

    now = datetime.now()
    sessionEndTime = sessionStartTime + timedelta(minutes=int(sessionLength))
    sessionRemainingO = (sessionEndTime - now)
    sessionRemaining = dnp_util.strfdelta(sessionRemainingO,"%s%H:%M:%S")

    sessionStatus.sessionStartTime = sessionStartTime.strftime("%I:%M:%S %p")
    sessionStatus.sessionEndTime = sessionEndTime.strftime("%I:%M:%S %p")
    sessionStatus.sessionRemaining = sessionRemaining

    sessionStatus.data = 'ok'
    sessionStatus.onAir=onAir
    sessionStatus.sessionMessage=sessionMessage
    sessionStatus.sessionLength=sessionLength
    sessionStatus.sessionNow=now.strftime("%I:%M:%S %p")
    
    # print(sessionStatus)
    return sessionStatus.toDict()


@app.route('/')
def index():
    return render_template('index.html',adminPanel='none', date=datetime.now())

@app.route('/admin')
def admin():
    return render_template('index.html',adminPanel='block', date=datetime.now())

@app.route('/on')
def on():
    newSessionLength = request.args.get('sessionLength', default=defaultSessionLength)
    startOnAir(newSessionLength)
    return jsonify(dict(success=True, message='On', sessionLength=newSessionLength))

@app.route('/off')
def off():
    stopOnAir()
    return jsonify(dict(success=True, message='Off'))

@app.route('/api')
def api():
    logging.info('api called')
    query = dict(request.args)
    socketio.emit('log', dict(data=str(query)), broadcast=True)
    return jsonify(dict(success=True, message='Received'))

@app.route('/onair')
def onair():
    logging.info('onair called')
    query = dict(request.args)
    # socketio.emit('log', dict(data=str(query)), broadcast=True)
    global msgStatus, onAir
    msgStatus = True
    onAir = True
    # payload = dict(data='ok', messageStatus=msgStatus, onAir=onAir, sessionMessage=sessionMessage)
    payload = formatSessionStatus()
    socketio.emit('update', payload, broadcast=True)
    return render_template('index.html',date=datetime.now())


@socketio.on('refresh')
def refreshFunc(data):
    global refreshVal
    logging.info('refresh called')
    refreshVal = refreshVal + 1
    payload = dict(data=refreshVal, messageStatus=msgStatus, message=sessionMessage)
    emit('refreshResp', payload, broadcast=True)

@socketio.on('getrefresh')
def getrefreshFunc(data):
    logging.info('getrefresh called')
    payload = dict(data=refreshVal, messageStatus=msgStatus, onAir=onAir, message=sessionMessage)
    emit('refreshResp', payload, broadcast=True)

def startOnAir(newSessionLength=defaultSessionLength):
    global msgStatus, onAir, sessionLength, sessionStartTime, pushBackground
    logging.info('startOnAir called')
    msgStatus = True
    onAir = True
    sessionLength = newSessionLength
    sessionStartTime = datetime.now()
    pushBackground = dnp_util.start_run_thread(pushStatus)
    # payload = dict(data='ok', messageStatus=msgStatus,onAir=onAir, sessionMessage=sessionMessage,sessionLength=sessionLength)
    payload = formatSessionStatus()
    socketio.emit('update', payload, broadcast=True)

@socketio.on('showmsg')
def showMsgNow(data):
    startOnAir()

def stopOnAir():
    global msgStatus, onAir
    logging.info('hideMsg called')
    msgStatus = False
    onAir = False
    pushBackground.terminate() 
    # payload = dict(data='ok', messageStatus=msgStatus,onAir=onAir, message=sessionMessage)
    payload = formatSessionStatus()
    socketio.emit('update', payload, broadcast=True)
    return 

@socketio.on('hidemsg')
def hideMsgNow(data):
    stopOnAir()
    

@socketio.on('getstatus')
def getStatus(data):
    logging.info('getStatus called')
    # payload = dict(data='ok', messageStatus=msgStatus,onAir=onAir,sessionLength=sessionLength, sessionMessage=sessionMessage)
    payload = formatSessionStatus()
    emit('update', payload, broadcast=True)

@socketio.on('one')
def one(data):
    logging.info('one called')
    logging.info(request.sid)
    payload = dict(data='This response is from one')
    emit('oneResp', payload)

@socketio.on('mirror')
def mirror(data):
    logging.info('mirror called')
    logging.info(data)
    payload = data
    emit('mirrorResp', payload)

@socketio.on('connect')
def on_connect():
    logging.info('connected called')
    payload = dict(data='Connection ack from server')
    emit('connectResp', payload)

if __name__ == '__main__':
    # allow_unsafe_werkzeug=True - allows flask to run in docker container as production. Not safe.
    socketio.run(app,allow_unsafe_werkzeug=True,host='0.0.0.0', port=5000, debug=True)