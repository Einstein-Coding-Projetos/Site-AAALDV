const express = require('express');
const router = express.Router();
const bd = require('../database');

router.get('/', (req, res) => {
  bd.all('SELECT * FROM noticias ORDER BY data DESC', (erro, linhas) => {
    if (erro) return res.status(500).json({ erro: erro.message });
    res.json(linhas);
  });
});

router.post('/', (req, res) => {
  const { titulo, conteudo, data } = req.body;
  bd.run('INSERT INTO noticias (titulo, conteudo, data) VALUES (?, ?, ?)',
    [titulo, conteudo, data],
    function(erro) {
      if (erro) return res.status(500).json({ erro: erro.message });
      res.json({ id: this.lastID });
    }
  );
});

module.exports = router;
