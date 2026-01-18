# Site-AAALDV

Repositório destinado à elaboração do site institucional da Associação Atlética Acadêmica Leonardo Da Vinci.

## Especificação Técnica

### Arquitetura
- **Modelo**: Cliente-Servidor
- **Padrão**: API REST + Frontend estático

### Stack Tecnológica

#### Backend
- **Linguagem**: Python 3.8+
- **Framework**: Flask (micro-framework)
- **Armazenamento**: Arquivos JSON (sem banco de dados)
- **Middleware**: Flask-CORS

#### Frontend
- **Tecnologias**: HTML5, CSS3, JavaScript
- **Estilo**: CSS customizado (utility classes)
- **Renderização**: Client-Side

### Estrutura do Projeto
```
MVP-AAALDV/
├── frontend/          # Interface HTML/CSS
│   ├── index.html
│   └── styles.css
└── backend/           # API REST simplificada
    ├── servidor.py    # Servidor Flask (código em português)
    ├── requirements.txt # Dependências Python
    ├── noticias.json  # Dados das notícias
    └── contatos.json  # Dados dos contatos
```

### API Endpoints
- `GET/POST /api/news` - Notícias
- `GET/POST /api/contacts` - Contatos

### Armazenamento
- `news.json` - Array com notícias (id, titulo, conteudo, data)
- `contacts.json` - Array com contatos (id, nome, email, mensagem)

## Requisitos Funcionais

**RF01** - Página Inicial: Apresentação da atlética, links para redes sociais, informações de contato.

**RF02** - Gestão de Conteúdo: Seções "Quem Somos", notícias e informações institucionais.

**RF03** - Formulário de Contato: Sistema para receber mensagens dos visitantes.

**RF04** - Portal de Notícias: Publicação e exibição de notícias da atlética.

## Requisitos Não Funcionais

**RNF01** - Simplicidade: Código limpo e fácil de manter.

**RNF02** - Performance: API leve e rápida com arquivos JSON.

**RNF03** - Manutenibilidade: Estrutura simples para facilitar atualizações.

## Como Usar

### Pré-requisitos
**IMPORTANTE:** Python precisa estar instalado!

**Instalar Python:**
- **Microsoft Store**: Procure "Python 3.12" e instale
- **Site oficial**: https://www.python.org/downloads/
  - Durante instalação, marque "Add Python to PATH"

### Backend
```bash
cd backend
pip install -r requirements.txt
python servidor.py
```

**Link do site:** http://localhost:3000

### Frontend
Abra o arquivo `frontend/index.html` no navegador.

### API Disponível
- `GET http://localhost:3000/api/news` - Lista notícias
- `POST http://localhost:3000/api/news` - Cria notícia
- `GET http://localhost:3000/api/contacts` - Lista contatos
- `POST http://localhost:3000/api/contacts` - Cria contato


