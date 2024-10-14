# Live Chat Application

This is a real-time live chat application where users can create a chat room and share the room code with others to join. Multiple users can participate in the same chat room, communicating in real-time. The application is built using Flask for the backend and SocketIO for handling real-time messaging.

## Features

- **Create and Join Chat Rooms:** Users can create a chat room, generating a unique code, and share it with others. The room will remain active as long as there are participants.
- **Real-time Messaging:** Messages sent by users are broadcasted to all members of the chat room instantly, providing a seamless live chat experience.
- **Chat History:** The chat history is displayed when the page is refreshed, so users can view previous messages sent in the room.

## Tech Stack

### Front-End:
- **HTML**: Structuring the web pages.
- **CSS**: Styling the UI components.
- **JavaScript**: Handling client-side interactions and integrating with SocketIO for real-time communication.

### Back-End:
- **Python**: Main server logic is built using Python.
- **Flask**: A lightweight web framework used to create routes and handle HTTP requests.
- **SocketIO**: Enables real-time, bidirectional communication between the client and server for live chat functionality.

## Project Structure:
/live-chat-app
│
├── /static
│   ├── /css
│   │   └── style.css       # CSS file for styling the chat application
│   └── /js
│       └── chat.js         # JavaScript file handling socket events for sending/receiving messages
│
├── /templates
│   ├── base.html           # Base HTML template
│   ├── home.html           # HTML for the home page where users create/join rooms
│   └── room.html           # HTML for the chat room interface
│
├── main.py                 # Main Python file with Flask app routes and SocketIO event handling
├── README.md               # Project README file
└── requirements.txt        # List of dependencies needed to run the project

## Installation:
**1. Clone the repository:**
`git clone https://github.com/your-username/live-chat-app.git`

**2. Navigate to the project directory:**
`cd live-chat-app`

**3. Create and activate a virtual environment (optional but recommended):**
`python -m venv venv`
`source venv/bin/activate` # On Windows use `venv\Scripts\activate`

**4. Install the required dependencies:**
`pip install -r requirements.txt`

**5. Run the Application:**
`python main.py`

**6. Open your web browser and navigate to http://127.0.0.1:5000 to access the app**




