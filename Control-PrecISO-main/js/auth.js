// js/auth.js
// FUNCIONES PARA AUTENTICACIÓN CON COGNITO (API DIRECTA)

function getAccessToken() {
    return localStorage.getItem('access_token') || localStorage.getItem('id_token');
}

function authHeaders(extraHeaders = {}) {
    const headers = { ...extraHeaders };
    const token = getAccessToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

function handleUnauthorized() {
    logout();
}

/** Petición a API propia (API Gateway); añade token y gestiona 401. */
async function apiFetch(url, options = {}) {
    const opts = { ...options };
    opts.headers = authHeaders(opts.headers || {});
    const response = await fetch(url, opts);
    if (response.status === 401) {
        handleUnauthorized();
    }
    return response;
}

function isApiGatewayUrl(url) {
    const u = String(url);
    return u.includes('execute-api') || (u.includes('amazonaws.com') && !u.includes('cognito-idp'));
}

async function login(email, password) {
    try {
        const response = await fetch(`https://cognito-idp.${COGNITO_CONFIG.region}.amazonaws.com/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-amz-json-1.1',
                'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth'
            },
            body: JSON.stringify({
                AuthFlow: 'USER_PASSWORD_AUTH',
                ClientId: COGNITO_CONFIG.clientId,
                AuthParameters: {
                    USERNAME: email,
                    PASSWORD: password
                }
            })
        });

        if (!response.ok) {
            const error = await response.json();
            console.error('Error response:', error);

            if (error.message === 'User does not exist') {
                throw new Error('El usuario no existe');
            } else if (error.message === 'Incorrect username or password') {
                throw new Error('Contraseña incorrecta');
            } else if (error.message === 'User is not confirmed') {
                throw new Error('El usuario no ha confirmado su email. Revisa tu bandeja de entrada.');
            } else {
                throw new Error(error.message || 'Error al iniciar sesión');
            }
        }

        const data = await response.json();

        localStorage.setItem('access_token', data.AuthenticationResult.AccessToken);
        localStorage.setItem('id_token', data.AuthenticationResult.IdToken);
        localStorage.setItem('user_email', email);

        return { success: true };

    } catch (error) {
        console.error('Error en login:', error);
        return { success: false, error: error.message };
    }
}

function isAuthenticated() {
    const token = localStorage.getItem('access_token');
    if (!token) return false;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const expirado = payload.exp * 1000 < Date.now();
        return !expirado;
    } catch {
        return false;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('id_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_email');
    window.location.href = 'index.html';
}

function getUserEmail() {
    return localStorage.getItem('user_email');
}

function getUserRole() {
    const token = localStorage.getItem('id_token');
    if (!token) return null;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const groups = payload['cognito:groups'] || [];
        if (groups.includes('Superadmin')) return 'Superadmin';
        if (groups.includes('AdminEmpresa')) return 'AdminEmpresa';
        if (groups.includes('UsuarioEmpresa')) return 'UsuarioEmpresa';
        return null;
    } catch (error) {
        console.error('Error al decodificar token:', error);
        return null;
    }
}

async function getEmpresaId() {
    const token = getAccessToken();
    if (!token) {
        console.error('No hay token de acceso');
        return null;
    }

    try {
        const response = await apiFetch('https://cf759ojbfj.execute-api.us-east-1.amazonaws.com/V1/usuarios/empresa', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            console.error('Error al obtener empresa_id:', response.status);
            return null;
        }

        const data = await response.json();
        console.log('Empresa ID recibido:', data.empresa_id);
        return data.empresa_id;
    } catch (error) {
        console.error('Error en getEmpresaId:', error);
        return null;
    }
}
