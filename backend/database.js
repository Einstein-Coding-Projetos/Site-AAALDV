const sqlite3 = require('sqlite3').verbose();
const bd = new sqlite3.Database('./banco.db');

bd.serialize(() => {
  bd.run(`CREATE TABLE IF NOT EXISTS noticias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    conteudo TEXT,
    data TEXT
  )`);

  bd.run(`CREATE TABLE IF NOT EXISTS contatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    mensagem TEXT
  )`);
});

module.exports = bd;
