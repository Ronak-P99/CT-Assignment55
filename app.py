from web_socket_server import WebSocketServer, socketio, app
from flask import render_template, request, jsonify

app = WebSocketServer().create_app()
message_storage = {}


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    author = data['user']
    message = data['message']

    if author and message:
        if author not in message_storage:
            message_storage[author] = [message]
        else:
            message_storage[author].append(message)
        
        socketio.emit('message', {'author': author, 'message': message})
        return jsonify({"status": "success", "author": author, "message": message}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid data"}), 400


@socketio.on('get_all_messages')
def handle_get_user_messages(data):
    author = data['user']  
    if author in message_storage:
        socketio.emit('get_user_messages', {'author': author, 'messages': message_storage[author]})
    else:
        socketio.emit('get_user_messages', {'author': author, 'messages': []})

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

  