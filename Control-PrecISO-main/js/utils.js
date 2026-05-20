// Utilidades compartidas — mitigación XSS (V-004, V-005)
function escapeHtml(text) {
    if (text == null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

function showLoadError(elementId, message) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = '';
    const div = document.createElement('div');
    div.style.color = '#dc2626';
    div.textContent = 'Error: ' + message;
    el.appendChild(div);
}
