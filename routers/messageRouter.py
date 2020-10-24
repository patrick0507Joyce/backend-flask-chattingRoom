from flask_socketio import leave_room

from app import *
from flask import Flask, jsonify, session, request


@socketio.on('connect')
def on_connect():
    print("is connected")

@socketio.on('message')
def on_message(msg):
    body = msg
    print('received json: ' + str(body) + " from:" + request.sid)
    body_type = body["type"]
    if body_type == 'setNameEvent':
        msg_content = {
            'type':'userChangeInfoMessageEvent',
            'message':body['userName'] + 'enter room'
        }
        socketio.emit('responseMessage',msg_content, broadcast=True)
    elif body_type == 'messageEvent':
        msg_content = {
            'type': 'messageEvent',
            'message': body['message']
        }
        socketio.emit('responseMessage', msg_content, broadcast=True)
    else:
        socketio.emit('responseMessage', {'case':'unDefined'}, broadcast=True)


@socketio.on('close')
def on_leave(data):
    username = session['username']
    room = data['room']
    leave_room(room)
    msg_content = {
        'type': 'userChangeInfoMessageEvent',
        'message':username + 'enter room'
    }
    socketio.emit('responseMessage', jsonify(msg_content), broadcast=True)



