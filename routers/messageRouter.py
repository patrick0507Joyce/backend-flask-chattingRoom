from flask_socketio import leave_room, join_room

from app import *
from flask import Flask, jsonify, session, request, json

roomForStudents = 'studentRoom'
roomForStudentsList = []
roomForTeachers = 'teacherRoom'
roomForTeachersList = []
roomForCommon = 'commonRoom'
roomForCommonList = []


@socketio.on('connect')
def on_connect():
    response = str(request.sid)
    socketio.emit('established', {"sid": response}, callback=(
        print("received by client" + response)
    ))


@socketio.on('join')
def on_join(group_info):
    global roomName
    global roomList
    group_type = group_info["type"]
    user_name = group_info['userName']
    if group_type == "Student":
        roomName = roomForStudents
        roomList = roomForStudentsList
        roomForStudentsList.append(request.sid)
    elif group_type == "Teacher":
        roomName = roomForTeachers
        roomList = roomForTeachersList
        roomForTeachersList.append(request.sid)
    else:
        roomName = roomForCommon
        roomList = roomForCommonList
        roomForCommonList.append(request.sid)

    join_room(roomName)
    room_join_msg_info = {
        'type': 'userChangeInfoMessageEvent',
        'message': user_name + ' join room ' + roomName,
        'groupMembers': roomList
    }
    socketio.emit('responseMessage', room_join_msg_info, room=roomName)


@socketio.on('requestMessage')
def on_message(msg):
    global msg_content
    body = msg
    print('received json: ' + str(body) + " from:" + request.sid)
    body_type = body["type"]

    if body_type == 'setNameEvent':
        msg_content = {
            'type': 'userChangeInfoMessageEvent',
            'message': body['userName'] + ' enter room'
        }
    elif body_type == 'messageEvent':
        msg_content = {
            'type': 'messageEvent',
            'message': body['message']
        }
    else:
        msg_content = {
            'type': 'messageEvent',
            'message': 'unDefined'
        }

    user_sid = request.sid
    if user_sid in roomForStudentsList:
        socketio.emit('responseMessage', msg_content, room=roomForStudents)
    elif user_sid in roomForTeachersList:
        socketio.emit('responseMessage', msg_content, room=roomForTeachers)
    else:
        socketio.emit('responseMessage', msg_content, broadcast=True)


@socketio.on('disconnect')
def on_leave(data):
    username = session['username']
    room = data['room']
    leave_room(room)
    msg_content = {
        'type': 'userChangeInfoMessageEvent',
        'message': username + 'enter room'
    }
    socketio.emit('responseMessage', jsonify(msg_content), broadcast=True)
