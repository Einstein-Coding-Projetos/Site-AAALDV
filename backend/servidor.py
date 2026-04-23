from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from werkzeug.utils import secure_filename
from functools import wraps
import os
import jwt
import bcrypt
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (onde deve estar seu DATABASE_URL)
load_dotenv()

app = Flask(__name__)

# --- CORS RESTRITO ---
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'https://site-aaaldv-frontend.onrender.com,https://site-aaaldv.onrender.com,http://localhost:5500,http://127.0.0.1:5500').split(',')
CORS(app, origins=ALLOWED_ORIGINS)

# --- CONFIGURAÇÕES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configuração do Banco de Dados Neon
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Segredos para autenticação
JWT_SECRET = os.getenv('JWT_SECRET', 'troque-este-segredo-em-producao')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '')

db = SQLAlchemy(app)

# --- MODELOS DO BANCO DE DADOS ---

class Noticia(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(500))
    data = db.Column(db.String(20))

class Produto(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.String(50), nullable=False)
    foto = db.Column(db.String(500))

class Transparencia(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(100))
    data = db.Column(db.String(20))
    arquivo = db.Column(db.String(500))

class Carrossel(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    legenda = db.Column(db.String(255))

class ValorMensalidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor_sem_campeonato = db.Column(db.String(50))
    valor_com_campeonato = db.Column(db.String(50))

class MembroDiretoria(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    periodo = db.Column(db.String(100))
    presidente = db.Column(db.String(100))
    membros = db.Column(db.JSON)


# Cria as tabelas se não existirem
with app.app_context():
    db.create_all()

# --- FUNÇÕES AUXILIARES ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = int(datetime.now().timestamp() * 1000)
        filename = f"{timestamp}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"/uploads/{filename}"
    return None

def delete_uploaded_file(file_path):
    """Remove o arquivo do disco quando um registro é deletado."""
    if file_path:
        # file_path vem como "/uploads/nome_do_arquivo"
        filename = file_path.replace('/uploads/', '')
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except OSError:
                pass

# --- AUTENTICAÇÃO ---
def require_auth(f):
    """Decorator que protege rotas POST/DELETE exigindo JWT válido."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token não fornecido'}), 401
        token = auth_header.split(' ', 1)[1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    """Autentica com senha única compartilhada e retorna JWT (8h)."""
    data = request.get_json(silent=True) or {}
    senha = data.get('senha', '')

    if not ADMIN_PASSWORD:
        return jsonify({'error': 'Senha de admin não configurada no servidor'}), 500

    # ADMIN_PASSWORD no env deve ser o hash bcrypt da senha
    # Para gerar: python -c "import bcrypt; print(bcrypt.hashpw(b'sua-senha', bcrypt.gensalt()).decode())"
    try:
        if not bcrypt.checkpw(senha.encode('utf-8'), ADMIN_PASSWORD.encode('utf-8')):
            return jsonify({'error': 'Senha incorreta'}), 401
    except (ValueError, TypeError):
        return jsonify({'error': 'Senha incorreta'}), 401

    token = jwt.encode(
        {'exp': datetime.now(timezone.utc) + timedelta(hours=8)},
        JWT_SECRET,
        algorithm='HS256'
    )
    return jsonify({'token': token}), 200


# --- ROTAS API ---

@app.route('/')
def index():
    return jsonify({"status": "online", "message": "API AAALDV funcionando!"})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Notícias
@app.route('/api/news', methods=['GET'])
def listar_noticias():
    noticias = Noticia.query.order_by(Noticia.id.desc()).all()
    return jsonify([{"id": n.id, "titulo": n.titulo, "descricao": n.descricao, "foto": n.foto, "data": n.data} for n in noticias])

@app.route('/api/news', methods=['POST'])
@require_auth
def criar_noticia():
    foto_url = save_uploaded_file(request.files.get('foto'))
    nova = Noticia(
        id=int(datetime.now().timestamp() * 1000),
        titulo=request.form.get('titulo'),
        descricao=request.form.get('descricao'),
        foto=foto_url,
        data=request.form.get('data', datetime.now().strftime('%d/%m/%Y'))
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({"message": "Notícia criada"}), 201

@app.route('/api/news/<int:id>', methods=['DELETE'])
@require_auth
def deletar_noticia(id):
    noticia = Noticia.query.get_or_404(id)
    delete_uploaded_file(noticia.foto)
    db.session.delete(noticia)
    db.session.commit()
    return jsonify({"message": "Notícia deletada"}), 200

# Produtos
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{"id": p.id, "nome": p.nome, "preco": p.preco, "foto": p.foto} for p in produtos])

@app.route('/api/produtos', methods=['POST'])
@require_auth
def criar_produto():
    foto_url = save_uploaded_file(request.files.get('foto'))
    novo = Produto(
        id=int(datetime.now().timestamp() * 1000),
        nome=request.form.get('nome'),
        preco=request.form.get('preco'),
        foto=foto_url
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Produto criado"}), 201

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
@require_auth
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    delete_uploaded_file(produto.foto)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({"message": "Produto deletado"}), 200

# Transparência
@app.route('/api/transparencia', methods=['GET'])
def get_transparencia():
    docs = Transparencia.query.order_by(Transparencia.id.desc()).all()
    return jsonify([{"id": d.id, "titulo": d.titulo, "categoria": d.categoria, "data": d.data, "arquivo": d.arquivo} for d in docs])

@app.route('/api/transparencia', methods=['POST'])
@require_auth
def criar_transparencia():
    arquivo_url = save_uploaded_file(request.files.get('arquivo'))
    novo = Transparencia(
        id=int(datetime.now().timestamp() * 1000),
        titulo=request.form.get('titulo'),
        categoria=request.form.get('categoria'),
        data=request.form.get('data'),
        arquivo=arquivo_url
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Documento adicionado"}), 201

@app.route('/api/transparencia/<int:id>', methods=['DELETE'])
@require_auth
def deletar_transparencia(id):
    doc = Transparencia.query.get_or_404(id)
    delete_uploaded_file(doc.arquivo)
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"message": "Documento deletado"}), 200

# Mensalidade
@app.route('/api/mensalidade', methods=['GET'])
def obter_valor():
    valor = ValorMensalidade.query.first()
    if not valor: return jsonify({})
    return jsonify({"valor_sem_campeonato": valor.valor_sem_campeonato, "valor_com_campeonato": valor.valor_com_campeonato})

@app.route('/api/mensalidade', methods=['POST'])
@require_auth
def alterar_valor():
    valor = ValorMensalidade.query.first()
    if not valor:
        valor = ValorMensalidade()
        db.session.add(valor)

    valor.valor_sem_campeonato = request.json.get('valor_sem_campeonato')
    valor.valor_com_campeonato = request.json.get('valor_com_campeonato')
    db.session.commit()
    return jsonify({"message": "Valor atualizado"}), 201

# --- ROTA CARROSSEL ---
@app.route('/api/carousel', methods=['GET'])
def listar_carrossel():
    fotos = Carrossel.query.all()
    return jsonify([{"id": f.id, "url": f.url, "legenda": f.legenda} for f in fotos])

@app.route('/api/carousel', methods=['POST'])
@require_auth
def criar_carrossel():
    try:
        foto_url = save_uploaded_file(request.files.get('foto'))
        if not foto_url:
            return jsonify({'error': 'Arquivo inválido ou ausente'}), 400

        nova_foto = Carrossel(
            id=int(datetime.now().timestamp() * 1000),
            url=foto_url,
            legenda=request.form.get('legenda', 'Sem legenda')
        )
        db.session.add(nova_foto)
        db.session.commit()
        return jsonify({"id": nova_foto.id, "url": nova_foto.url}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/carousel/<int:id>', methods=['DELETE'])
@require_auth
def deletar_carrossel(id):
    foto = Carrossel.query.get_or_404(id)
    delete_uploaded_file(foto.url)
    db.session.delete(foto)
    db.session.commit()
    return jsonify({"message": "Foto deletada"}), 200

# --- ROTA DIRETORIA (BOARD) ---
@app.route('/api/board', methods=['GET'])
def listar_diretoria():
    dados = MembroDiretoria.query.order_by(MembroDiretoria.id.desc()).first()
    if not dados:
        return jsonify({"atual": {}, "historico": []})
    return jsonify({"atual": {"periodo": dados.periodo, "presidente": dados.presidente, "membros": dados.membros}, "historico": []})

@app.route('/api/board/atual', methods=['POST'])
@require_auth
def salvar_gestao_atual():
    data = request.get_json(silent=True) or {}
    novo = MembroDiretoria(
        id=int(datetime.now().timestamp() * 1000),
        periodo=data.get('periodo'),
        presidente=data.get('presidente'),
        membros=data.get('membros', [])
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Gestão salva"}), 201

@app.route('/api/board/archive', methods=['POST'])
@require_auth
def arquivar_gestao():
    return jsonify({"message": "Gestão arquivada"}), 200

if __name__ == '__main__':
    print('=' * 50)
    print('  SERVIDOR CONECTADO AO NEON!')
    print('=' * 50)
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
