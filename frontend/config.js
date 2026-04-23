// Configuração centralizada — altere apenas aqui ao trocar de ambiente
const API_URL = 'https://site-aaaldv-back.onrender.com';

// --- Helpers de autenticação ---
function getToken() {
  return sessionStorage.getItem('aaaldv_token');
}

function setToken(token) {
  sessionStorage.setItem('aaaldv_token', token);
}

function removeToken() {
  sessionStorage.removeItem('aaaldv_token');
}

function isLoggedIn() {
  return !!getToken();
}

/**
 * Retorna headers com Authorization para requisições autenticadas.
 * Para FormData, não inclui Content-Type (o browser cuida).
 * Para JSON, inclui Content-Type: application/json.
 */
function authHeaders(isJson = false) {
  const headers = {};
  const token = getToken();
  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }
  if (isJson) {
    headers['Content-Type'] = 'application/json';
  }
  return headers;
}
