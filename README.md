# Site-AAALDV
Repositório destinado a elaboração do projeto do site institucional da entidade Associação Atlética Acadêmica Leonardo Da Vinci

Especificação Técnica - Site AAALDV 
1. Arquitetura do Sistema
Modelo Arquitetural: Cliente-Servidor tradicional.

Padrão de Projeto (Backend): MVC (Model-View-Controller) adaptado para C++ web development.

O servidor C++ processará as requisições, manipulará a lógica de negócios e gerará o HTML de resposta diretamente.

2. Stack Tecnológica
2.1. Backend (Camada de Aplicação)
Linguagem: C++ 

Framework Web C++: 

Drogon: Framework HTTP de alta performance, full-stack .

Oat++: Leve, focado em performance e zero dependências pesadas.


Gerenciamento de Dependências C++: Conan ou Vcpkg 

2.2. Frontend (Camada de Apresentação)
Tecnologias Base: HTML5, CSS3, JavaScript puro (Vanilla JS).

Renderização: Server-Side Rendering (SSR) gerado pela aplicação C++.

O backend C++ irá ler arquivos de template HTML, injetar os dados dinâmicos (ex: nome do usuário, lista de notícias) e enviar o HTML final para o navegador.

Template Engine C++: Necessário para facilitar a injeção de dados no HTML sem "macarrão de código". 

2.3. Banco de Dados (Camada de Dados)
SGBD: PostgreSQL.

Interface de Conexão C++: libpqxx (biblioteca oficial C++ para PostgreSQL) ou um ORM C++ como ODB ou SOCI (para facilitar o mapeamento objeto-relacional, embora menos maduros que os de outras linguagens).

3. Ambiente de Desenvolvimento e Ferramentas
IDE: Visual Studio (Windows), CLion (Multiplataforma) ou VS Code com extensões C/C++ e CMake.

Sistema de Build: CMake (Padrão da indústria para C++, garante que o projeto compile igual no Windows, macOS e Linux).

Compilador: GCC/Clang (Linux/macOS) ou MSVC (Windows).







Requisitos Funcionais


RF01 - Página Inicial (Home): O site deve ter uma página inicial contendo uma breve introdução sobre a atlética, links para redes sociais, e um rodapé com contatos, CNPJ e endereço.

RF02 - Gestão de Conteúdo Institucional: O sistema deve permitir a publicação de informações sobre "Quem somos" , a atual "Diretoria" , as "Modalidades" esportivas oferecidas e uma "Galeria" de fotos/vídeos.

RF03 - Área de Parceiros: Deve haver uma seção dedicada para listar "Nossas parcerias" e uma página com informações sobre como "Seja um patrocinador".

RF04 - Portal da Transparência: O site deve disponibilizar arquivos para download ou visualização referentes ao "Estatuto" da atlética , "ATAS" de reuniões e "Relatório Financeiro".

RF05 - Autenticação de Sócios: O sistema deve possuir uma funcionalidade de Login e Senha para restringir o acesso à "Área Sócio".

RF06 - Loja Virtual/Exclusiva: Deve haver uma seção de "Loja" acessível aos sócios  

RF07 - Mural de Comunicados: O sistema deve permitir que a administração publique "Comunicados" exclusivos para os sócios logados.

RF08 - Contatos Estratégicos: Disponibilização de informações de contato direto de "Diretores e presidência" apenas para usuários autenticados.


Requisitos Não Funcionais 


RNF01 - Responsividade (Usabilidade): O site deve ser totalmente responsivo, adaptando-se perfeitamente a dispositivos móveis (celulares e tablets)Futuramente!

RNF02 - Segurança: A área de login  deve utilizar protocolos seguros (HTTPS/SSL) e criptografia de senhas para proteger os dados dos sócios.

RNF03 - Facilidade de Gestão (Manutenibilidade): O sistema deve possuir um painel administrativo  intuitivo para que a própria diretoria possa atualizar textos, subir atas e relatórios financeiros  sem depender sempre de desenvolvedores.
