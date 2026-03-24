import json
import os
from servidor import app, db, Noticia, Produto, Transparencia # Importe seus modelos aqui
from dotenv import load_dotenv

load_dotenv()

def migrar_noticias():
    if os.path.exists('noticias.json'):
        with open('noticias.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for item in dados:
                # Evita duplicados se rodar o script 2x
                exists = Noticia.query.get(item['id'])
                if not exists:
                    nova = Noticia(
                        id=item['id'],
                        titulo=item['titulo'],
                        descricao=item['descricao'],
                        foto=item.get('foto'),
                        data=item['data']
                    )
                    db.session.add(nova)
        db.session.commit()
        print("✅ Notícias migradas!")

def migrar_produtos():
    if os.path.exists('produtos.json'):
        with open('produtos.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for item in dados:
                # Supondo que você criou o modelo Produto similar ao Noticia
                nova = Produto(
                    id=item['id'],
                    nome=item['nome'],
                    preco=item['preco'],
                    foto=item.get('foto')
                )
                db.session.add(nova)
        db.session.commit()
        print("✅ Produtos migrados!")

if __name__ == "__main__":
    with app.app_context():
        # Cria as tabelas no Neon antes de migrar
        db.create_all()
        
        print("Iniciando migração para o Neon...")
        migrar_noticias()
        migrar_produtos()
        # Adicione aqui as outras funções (transparência, carrossel, etc)
        print("🚀 Processo finalizado!")