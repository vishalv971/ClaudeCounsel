function sendMessage() {
    const userMessage = document.getElementById("userMessage").value;
    const chatContainer = document.querySelector(".chat-container");
    const newMessage = document.createElement("div");
    newMessage.classList.add("message", "send");
    newMessage.innerText = userMessage;
    chatContainer.appendChild(newMessage);
    document.getElementById("userMessage").value = "";

    // Make the API call to the backend

    const jsonData = {
        "message": userMessage
    };

    // Convert the JSON object to a string
    const jsonPayload = JSON.stringify(jsonData);
    const xhr = new XMLHttpRequest();

    // Configure the request
    xhr.open("POST", "https://claudecounsel.onrender.com/infer", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            const response = JSON.parse(xhr.responseText);
            const newReceivedMessage = document.createElement("div");
            newReceivedMessage.classList.add("message", "receive");
            newReceivedMessage.innerText = response['data'];
            chatContainer.appendChild(newReceivedMessage);

        } else {
            console.error("API request failed");
        }
    };

    // Define a function to handle errors
    xhr.onerror = function () {
        console.error("Network error occurred");
    };

    // Send the request with the JSON payload
    xhr.send(jsonPayload);
}
