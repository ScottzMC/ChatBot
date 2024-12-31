async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    // Append user input to chat log
    const chatLog = document.getElementById("chat-log");
    chatLog.innerHTML += `<div class="user">You: ${userInput}</div>`;

    // Send query to Flask server
    const response = await fetch("/get_response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: userInput })
    });

    const data = await response.json();
    const botResponse = data.response;

    // Append chatbot's response to chat log
    chatLog.innerHTML += `<div class="bot">Chatbot: ${botResponse}</div>`;
    document.getElementById("user-input").value = "";

    // Auto-scroll to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
}