from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (onde deve estar seu DATABASE_URL)
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIGURAÇÕES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configuração do Banco de Dados Neon
# Certifique-se de que no seu .env a URL comece com postgresql:// (e não postgres://)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    membros = db.Column(db.JSON) # Salva a lista de membros como JSON no banco


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

# --- ROTAS API ---

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Notícias
@app.route('/api/news', methods=['GET'])
def listar_noticias():
    noticias = Noticia.query.all()
    # Ordenação simples por data pode ser feita via SQL se preferir
    return jsonify([{"id": n.id, "titulo": n.titulo, "descricao": n.descricao, "foto": n.foto, "data": n.data} for n in noticias])

@app.route('/api/news', methods=['POST'])
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

# Produtos
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{"id": p.id, "nome": p.nome, "preco": p.preco, "foto": p.foto} for p in produtos])

@app.route('/api/produtos', methods=['POST'])
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

# Transparência
@app.route('/api/transparencia', methods=['GET'])
def get_transparencia():
    docs = Transparencia.query.all()
    return jsonify([{"id": d.id, "titulo": d.titulo, "categoria": d.categoria, "data": d.data, "arquivo": d.arquivo} for d in docs])

@app.route('/api/transparencia', methods=['POST'])
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

# Mensalidade
@app.route('/api/mensalidade', methods=['GET'])
def obter_valor():
    valor = ValorMensalidade.query.first()
    if not valor: return jsonify({})
    return jsonify({"valor_sem_campeonato": valor.valor_sem_campeonato, "valor_com_campeonato": valor.valor_com_campeonato})

@app.route('/api/mensalidade', methods=['POST'])
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

# --- ROTA DIRETORIA (BOARD) ---
@app.route('/api/board', methods=['GET'])
def listar_diretoria():
    # Busca a gestão atual (exemplo simplificado)
    dados = MembroDiretoria.query.order_by(MembroDiretoria.id.desc()).first()
    if not dados:
        return jsonify({"atual": {}, "historico": []})
    return jsonify({"atual": {"periodo": dados.periodo, "presidente": dados.presidente, "membros": dados.membros}, "historico": []})

if __name__ == '__main__':
    print('═' * 50)
    print('  ✓ SERVIDOR CONECTADO AO NEON!')
    print('═' * 50)
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)