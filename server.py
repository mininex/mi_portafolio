from flask import Flask, request, jsonify

app = Flask(__name__)

# Rutas existentes del portafolio
@app.route('/')
def home():
    return "Hola desde el servidor de Flask."

@app.route('/enviar_feedback', methods=['POST'])
def enviar_feedback():
    data = request.get_json()
    nombre = data.get('nombre')
    comentario = data.get('comentario')

    comentario_lower = comentario.lower()
    respuesta_ia = ""

    if any(palabra in comentario_lower for palabra in ["excelente", "impresionante", "felicidades", "genial", "increíble", "gustó", "fantástico"]):
        respuesta_ia = f"¡Hola, {nombre}! Muchísimas gracias por tu comentario tan positivo. Me alegra que mi trabajo te haya parecido interesante."
    elif any(palabra in comentario_lower for palabra in ["mejorar", "cambiar", "no me gustó", "problema", "malo"]):
        respuesta_ia = f"¡Hola, {nombre}! Aprecio mucho tu honestidad. La retroalimentación constructiva es vital para mi crecimiento, ¡gracias por tomarte el tiempo!"
    else:
        respuesta_ia = f"¡Hola, {nombre}! Gracias por tu opinión. Me emociona saber que has visitado mi portafolio. Si tienes alguna pregunta, no dudes en contactarme."

    return jsonify({"respuesta": respuesta_ia})

# Nueva ruta para el chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    reply = ""

    # Lógica simple del chatbot
    if "proyectos" in user_message or "trabajo" in user_message:
        reply = "¡Claro! Tengo varios proyectos interesantes. Echa un vistazo a mi sección de Proyectos para ver mi trabajo en desarrollo web, ciencia de datos y IA."
    elif "habilidades" in user_message or "tecnologias" in user_message:
        reply = "Mis habilidades principales son: HTML, CSS, JavaScript, Python y mi enfoque en Inteligencia Artificial y Ciencia de Datos."
    elif "contacto" in user_message or "contactarte" in user_message:
        reply = "Puedes contactarme a través de mis redes sociales o enviándome un mensaje en la sección de feedback. ¡Estoy disponible para proyectos interesantes!"
    elif "quien eres" in user_message or "tu nombre" in user_message:
        reply = "Soy el asistente de IA del portafolio de [Tu Nombre]. Mi trabajo es ayudarte a navegar por sus proyectos y habilidades."
    elif "hola" in user_message or "que tal" in user_message:
        reply = "¡Hola! ¿Cómo puedo ayudarte a conocer el trabajo de [Tu Nombre]?"
    else:
        reply = "No estoy seguro de haber entendido. ¿Podrías preguntarme sobre mis proyectos, habilidades o cómo contactar a [Tu Nombre]?"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)