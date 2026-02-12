from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

ARQUIVO_NOTICIAS = 'noticias.json'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(ARQUIVO_NOTICIAS):
    with open(ARQUIVO_NOTICIAS, 'w', encoding='utf-8') as f:
        json.dump([], f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ler_dados(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/news', methods=['GET'])
def listar_noticias():
    noticias = ler_dados(ARQUIVO_NOTICIAS)
    noticias_sorted = sorted(noticias, key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'), reverse=True)
    return jsonify(noticias_sorted)

@app.route('/api/news', methods=['POST'])
def criar_noticia():
    try:
        noticias = ler_dados(ARQUIVO_NOTICIAS)
        
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        
        if not titulo or not descricao:
            return jsonify({'error': 'Título e descrição são obrigatórios'}), 400
        
        foto_url = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = int(datetime.now().timestamp() * 1000)
                filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto_url = f"/uploads/{filename}"
        
        data = request.form.get('data', datetime.now().strftime('%d/%m/%Y'))
        
        nova_noticia = {
            'id': int(datetime.now().timestamp() * 1000),
            'titulo': titulo,
            'descricao': descricao,
            'foto': foto_url,
            'data': data
        }
        
        noticias.append(nova_noticia)
        salvar_dados(ARQUIVO_NOTICIAS, noticias)
        return jsonify(nova_noticia), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/news/<int:noticia_id>', methods=['DELETE'])
def deletar_noticia(noticia_id):
    noticias = ler_dados(ARQUIVO_NOTICIAS)
    noticias = [n for n in noticias if n['id'] != noticia_id]
    salvar_dados(ARQUIVO_NOTICIAS, noticias)
    return jsonify({'message': 'Notícia deletada com sucesso'}), 200

if __name__ == '__main__':
    print('═' * 50)
    print('  ✓ SERVIDOR RODANDO COM SUCESSO!')
    print('═' * 50)
    print('  🌐 Site: http://localhost:3000')
    print('  📰 API Notícias: http://localhost:3000/api/news')
    print('  📁 Uploads: http://localhost:3000/uploads/')
    print('═' * 50)
    app.run(debug=True, port=3000)
