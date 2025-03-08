from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a secure key in production
socketio = SocketIO(app, cors_allowed_origins="*")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"  # Change this to a secure password
video_url = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global video_url
    if 'admin' in session:
        if request.method == 'POST':
            video_url = request.form.get('video_url')
        return render_template('admin.html', video_url=video_url)
    return render_template('index.html', video_url=video_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# WebSocket for Sync
@socketio.on('video_control')
def handle_video_control(data):
    emit('sync_video', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    os.makedirs("templates", exist_ok=True)  # Ensure templates directory exists
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

# HTML Templates
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Drive Video Sync</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body>
    <h2>Google Drive Synced Video</h2>
    {% if video_url %}
    <video id="video" width="800" controls>
        <source src="{{ video_url }}" type="video/mp4">
    </video>
    {% else %}
    <p>Waiting for admin to start streaming...</p>
    {% endif %}
    <script>
        const socket = io();
        const video = document.getElementById("video");
        if (video) {
            let ignoreEvents = false;
            function syncAction(action, time) {
                if (!ignoreEvents) {
                    socket.emit("video_control", { action, time });
                }
            }
            video.addEventListener("play", () => syncAction("play", video.currentTime));
            video.addEventListener("pause", () => syncAction("pause", video.currentTime));
            video.addEventListener("seeked", () => syncAction("seek", video.currentTime));
            socket.on("sync_video", (data) => {
                ignoreEvents = true;
                if (data.action === "play") video.play();
                if (data.action === "pause") video.pause();
                if (data.action === "seek") video.currentTime = data.time;
                setTimeout(() => { ignoreEvents = false; }, 500);
            });
        }
    </script>
</body>
</html>
'''

admin_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
</head>
<body>
    <h2>Admin Panel - Start Streaming</h2>
    <form method="post">
        <label for="video_url">Enter Google Drive Video URL:</label>
        <input type="text" name="video_url" required>
        <button type="submit">Start Streaming</button>
    </form>
    <a href="/logout">Logout</a>
</body>
</html>
'''

login_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Admin Login</h2>
    <form method="post">
        <label for="username">Username:</label>
        <input type="text" name="username" required>
        <label for="password">Password:</label>
        <input type="password" name="password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
'''

with open("templates/index.html", "w") as f:
    f.write(index_html)
with open("templates/admin.html", "w") as f:
    f.write(admin_html)
with open("templates/login.html", "w") as f:
    f.write(login_html)
