
import json
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


#infos copiadas do Watson assistant
apikey = 'FWS68jd6VrsknbWFgyMAZoWzIyQYuR3BQgD9TOQA3msA'
url = 'https://api.us-south.assistant.watson.cloud.ibm.com'
assistant_id = '1243be61-ea56-483c-9ec8-d431ddc0fe4b'

authenticator = IAMAuthenticator(apikey)

assistant = AssistantV2(
    version = '2018-09-20',
    authenticator=authenticator)
assistant.set_service_url(url)
assistant.set_disable_ssl_verification(True)

session = assistant.create_session(assistant_id).get_result()
session_json = json.dumps(session, indent=2)
session_dict = json.loads(session_json)
session_id = session_dict['session_id']


app = Flask(__name__)

# Função para criar uma nova sessão
def create_session():
    global session_id
    session = assistant.create_session(assistant_id=assistant_id).get_result()
    session_id = session['session_id']


# Função para enviar mensagem ao Watson Assistant
def send_message_to_watson(user_input):
    global session_id
    if session_id is None:
        create_session()

    response = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input={'message_type': 'text', 'text': user_input}
    ).get_result()

    # Extrai a resposta
    message = response['output']['generic'][0]['text']
    return message


@app.route('/')
def index():
    # Primeira resposta do chatbot (você pode mudar isso para uma resposta inicial personalizada)
    return render_template('chat.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form.get('respostaCliente')

    # Envia a mensagem do usuário para o Watson Assistant e obtém a resposta
    chatbot_response = send_message_to_watson(user_input)

    # Retorna a resposta como JSON para o frontend
    return jsonify({'response': chatbot_response})


if __name__ == '__main__':
    app.run(debug=True)