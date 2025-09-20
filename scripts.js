document.addEventListener("DOMContentLoaded", function() {

    const chatbotToggleBtn = document.getElementById('chatbot-toggle-btn');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotCloseBtn = document.getElementById('chatbot-close-btn');

    chatbotToggleBtn.addEventListener('click', () => {
        chatbotWindow.classList.toggle('hidden');
    });
    chatbotCloseBtn.addEventListener('click', () => {
        chatbotWindow.classList.add('hidden');
    });

    const chatInput = document.getElementById('chat-input');
    const sendChatBtn = document.getElementById('send-chat');
    const chatMessages = document.getElementById('chat-messages');

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendChatBtn.addEventListener('click', () => {
        const userMessage = chatInput.value.trim();
        if (userMessage === '') return;

        addMessage(userMessage, true);
        chatInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                addMessage(data.reply);
            }, 500);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Lo siento, hubo un error. Intenta de nuevo más tarde.');
        });
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendChatBtn.click();
        }
    });

    // --- Lógica del formulario de Recomendaciones ---
    const contenedorRecomendaciones = document.querySelector('.contenedor-recomendaciones');
    const formularioFeedback = document.getElementById('formulario-feedback');
    const nombreInput = document.getElementById('nombre-reclutador');
    const comentarioInput = document.getElementById('comentario-reclutador');
    const respuestaContainer = document.getElementById('ia-respuesta-container');
    
    function sanitizeInput(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;',
        };
        const reg = /[&<>"'/]/ig;
        return text.replace(reg, (match) => (map[match]));
    }

    formularioFeedback.addEventListener('submit', (e) => {
        e.preventDefault();
        const nombre = sanitizeInput(nombreInput.value);
        const comentario = sanitizeInput(comentarioInput.value);

        fetch('/enviar_feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nombre: nombre, comentario: comentario }),
        })
        .then(response => response.json())
        .then(data => {
            respuestaContainer.style.display = 'block';
            respuestaContainer.innerHTML = `<p class="ia-respuesta">${data.respuesta}</p>`;
            formularioFeedback.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            respuestaContainer.style.display = 'block';
            respuestaContainer.innerHTML = `<p>Lo sentimos, hubo un error. Por favor, inténtelo de nuevo más tarde.</p>`;
        });
    });

    const inputDemo = document.getElementById('input-demo');
    const resultadoDemo = document.getElementById('resultado-demo');

    inputDemo.addEventListener('input', () => {
        const textoInseguro = inputDemo.value;
        const textoSeguro = sanitizeInput(textoInseguro);

        if (textoInseguro.includes('<script>')) {
            resultadoDemo.textContent = `Código malicioso bloqueado. El texto inseguro era: ${textoSeguro}`;
            resultadoDemo.className = 'resultado-inseguro';
        } else {
            resultadoDemo.textContent = `Tu texto es seguro: ${textoSeguro}`;
            resultadoDemo.className = 'resultado-seguro';
        }
    });
});