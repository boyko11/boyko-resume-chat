
var BASE_URL = window.location.hostname === 'localhost' ? '' : '/chat';
let chatId = null;

document.getElementById('chatForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const inputField = document.getElementById('queryInput');
    const query = inputField.value;
    const chatArea = document.getElementById('chatArea');
    const loadingIndicator = document.getElementById('loading');

    const userMessageDiv = document.createElement('div');
    userMessageDiv.textContent = query;
    userMessageDiv.classList.add('message', 'user-message');
    chatArea.appendChild(userMessageDiv);

    inputField.value = '';
    inputField.disabled = true;
    loadingIndicator.style.display = 'flex';

    try {
        const response = await fetch(BASE_URL + '/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: query, chat_id: chatId })
        });

        const responseData = await response.json();
        chatId = responseData.chat_id;

        const botMessageDiv = document.createElement('div');
        botMessageDiv.textContent = responseData.message;
        botMessageDiv.classList.add('message', 'bot-message');
        chatArea.appendChild(botMessageDiv);

        chatArea.scrollTop = chatArea.scrollHeight;
    } catch (error) {
        console.error('Error:', error);
    } finally {
        inputField.disabled = false;
        loadingIndicator.style.display = 'none';
        inputField.focus();
    }
});
