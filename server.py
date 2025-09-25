import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import spacy

try:
    import openai
except ImportError:
    openai = None
    print("OpenAI no está instalado. Se usarán solo reglas de SpaCy.")

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("El modelo de SpaCy no está instalado. Ejecuta 'python -m spacy download es_core_news_sm'")
    exit()

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
if openai and OPENAI_KEY:
    openai.api_key = OPENAI_KEY
    print("API de OpenAI configurada. El chatbot la usará como fallback.")
else:
    print("No se encontró la clave de OpenAI. El chatbot solo usará reglas de SpaCy.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "No se proporcionó un mensaje"}), 400

    doc = nlp(user_message)
    reply = ""
    user_message_lower = user_message.lower()

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

    if not reply and openai and OPENAI_KEY:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
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

    if not reply:
        reply = "No estoy seguro de haber entendido. ¿Podrías preguntarme sobre mis habilidades, mi formación, mis idiomas o mis planes a futuro?"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
