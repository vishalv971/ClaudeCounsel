function searchKeyPress(e) {
    // look for window.event in case event isn't passed in
    e = e || window.event;
    if (e.keyCode == 13) {
        document.getElementById("send-button").click();
        return false;
    }
    return true;
}

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
        message: userMessage,
    };

    // Convert the JSON object to a string
    const jsonPayload = JSON.stringify(jsonData);
    const xhr = new XMLHttpRequest();

    // Configure the request
    xhr.open("POST", "http://127.0.0.1:5000/infer", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            const response = JSON.parse(xhr.responseText);
            const newReceivedMessage = document.createElement("div");
            newReceivedMessage.classList.add("message", "receive");
            newReceivedMessage.innerText = response["data"];

            if (response["discussionData"] != null) {
                newReceivedMessage.innerHTML += `<br/><br/> <h4>Relevant Forum Links:</h4>`;
                const discussionList = document.createElement("ul");
                discussionList.classList.add("list-group");

                // Iterate through the "discussionData" array and create list items
                response.discussionData.forEach((discussion) => {
                    const listItem = document.createElement("li");
                    listItem.classList.add("list-group-item");
                    const listItemContent = `
                    <a href="${discussion.url}" target="_blank">
                        <img src="${discussion.favicon}" alt="Favicon" class="favicon">
                        ${discussion.title}
                    </a>
                `;

                    listItem.innerHTML = listItemContent;
                    discussionList.appendChild(listItem);
                });

                newReceivedMessage.appendChild(discussionList);
            }
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
