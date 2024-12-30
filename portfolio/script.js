async function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    const chatOutput = document.getElementById('chat-output');

    if (!userInput) return;

    // Display user message
    appendMessage("You", userInput);
    document.getElementById('user-input').value = "";

    // Typing indicator
    const typingIndicator = document.createElement('p');
    typingIndicator.id = "typing-indicator";
    typingIndicator.innerHTML = `<strong>Chatbot:</strong> Typing...`;
    chatOutput.appendChild(typingIndicator);
    chatOutput.scrollTop = chatOutput.scrollHeight;

    try {
        // API call
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_input: userInput, session_id: 'default_session' })
        });

        const data = await response.json();

        // Remove typing indicator and display formatted response
        if (typingIndicator) typingIndicator.remove();
        appendFormattedMessage("Chatbot", data.answer || "Unexpected response");
    } catch (error) {
        if (typingIndicator) typingIndicator.remove();
        console.error('Error:', error);
        appendMessage("Chatbot", `Error: ${error.message}`);
    } finally {
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }
}

function appendMessage(sender, message) {
    const chatOutput = document.getElementById('chat-output');
    const messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatOutput.appendChild(messageElement);
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

function appendFormattedMessage(sender, message) {
    const chatOutput = document.getElementById('chat-output');
    const formattedMessage = formatMarkdown(message);
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${sender}:</strong><br>${formattedMessage}`;
    messageElement.className = "chatbot-response";
    chatOutput.appendChild(messageElement);
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

function formatMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Bold
        .replace(/(?<!\*)\*(.*?)\*(?!\*)/g, "<em>$1</em>") // Italics (single *)
        .replace(/\n/g, "<br>") // Newlines
        .replace(/^\d+\.\s(.*?)(?=\n|$)/gm, "<strong>$&</strong><br>") // Numbered lists
        .replace(/^\*\s(.*?)(?=\n|$)/gm, "• $1<br>") // Convert bullet points
        .replace(/•/g, "• "); // Ensure spacing after bullet points
}

function clearChat() {
    document.getElementById('chat-output').innerHTML = "";
}
