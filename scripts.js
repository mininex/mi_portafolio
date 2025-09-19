document.addEventListener("DOMContentLoaded", function() {

    // --- Lógica del fondo de partículas ---
    const canvas = document.getElementById('canvas-fondo');
    const ctx = canvas.getContext('2d');
    let W, H, particles;
    const colors = ['#f5d5e0', '#6667ab', '#7b337e']; // Colores de tu paleta

    function resizeCanvas() {
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
        particles = [];
        for (let i = 0; i < 50; i++) {
            particles.push(new Particle());
        }
    }
    window.addEventListener('resize', resizeCanvas);

    class Particle {
        constructor() {
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.size = Math.random() * 2 + 1;
            this.speedX = Math.random() * 3 - 1.5;
            this.speedY = Math.random() * 3 - 1.5;
            this.color = colors[Math.floor(Math.random() * colors.length)];
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x > W || this.x < 0) this.speedX *= -1;
            if (this.y > H || this.y < 0) this.speedY *= -1;
        }
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function animate() {
        ctx.fillStyle = 'rgba(33, 6, 53, 0.1)'; // Limpia con un color semitransparente
        ctx.fillRect(0, 0, W, H);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        connectParticles();
        requestAnimationFrame(animate);
    }
    
    function connectParticles() {
        let opacityValue = 1;
        for (let a = 0; a < particles.length; a++) {
            for (let b = a; b < particles.length; b++) {
                let distance = ((particles[a].x - particles[b].x) ** 2 + (particles[a].y - particles[b].y) ** 2) ** 0.5;
                if (distance < 100) {
                    opacityValue = 1 - (distance / 100);
                    ctx.strokeStyle = `rgba(122, 51, 126, ${opacityValue})`;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    ctx.stroke();
                }
            }
        }
    }

    resizeCanvas();
    animate();

    // --- Lógica del formulario de Recomendaciones ---
    const contenedorRecomendaciones = document.querySelector('.contenedor-recomendaciones');
    // ...

    // --- Lógica del formulario de Feedback ---
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
            headers: { 'Content-Type': 'application/json' },
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

    // --- Lógica de la demostración de Seguridad ---
    const inputDemo = document.getElementById('input-demo');
    const resultadoDemo = document.getElementById('resultado-demo');

    inputDemo.addEventListener('input', () => {
        const textoInseguro = inputDemo.value;
        const textoSeguro = sanitizeInput(textoInseguro);

        if (textoInseguro.includes('<script>')) {
            resultadoDemo.textContent = `Código malicioso bloqueado. El texto inseguro era: ${textoSeguro}`;
            resultadoDemo.className = 'resultado-seguro';
        } else {
            resultadoDemo.textContent = `Tu texto es seguro: ${textoSeguro}`;
            resultadoDemo.className = 'resultado-seguro';
        }
    });

    // --- Lógica del Chatbot ---
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
});