const express = require('express');
const router = express.Router();
const bd = require('../database');

router.get('/', (req, res) => {
  bd.all('SELECT * FROM contatos', (erro, linhas) => {
    if (erro) return res.status(500).json({ erro: erro.message });
    res.json(linhas);
  });
});

router.post('/', (req, res) => {
  const { nome, email, mensagem } = req.body;
  bd.run('INSERT INTO contatos (nome, email, mensagem) VALUES (?, ?, ?)',
    [nome, email, mensagem],
    function(erro) {
      if (erro) return res.status(500).json({ erro: erro.message });
      res.json({ id: this.lastID });
    }
  );
});

module.exports = router;
