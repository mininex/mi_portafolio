import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import spacy

# Intenta importar la librería de OpenAI; si no está instalada, no se usará.
try:
    import openai
except ImportError:
    openai = None
    print("OpenAI no está instalado. El chatbot usará las reglas de SpaCy y una respuesta genérica.")

# --- Inicialización de Flask y modelos ---
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) # Permite llamadas desde diferentes dominios

# Carga el modelo de SpaCy para análisis de lenguaje
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("El modelo de SpaCy no está instalado. Ejecuta 'python -m spacy download es_core_news_sm'")
    exit()

# Configura la clave de OpenAI si existe en las variables de entorno
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
if openai and OPENAI_KEY:
    openai.api_key = OPENAI_KEY
    print("API de OpenAI configurada. El chatbot la usará como fallback.")
else:
    print("No se encontró la clave de OpenAI. El chatbot solo usará las reglas de SpaCy.")

# --- Rutas de la aplicación ---
@app.route("/")
def home():
    """
    Ruta principal que sirve el archivo HTML del frontend.
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Ruta principal para manejar las solicitudes de chat.

    La lógica funciona en cascada:
    1. Primero intenta una respuesta basada en reglas predefinidas con SpaCy.
    2. Si no hay coincidencia, intenta generar una respuesta con OpenAI.
    3. Si no hay clave de OpenAI o la API falla, usa una respuesta genérica.
    """
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "No se proporcionó un mensaje"}), 400

    doc = nlp(user_message)
    reply = ""
    user_message_lower = user_message.lower()

    # --- Lógica con SpaCy (Respuestas basadas en reglas) ---
    if any(token.lemma_ in ["nombre", "quien", "eres"] for token in doc):
        reply = "Mi nombre es Vanessa Ferrer."
    elif any(token.lemma_ in ["habilidad", "tecnologia", "saber", "conocer"] for token in doc):
        reply = "Mis habilidades son: Python, Desarrollo de AI, Bases de datos, SQL, algo de HTML, JavaScript, CSS, Diseño Web."
    elif any(token.lemma_ in ["estudio", "licenciatura", "estudiar", "formacion"] for token in doc):
        reply = "Estoy estudiando una licenciatura en ingeniería en Ciencia de Datos. Planeo hacer una maestría en AI."
    elif any(token.lemma_ in ["idioma", "hablar"] for token in doc):
        reply = "Hablo inglés y francés de forma fluida. También estoy aprendiendo japonés."
    elif any(token.lemma_ in ["pasión", "apasiona", "gusta", "interesa"] for token in doc) or "ciberseguridad" in user_message_lower:
        reply = "Me apasiona la ciberseguridad y planeo combinarla con AI y Ciencia de Datos para proyectos a mayor escala."
    elif any(token.lemma_ in ["futuro", "plan"] for token in doc):
        reply = "Mi plan a futuro es combinar mis tres habilidades principales: AI, Ciencia de Datos y Ciberseguridad, para lograr proyectos a mayor escala."
    elif any(token.lemma_ in ["hola", "saludo", "que tal"] for token in doc):
        reply = "¡Hola! ¿Cómo puedo ayudarte a conocer el trabajo de Vanessa Ferrer?"
    
    # Si SpaCy no encontró una respuesta, usamos OpenAI como fallback
    if not reply and openai and OPENAI_KEY:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini", # Puedes cambiar el modelo
                messages=[
                    {"role": "system", "content": "Eres el asistente de Vanessa."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.2,
            )
            reply = resp['choices'][0]['message']['content']
        except Exception as e:
            print("Error en OpenAI:", e)
            reply = "Lo siento, no puedo contactar al motor de IA ahora. Intenta más tarde."

    # Si SpaCy y OpenAI no pueden responder, se usa la respuesta por defecto
    if not reply:
        reply = "No estoy seguro de haber entendido. ¿Podrías preguntarme sobre mis habilidades, mi formación, mis idiomas o mis planes a futuro?"
        
    return jsonify({"reply": reply})

# --- Ejecución del servidor ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

