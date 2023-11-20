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
        const response = await fetch('/query', {
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


async function loadConfig(config_name) {
    try {
        const response = await fetch(`/config/${config_name}`);
        const person_config = await response.json();
        customizeUIForPerson(person_config.name);
    } catch (error) {
        console.error('Error fetching config:', error);
    }
}

function customizeUIForPerson(person_name) {
    document.title = `${person_name} Resume Chat`;
    const inputField = document.getElementById('queryInput');
    inputField.placeholder = `Ask a question about ${person_name}...`;
}

loadConfig('PersonConfig');

