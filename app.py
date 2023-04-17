
import openai
from flask import request, jsonify, Flask, make_response
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}},
     methods={"POST", "GET"}, supports_credentials=True)

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = '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'




@app.route('/', methods=['GET', 'POST'])
def index():
    return make_response(jsonify('Server Online'), 200)


@app.route('/api/report', methods=['GET', 'POST'])
def report():
    json_data = request.get_json()
    content = json_data['content']    

    # if len(content) > 2000:
    #     print("arquivo muito grande :" + str(len(content)))
    #     response = make_response(jsonify("Arquivo muito grande"), 400)
    #     return response
    # separa as frases

    phrases = content.splitlines()
    # gera o pronpt para a api
    prompt = generate_prompt(phrases)

    print('prompt length: ' + str(len(prompt)))

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.2,
    )
    print(response)
    return make_response(jsonify(response.choices[0].text), 200)


def generate_prompt(phrases_list):
    prompt_string = ''
    for i in phrases_list:
        prompt_string = prompt_string + ' \n '+i

    return """ Tenho uma lista de comentários em português do Brasil sobre uma marca de cerveja, com cada linha representando um comentário diferente.
Analise esses comentários e crie um novo comentário que melhor represente o sentimento médio expresso na lista, utilizando o máximo de palavras e frases encontradas nos comentários originais.
O objetivo é gerar um comentário que resuma de forma geral as opiniões das pessoas sobre a marca de cerveja.
Lista de comentários: {}
""".format(prompt_string)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
