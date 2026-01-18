from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

ARQUIVO_NOTICIAS = 'noticias.json'
ARQUIVO_CONTATOS = 'contatos.json'

for arquivo in [ARQUIVO_NOTICIAS, ARQUIVO_CONTATOS]:
    if not os.path.exists(arquivo):
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump([], f)

def ler_dados(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

@app.route('/api/news', methods=['GET'])
def listar_noticias():
    noticias = ler_dados(ARQUIVO_NOTICIAS)
    return jsonify(noticias)

@app.route('/api/news', methods=['POST'])
def criar_noticia():
    noticias = ler_dados(ARQUIVO_NOTICIAS)
    nova_noticia = {
        'id': int(datetime.now().timestamp() * 1000),
        'titulo': request.json.get('titulo'),
        'conteudo': request.json.get('conteudo'),
        'data': datetime.now().strftime('%d/%m/%Y')
    }
    noticias.append(nova_noticia)
    salvar_dados(ARQUIVO_NOTICIAS, noticias)
    return jsonify(nova_noticia), 201

@app.route('/api/contacts', methods=['GET'])
def listar_contatos():
    contatos = ler_dados(ARQUIVO_CONTATOS)
    return jsonify(contatos)

@app.route('/api/contacts', methods=['POST'])
def criar_contato():
    contatos = ler_dados(ARQUIVO_CONTATOS)
    novo_contato = {
        'id': int(datetime.now().timestamp() * 1000),
        'nome': request.json.get('nome'),
        'email': request.json.get('email'),
        'mensagem': request.json.get('mensagem')
    }
    contatos.append(novo_contato)
    salvar_dados(ARQUIVO_CONTATOS, contatos)
    return jsonify(novo_contato), 201

if __name__ == '__main__':
    print('═' * 50)
    print('  ✓ SERVIDOR RODANDO COM SUCESSO!')
    print('═' * 50)
    print('  🌐 Site: http://localhost:3000')
    print('  📰 API Notícias: http://localhost:3000/api/news')
    print('  📧 API Contatos: http://localhost:3000/api/contacts')
    print('═' * 50)
    app.run(debug=True, port=3000)
