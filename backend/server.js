const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/news', require('./routes/news'));
app.use('/api/contacts', require('./routes/contacts'));

app.listen(3000, () => console.log('Servidor na porta 3000'));

module.exports = app;
