from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatRoom'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def hello_world():
    return 'Hello World!'

from routers import messageRouter

if __name__ == '__main__':
    socketio.run(app)
