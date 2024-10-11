from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "jfjfjfj"
socketio = SocketIO(app)

# Making a dictonary to store the details of the already present Chat Rooms.
rooms = {}

# Function for creating random room codes:
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        # If the generated chat room code doesn't exist already in the created rooms list, then break the loop.
        if code not in rooms:
            break

    return code

# HomePage route: Home page is where we will land, or page before entering to any chat room.
@app.route('/', methods=['POST', 'GET']) # POST for posting the chat room unique ID, and GET to get the home page.
def home():

    #clearing session data when user goes back to home page, so that they can create or join a new chat.
    session.clear()
    # Check if the request method is "POST" i.e. we are trying to get the form data when the user clicks on "Submit" Button.
    #'request.form' is a python dictionary.
    if request.method == "POST":
        name = request.form.get("name") #get() function fetches the values of "name" key. If the value doesn't exist, it'll return none.
        code = request.form.get("code") #get() function fetches the values of "code" key. If the value doesn't exist, it'll return none.
        '''
            Below mentioned "join" and "create" are button, hence, they don't have any value associated with them,
            we are just trying to get the keys, to know that the buttons are pressed.
        '''
        join = request.form.get("join", False) # get() function fetches the values of "join" key. We provide second arg. as "False"...(below)
        create = request.form.get("create", False)# ... "False", as if the user doesn't not click on "join" or "create" button, instead of returning none, we'll get False.

        # Checking if the user haven't provided the 'name'. We will give an error if 'name' is empty.
        if not name:
            return render_template('home.html', error='Please enter a name', code=code, name=name)
        
        # Checking if the user has pressed 'join' or 'create':
          # Checking if user has not clicked 'join' button and their is no entered 'code':
        if join != False and not code:
            return render_template('home.html', error="Please Enter a Room Code.!!!", code=code, name=name)

        room = code

        # Checking if 'create' button is pressed. It means that user wants to create a chat room
        if create != False:
            room = generate_unique_code(4) #defined above.
            rooms[room] = {'members': 0, 'messages': []}
        # Checking if they have not pressed "create" button. It means that if the user don't want to create a room, instead they want to 'join' a Chat room.
        # Checking if the entered 'code' is not available alread in the room dictionary. Hence, give an error.
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist !!!", code=code, name=name)
        
        # A session is a way to store information about user's interaction with a web application across MULTIPLE REQUESTS.
        session["room"] = room # Storing the room code in which user is or is going to be in.
        session["name"] = name # Storing the name of the user.

        # Redirect to the Chat Room (a different route define later)
        return redirect(url_for("room"))

    return render_template('home.html')

@app.route("/room")
def room():
    # Writing the below code, so that if a user tries to directly access the "room" page by manually typing '/room', it doesn't goes to the room page.
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"]) #third argument is so that even when we refresh the page, the chat remains there. We are rendering the chat history with the html page.

@socketio.on("sentMessage")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "name": session.get('name'),
        "message": data['data']
    }
    socketio.emit("customEvent", content, to=room) #this send the content back to all the clients. socketio.on("customEvent", (data)) in room.html will listen to this...
                            #We can also use, send() method which by default assigns the event name to "message", which is heard by the socketio() in room.html
                            # then we have to change the eventlistener socketio.on() event name from "customEvent" to "message".
    rooms[room]["messages"].append(content) # If the server restarts, we will loose all messages, as the "rooms" dict is in RAM (local),...
    # we can use a DB to store the messages, so that the history of messages does not go away.
    print(f"{session.get('name')} said: {data['data']}") #Logging

# Connection Route - Joining the Chat Room
# Using @socketio as that's the initilization object for the SocketIO Library. (In the beginning).
@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    # Just confirming anybody is not directly coming to any room before inputting the room code and their name.
    if not room or not name:
        return
    # Making sure that the room exists.
    if room not in rooms:
        leave_room(room)
        return
    
    #The above if statements did not make the function return, it means the room does exist.
    join_room(room)
    socketio.emit("customEvent", {"name": name, "message": "has entered the room"}, to=room) # Sending the message to the chat room.
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}") #Logging.

# Disconnection - Leaving the Chat Room
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0: #If everybody left the room, and there's no one,...
            del rooms[room] #...Then... Delete the room.

    socketio.emit("customEvent", {"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app, debug=True)