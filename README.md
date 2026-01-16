# Site-AAALDV

Repositório destinado à elaboração do site institucional da Associação Atlética Acadêmica Leonardo Da Vinci.

## Especificação Técnica

### Arquitetura
- **Modelo**: Cliente-Servidor
- **Padrão**: API REST + Frontend estático

### Stack Tecnológica

#### Backend
- **Runtime**: Node.js
- **Framework**: Express.js
- **Banco de Dados**: SQLite3
- **Middleware**: CORS

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
└── backend/           # API REST
    ├── routes/        # Endpoints
    ├── server.js
    ├── database.js
    └── package.json
```

### API Endpoints
- `GET/POST /api/news` - Notícias
- `GET/POST /api/contacts` - Contatos

### Tabelas do Banco
- `noticias` (id, titulo, conteudo, data)
- `contatos` (id, nome, email, mensagem)

## Requisitos Funcionais

**RF01** - Página Inicial: Apresentação da atlética, links para redes sociais, informações de contato.

**RF02** - Gestão de Conteúdo: Seções "Quem Somos", notícias e informações institucionais.

**RF03** - Formulário de Contato: Sistema para receber mensagens dos visitantes.

**RF04** - Portal de Notícias: Publicação e exibição de notícias da atlética.

## Requisitos Não Funcionais

**RNF01** - Simplicidade: Código limpo e fácil de manter.

**RNF02** - Performance: API leve e rápida com SQLite.

**RNF03** - Manutenibilidade: Estrutura simples para facilitar atualizações.

## Como Usar

### Backend
```bash
cd backend
npm install
npm start
```
Servidor: `http://localhost:3000`

### Frontend
Abra `frontend/index.html` no navegador.

## Tecnologias em Português
Todo código backend traduzido para português (variáveis, tabelas, campos).
