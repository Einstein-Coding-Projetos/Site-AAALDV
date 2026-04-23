# Site-AAALDV

Repositório destinado ao site institucional da Associação Atlética Acadêmica Leonardo Da Vinci.

## Especificação Técnica

### Arquitetura
- **Modelo**: Cliente-Servidor
- **Padrão**: API REST + Frontend estático

### Stack Tecnológica

#### Backend
- **Linguagem**: Python 3.8+
- **Framework**: Flask (micro-framework)
- **Banco de Dados**: PostgreSQL (Neon - serverless)
- **ORM**: SQLAlchemy
- **Autenticação**: JWT (PyJWT) + bcrypt
- **Middleware**: Flask-CORS (restrito por domínio)
- **Deploy**: Render

#### Frontend
- **Tecnologias**: HTML5, CSS3, JavaScript
- **Estilo**: CSS customizado (utility classes)
- **Renderização**: Client-Side
- **Auth**: JWT armazenado em sessionStorage

### Estrutura do Projeto
```
Site-AAALDV/
├── frontend/
│   ├── index.html           # Página inicial + carrossel
│   ├── institucional.html   # Quem somos + diretoria
│   ├── liga.html            # Liga Einstein + modalidades
│   ├── eventos.html         # Eventos e galeria
│   ├── produtos.html        # Loja de produtos
│   ├── transparencia.html   # Documentos e relatórios
│   ├── admin.html           # Painel administrativo (protegido por senha)
│   ├── config.js            # URL da API centralizada + helpers de auth
│   ├── styles.css           # Estilos globais
│   └── assets/              # Imagens e fontes
└── backend/
    ├── servidor.py          # API Flask + modelos + autenticação
    ├── requirements.txt     # Dependências Python
    ├── uploads/             # Arquivos enviados pelo admin
    └── migrar_dados.py      # Script de migração de dados
```

### Variáveis de Ambiente (backend)
| Variável | Obrigatória | Descrição |
|---|---|---|
| `DATABASE_URL` | Sim | Connection string PostgreSQL (Neon) |
| `ADMIN_PASSWORD` | Sim | Hash bcrypt da senha de admin |
| `JWT_SECRET` | Sim | Segredo para assinar tokens JWT |
| `ALLOWED_ORIGINS` | Não | Domínios permitidos no CORS (default: `https://site-aaaldv.onrender.com`) |
| `PORT` | Não | Porta do servidor (default: 3000) |
| `FLASK_DEBUG` | Não | Ativar modo debug (default: false) |

#### Gerando o hash da senha de admin
```bash
python -c "import bcrypt; print(bcrypt.hashpw(b'sua-senha-aqui', bcrypt.gensalt()).decode())"
```
Copie o resultado e configure como `ADMIN_PASSWORD` no Render.

### API Endpoints

#### Públicas (GET)
- `GET /api/news` - Lista notícias (ordenadas por mais recente)
- `GET /api/produtos` - Lista produtos
- `GET /api/transparencia` - Lista documentos (ordenados por mais recente)
- `GET /api/carousel` - Lista fotos do carrossel
- `GET /api/mensalidade` - Valores de mensalidade
- `GET /api/board` - Diretoria atual e histórico

#### Autenticadas (requer header `Authorization: Bearer <token>`)
- `POST /api/login` - Autentica com senha e retorna JWT (8h)
- `POST /api/news` - Cria notícia
- `DELETE /api/news/:id` - Remove notícia
- `POST /api/produtos` - Cria produto
- `DELETE /api/produtos/:id` - Remove produto
- `POST /api/transparencia` - Adiciona documento
- `DELETE /api/transparencia/:id` - Remove documento
- `POST /api/carousel` - Adiciona foto ao carrossel
- `DELETE /api/carousel/:id` - Remove foto do carrossel
- `POST /api/mensalidade` - Atualiza valores de mensalidade
- `POST /api/board/atual` - Salva gestão atual
- `POST /api/board/archive` - Arquiva gestão

## Como Usar

### Pré-requisitos
- Python 3.8+ instalado
- Banco de dados PostgreSQL (ou conta no Neon)

### Desenvolvimento local
```bash
cd backend
pip install -r requirements.txt

# Crie um arquivo .env com:
# DATABASE_URL=postgresql://...
# ADMIN_PASSWORD=$2b$12$... (hash bcrypt)
# JWT_SECRET=um-segredo-forte

python servidor.py
```

O servidor roda em `http://localhost:3000`.

### Frontend
Abra `frontend/index.html` no navegador, ou sirva via servidor estático.

### Deploy (Render)
1. Backend: deploy como Web Service apontando para `backend/`
2. Frontend: deploy como Static Site apontando para `frontend/`
3. Configure as variáveis de ambiente no dashboard do Render
