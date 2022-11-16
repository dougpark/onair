import logging
from datetime import datetime
from datetime import timedelta
from threading import Thread
import dnp_util as dnp_util

from flask import Flask, jsonify, render_template, request
# https://flask-socketio.readthedocs.io/en/latest/intro.html
from flask_socketio import SocketIO, emit

# DotMap is a dot-access dictionary subclass
# https://pypi.org/project/dotmap/
# https://github.com/drgrib/dotmap
from dotmap import DotMap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'justasecretkeythatishouldputhere'
socketio = SocketIO(app)

# Test Data
refreshVal = 0
msg_status = 'no message'

# OnAir Data
default_session_message = 'On Air'
default_standby_message = 'Stand By'
default_session_duration = 120
default_session_color = 'red'
default_standby_color = 'green'
onair_status = False
session_start_time = datetime.now()
session_end_time = None
session_remaining = None
session_status = DotMap()
broadcast_bg_thread = None

# logging configuration
# debug, info, warning, error, critical
logging.basicConfig(filename='./instance/server.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Started')
logging.info('running socket_server.py')

# update the payload with current session status
def get_session_status():
    global session_status, session_end_time, session_remaining

    now = datetime.now()
    session_end_time = session_start_time + timedelta(minutes=int(default_session_duration))
    sessionRemainingO = (session_end_time - now)
    session_remaining = dnp_util.strfdelta(sessionRemainingO,"%s%H:%M:%S")

    session_status.sessionStartTime = session_start_time.strftime("%I:%M:%S %p")
    session_status.sessionEndTime = session_end_time.strftime("%I:%M:%S %p")
    session_status.sessionRemaining = session_remaining

    session_status.standByMessage = default_standby_message
    session_status.onAir = onair_status
    session_status.sessionMessage = default_session_message
    session_status.sessionDuration = default_session_duration
    session_status.sessionNow = now.strftime("%I:%M:%S %p")
    session_status.sessionColor = default_session_color
    session_status.standByColor = default_standby_color
    
    # print(sessionStatus)
    return session_status.toDict()

# process the start-session request, resets time-remaining timer
def start_onair_session():
    global onair_status, session_start_time, broadcast_bg_thread
    logging.info('start_onair_session called')
    onair_status = True
    session_start_time = datetime.now()
    broadcast_bg_thread = dnp_util.start_background_thread(1, broadcast_status)
    payload = get_session_status()
    socketio.emit('update', payload, broadcast=True)

# process the stop-session request
def stop_onair_session():
    global onair_status
    logging.info('stop_onair_session called')
    onair_status = False
    broadcast_bg_thread.terminate() 
    payload = get_session_status()
    socketio.emit('update', payload, broadcast=True)
    return 

# called every n seconds to push current status to all clients
def broadcast_status():
    payload = get_session_status()
    socketio.emit('update', payload, broadcast=True)

# return normal view-only page
@app.route('/')
def index():
    return render_template('index.html',adminPanel='none', date=datetime.now())

# return page with admin panel
@app.route('/admin')
def admin():
    return render_template('index.html',adminPanel='block', date=datetime.now())

# api to start the session
# can set sessionLength in minutes
# ex. https://server/start?sessionlength=90
@app.route('/start')
def route_start():
    global default_session_message, default_standby_message, default_session_duration
    default_session_message = request.args.get('message', default=default_session_message)
    default_standby_message = request.args.get('standby', default=default_standby_message)
    default_session_duration = request.args.get('duration', default=default_session_duration)

    start_onair_session()
    return jsonify(dict(success=True, message='start', 
        sessionMessage=default_session_message,
        sessionStandby=default_standby_message,
        sessionDuration=default_session_duration))

# api to stop the session
# ex. https://server/stop
@app.route('/stop')
def route_stop():
    stop_onair_session()
    return jsonify(dict(success=True, message='stop'))

# responds to button click to start a new session
@socketio.on('startSession')
def start_session(data):
    start_onair_session()

# responds to button click to stop the session
@socketio.on('stopSession')
def stop_session(data):
    stop_onair_session()

# process the getstatus request, does not change status
@socketio.on('getstatus')
def get_status(data):
    logging.info('getStatus called')
    payload = get_session_status()
    emit('update', payload, broadcast=True)

# process connection request
@socketio.on('connect')
def on_connect():
    logging.info('on_connect called')
    payload = dict(data='Connection ack from server')
    emit('connectResp', payload)

# not used
@app.route('/api')
def api():
    logging.info('api called')
    query = dict(request.args)
    socketio.emit('log', dict(data=str(query)), broadcast=True)
    return jsonify(dict(success=True, message='Received'))

# start a session from a route
# best to use /start
@app.route('/onair')
def route_onair():
    logging.info('onair called')
    query = dict(request.args)
    start_onair_session()
    return render_template('index.html',date=datetime.now())

# not used
@socketio.on('one')
def one(data):
    logging.info('one called')
    logging.info(request.sid)
    payload = dict(data='This response is from one')
    emit('oneResp', payload)

# not used
@socketio.on('mirror')
def mirror(data):
    logging.info('mirror called')
    logging.info(data)
    payload = data
    emit('mirrorResp', payload)

# used for testing
@socketio.on('refresh')
def refreshFunc(data):
    global refreshVal
    logging.info('refresh called')
    refreshVal = refreshVal + 1
    payload = dict(data=refreshVal, messageStatus=msg_status, message=default_session_message)
    emit('refreshResp', payload, broadcast=True)

# not used
@socketio.on('getrefresh')
def getrefreshFunc(data):
    logging.info('getrefresh called')
    payload = dict(data=refreshVal, messageStatus=msg_status, onAir=onair_status, message=default_session_message)
    emit('refreshResp', payload, broadcast=True)

if __name__ == '__main__':
    # allow_unsafe_werkzeug=True - allows flask to run in docker container as production. Not safe.
    socketio.run(app,allow_unsafe_werkzeug=True,host='0.0.0.0', port=5000, debug=True)