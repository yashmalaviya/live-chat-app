from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "jfjfjfj" # Secure app configuration.
socketio = SocketIO(app)

# Dictonary to store active chat room details.
rooms = {}

# Function to generate a random room code of specified length.
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase) #Create a random code
        
        if code not in rooms: # Ensure that the generated code is unique.
            break

    return code

# HomePage route
@app.route('/', methods=['POST', 'GET']) # POST for posting the chat room unique ID, and GET to get the home page.
def home():
    """Handles the landing page where users can create or join chat rooms."""
    session.clear()  # Clear session data on navigating back to the home page
    
    if request.method == "POST":
        name = request.form.get("name") # Fetching the user's name
        code = request.form.get("code") # Fetching the room code
        
        # Determine if the user pressed 'Join' or 'Create'.
        join = request.form.get("join", False) # If the user doesn't press 'join', it returns False, instead of 'None'
        create = request.form.get("create", False) # If the user doesn't press 'create', it returns False, instead of 'None'

         
        # Check if the user has entered a name
        if not name:
            return render_template('home.html', error='Please enter a name', code=code, name=name)
        
        # If trying to join a room but no code is entered
        if join and not code:
            return render_template('home.html', error="Please Enter a Room Code.!!!", code=code, name=name)

        room = code

        # Handles room creation: Create a new room if 'create' is pressed.
        if create != False:
            room = generate_unique_code(4)   # Generate a 4-character room code
            rooms[room] = {'members': 0, 'messages': []}
        

        # If joining, check if the room code exists
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist !!!", code=code, name=name)
        
        # A session is a way to store information about user's interaction with a web application across MULTIPLE REQUESTS.
        # Store session details for the room and name.
        session["room"] = room
        session["name"] = name

        return redirect(url_for("room")) # Redirect to chat room.

    return render_template('home.html')

@app.route("/room")
def room():
    """Displays the chat room page if session data is valid."""
    room = session.get("room")

    # If no room or invalid session data, redirect to home
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"]) #third argument is so that even when we refresh the page, the chat remains there. We are rendering the chat history with the html page.

@socketio.on("sentMessage")
def message(data):
    """Handles the message event when a user sends a message."""
    room = session.get("room")
    if room not in rooms:
        return
    
    # Prepare content of the message
    content = {
        "name": session.get('name'),
        "message": data['data']
    }

    # Emit the message to all the client in the room.
    socketio.emit("customEvent", content, to=room)

    # Store the message in the room’s message history
    rooms[room]["messages"].append(content)

    print(f"{session.get('name')} said: {data['data']}") #Logging


@socketio.on("connect")
def connect(auth):
    """Handles when a user connects to a room."""
    room = session.get("room")
    name = session.get("name")

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
    """Handles when a user disconnects from a room."""
    room = session.get("room")
    name = session.get("name")
    leave_room(room)


    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room] # Delete the room if no members remain.

    socketio.emit("customEvent", {"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app, debug=True)