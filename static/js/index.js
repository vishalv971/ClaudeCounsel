function sendMessage() {
    const userMessage = document.getElementById("userMessage").value;
    const chatContainer = document.querySelector(".chat-container");
    const newMessage = document.createElement("div");
    newMessage.classList.add("message", "send");
    newMessage.innerText = userMessage;
    chatContainer.appendChild(newMessage);
    document.getElementById("userMessage").value = "";
}