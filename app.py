from web_socket_server import WebSocketServer, socketio, app
from flask import render_template

app = WebSocketServer().create_app()
message_storage = {}

@socketio.on('message', 'author')
def handle_message(message, author):
    print(f'Received author: {author}')
    print(f'Received message: {message}')
    if author and message:
        if author not in message_storage:
            message_storage[author] = []
        else:
            message_storage[author].append(message) 

    socketio.emit('message', {'author': author, 'message': message})

@socketio.on('get_all_messages')
def handle_get_user_messages(data):
    socketio.emit('get_user_messages', message_storage)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('WebSocketClient.html')

if __name__ == '__main__':
    socketio.run(app)