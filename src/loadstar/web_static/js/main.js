function getStats() {
    var req = new XMLHttpRequest();
    req.open('GET', '/stats', false);
    req.send(null);
    return JSON.parse(req.responseText);
}