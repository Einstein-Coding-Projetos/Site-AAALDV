from functools import wraps
from hmac import compare_digest
from secrets import token_urlsafe

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

ARQUIVO_NOTICIAS = 'noticias.json'
ARQUIVO_CONTATOS = 'contatos.json'
ADMIN_TOKEN = os.getenv('AAALDV_ADMIN_TOKEN')
ADMIN_USER = os.getenv('AAALDV_ADMIN_USER')
ADMIN_PASSWORD = os.getenv('AAALDV_ADMIN_PASSWORD')
ADMIN_SESSION_MINUTES = int(os.getenv('AAALDV_ADMIN_SESSION_MINUTES', '120'))
SESSOES_ADMIN = {}

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


def agora_ts():
    return datetime.now().timestamp()


def limpar_sessoes_expiradas():
    atual = agora_ts()
    expiradas = [token for token, expira_em in SESSOES_ADMIN.items() if expira_em <= atual]

    for token in expiradas:
        SESSOES_ADMIN.pop(token, None)


def token_sessao_valido(token):
    if not token:
        return False

    limpar_sessoes_expiradas()
    expira_em = SESSOES_ADMIN.get(token)
    if not expira_em:
        return False

    return expira_em > agora_ts()


def emitir_sessao_admin():
    token = token_urlsafe(32)
    expira_em = agora_ts() + (ADMIN_SESSION_MINUTES * 60)
    SESSOES_ADMIN[token] = expira_em
    return token, int(expira_em)


def token_recebido():
    authorization = request.headers.get('Authorization', '')
    bearer = ''

    if authorization.lower().startswith('bearer '):
        bearer = authorization[7:].strip()

    return request.headers.get('X-Admin-Token') or bearer


def rota_admin_protegida(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        possui_config_token = bool(ADMIN_TOKEN)
        possui_config_login = bool(ADMIN_USER and ADMIN_PASSWORD)

        if not possui_config_token and not possui_config_login:
            return jsonify({
                'erro': 'Seguranca admin nao configurada no servidor.',
                'configuracao': 'Defina AAALDV_ADMIN_TOKEN ou AAALDV_ADMIN_USER/AAALDV_ADMIN_PASSWORD.'
            }), 503

        token = token_recebido()
        token_fixo_valido = bool(ADMIN_TOKEN and token and compare_digest(token, ADMIN_TOKEN))
        sessao_valida = token_sessao_valido(token)

        if not token_fixo_valido and not sessao_valida:
            return jsonify({'erro': 'Acesso nao autorizado.'}), 401

        return func(*args, **kwargs)

    return wrapper


@app.route('/api/admin/login', methods=['POST'])
def login_admin():
    if not ADMIN_USER or not ADMIN_PASSWORD:
        return jsonify({
            'erro': 'Login admin nao configurado no servidor.',
            'configuracao': 'Defina AAALDV_ADMIN_USER e AAALDV_ADMIN_PASSWORD.'
        }), 503

    dados = request.get_json(silent=True) or {}
    usuario = str(dados.get('usuario') or '').strip()
    senha = str(dados.get('senha') or '')

    if not compare_digest(usuario, ADMIN_USER) or not compare_digest(senha, ADMIN_PASSWORD):
        return jsonify({'erro': 'Credenciais invalidas.'}), 401

    token, expira_em = emitir_sessao_admin()
    return jsonify({
        'token': token,
        'tipo': 'Bearer',
        'expira_em': expira_em,
        'expira_em_iso': datetime.fromtimestamp(expira_em).isoformat(),
    })


@app.route('/api/admin/logout', methods=['POST'])
def logout_admin():
    token = token_recebido()
    if token:
        SESSOES_ADMIN.pop(token, None)

    return jsonify({'ok': True})


@app.route('/api/admin/verify', methods=['GET'])
@rota_admin_protegida
def verify_admin():
    return jsonify({'ok': True})

@app.route('/api/news', methods=['GET'])
def listar_noticias():
    noticias = ler_dados(ARQUIVO_NOTICIAS)
    return jsonify(noticias)

@app.route('/api/news', methods=['POST'])
@rota_admin_protegida
def criar_noticia():
    dados = request.get_json(silent=True) or {}

    noticias = ler_dados(ARQUIVO_NOTICIAS)
    nova_noticia = {
        'id': int(datetime.now().timestamp() * 1000),
        'titulo': dados.get('titulo'),
        'conteudo': dados.get('conteudo'),
        'data': datetime.now().strftime('%d/%m/%Y')
    }
    noticias.append(nova_noticia)
    salvar_dados(ARQUIVO_NOTICIAS, noticias)
    return jsonify(nova_noticia), 201

@app.route('/api/contacts', methods=['GET'])
@rota_admin_protegida
def listar_contatos():
    contatos = ler_dados(ARQUIVO_CONTATOS)
    return jsonify(contatos)

@app.route('/api/contacts', methods=['POST'])
def criar_contato():
    dados = request.get_json(silent=True) or {}

    contatos = ler_dados(ARQUIVO_CONTATOS)
    novo_contato = {
        'id': int(datetime.now().timestamp() * 1000),
        'nome': dados.get('nome'),
        'email': dados.get('email'),
        'mensagem': dados.get('mensagem')
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
    print('  🔐 Admin login: POST /api/admin/login com usuario/senha')
    print('  🔐 Admin auth: X-Admin-Token ou Authorization: Bearer <token>')
    print('═' * 50)
    app.run(debug=True, port=3000)
