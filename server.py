from flask import Flask, request, jsonify, render_template
import spacy
# Asegúrate de que las carpetas 'static' y 'templates' existan
app = Flask(__name__, static_folder='static', template_folder='templates')
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("El modelo de SpaCy no está instalado. Ejecuta: python -m spacy download es_core_news_sm")
    exit()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
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
    else:
        reply = "No estoy seguro de haber entendido. ¿Podrías preguntarme sobre mis habilidades, mi formación, mis idiomas o mis planes a futuro?"
    return jsonify({"reply": reply})
if __name__ == '__main__':
    app.run(debug=True)
