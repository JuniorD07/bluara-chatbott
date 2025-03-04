import openai
import json
import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Configuração da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Função para processar mensagens
def chatbot_response(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é um assistente da loja Bluara Modas. Responda às dúvidas dos clientes de forma amigável e profissional."},
                  {"role": "user", "content": message}]
    )
    return response["choices"][0]["message"]["content"]

# Rota principal para testar no navegador
@app.route("/", methods=["GET"])
def home():
    return "🚀 Chatbot Bluara Modas atualizado e rodando!", 200

# Rota para integração com WhatsApp (Twilio)
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()

    if not incoming_msg:
        return "", 400

    bot_reply = chatbot_response(incoming_msg)

    response = MessagingResponse()
    response.message(bot_reply)

    return str(response)

# Rota para integração com o chat do site
@app.route("/chatbot", methods=["POST"])
def site_chatbot():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = chatbot_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Define a porta exigida pelo Render
    app.run(host="0.0.0.0", port=port, debug=True)
