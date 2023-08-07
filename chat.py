from flask import Flask,redirect,url_for,render_template,request,session
from flask_socketio import SocketIO,join_room,leave_room,send
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"]="gp"
socketio = SocketIO(app)

rooms = {}





@app.route('/')
def chat():
    session.clear()
    return render_template('chat.html')



@app.route('/registration', methods=['POST'])
def registration():

    return render_template('registration.html')


 

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')




import string
import random
def generate_random_string(length=7):
    while True:
        roomid = ""
        for _ in range(length):
            roomid += random.choice(ascii_uppercase)
        if roomid not in rooms:
            break
    return roomid       




@app.route('/code',methods=['GET', 'POST'])
def code():
    random_code = generate_random_string()
    
    return render_template('code.html', random_code=random_code)

@app.route('/chatting',methods=['GET', 'POST'])
def chatting():
    if request.method == 'POST':
        username = request.form.get('username')
        roomid = request.form.get('roomid',False)
        create = request.form.get("create",False)

        if username and roomid:
            return render_template('chatting.html',username=username,roomid=roomid)

        if not username:
            return render_template('login.html',error="Please enter a name",roomid =roomid,username=username)
        if roomid!=False:
            return render_template('login.html',error="Please enter a roomid")
        room=roomid
        if create in False:
            rooms[room] = {"members":0,"messages":[]}
        
        session["room"] = room
        session["username"] = username
        return redirect(url_for("room")) 
        
    return render_template("/")
@socketio.on("connect")
def connect(auth):
    roomid = session.get("roomid")
    username = session.get("username")
    if not roomid: 
        return


    join_room(roomid)
    send({"username": username , "message": "has entered the room"}, to=room)
    rooms[roomid]["members"] += 1
    print(f"{username} joined room {roomid}")


@socketio.on("disconnect")
def disconnect():
    roomid = session.get("roomid")
    username = session.get("username")
    leave_room(roomid)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    send({"username": username , "message": "has left the room"}, to=roomid)
    print(f"{username}has left the room {roomid}")

if __name__ == '__main__':
    socketio.run(app,debug = True)