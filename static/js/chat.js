// Connect to the socket on the server
var socketio = io();

// Get the message div for displaying chat messages
const messages = document.getElementById("messages");

// Function to create and display a new message in the chat
const createMessage = (name, msg) => {
    const content = `
    <div class = "text">
        <strong>${name}:</strong> ${msg}
        <span class="dateAndTime">${new Date().toLocaleString()}</span>
    </div>
    `;
    messages.innerHTML += content; // Append message to the chat
};

// Listen for the "customEvent" sent from the server
socketio.on("customEvent", (data) => {
    createMessage(data.name, data.message);
});

// Send the message when the user clicks the "Send" button
const sendMessage = () => {
    const message = document.getElementById("message");
    if (message.value === "") return; // Prevent sending empty messages

    socketio.emit("sentMessage", { data: message.value }); //Emit the message to the server
    message.value = ""; // Clear the message input box after sending
};