function getEndpoint(endpointName, callback) {
    fetch('/' + endpointName).then(function(response) {
        callback(response);
    });
}

function getEndpointJson(endpointName, callback) {
    getEndpoint(endpointName, function(resp) {
        resp.json().then(function(data) {
            callback(data);
        });
    });
}

function getStats(callback) {
    getEndpointJson('stats.json', function(data) {
        callback(data);
    })
}

function sendAction(action, callback = undefined) {
    getEndpoint('action/' + action, function() {
        if (callback != undefined) {
            callback();
        }
    });
}

function quit() {
    document.getElementById('controlPanel').innerHTML = 'Shutting down...';
    document.getElementById('statsPanelContainer').style.display = 'none';
    document.getElementById('logPanelContainer').style.display = 'none';
    document.getElementById('videoPlaybackContainer').style.display = 'none';
    clearInterval(window.logInterval);
    clearInterval(window.statsInterval);
    sendAction("quit", function() {
        document.getElementById('controlPanel').innerHTML = 'Done! Goodbye!';
    });
}

function getLog(callback) {
    var req = new XMLHttpRequest();
    getEndpoint('log.html', function(response) {
        response.text().then(function(text) {
            callback(text);
        });
    })
}

function updateLog() {
    getLog(function(text) {
        document.getElementById("log-box").innerHTML = text;
    })
}

function updateStats() {
    let out = "<p><b>Note!</b><br>These stats only update every 0.25 seconds.<br>If your livesplit is accurate, then we're all good on capturing!</p><p><b>What do these stats mean?</b><p><p><code>loadingColour</code> refers to the black level the entire picture needs to be for the scene to be determined as \"loading\".</p><p><code>loading</code> is whether the current picture is being detected as loading - again, there's latency here, but it's more of a litmus test if you are trying to calibrate using a screenshot of a load black screen.</p><p><code>frameInterval</code> is the amount of frames LoadStar will check on - a value of 2 will mean LoadStar will check every 2 frames for loading. This exists for performance reasons, and that generally this at a value of 2 will not cause any timing differences over a run, just because of the laws of proability. However, setting it too high may cause your loads to be missed, so try to keep it at the default of 2 or lower.</p><p><code>fps</code> is the current framerate we're processing frames at. We target 30fps for processing.</p><p><code>capturing</code> is whether the LoadStar backend is telling us it has a camera feed. If your preview is garbled, but this says capturing, it's likely something has gone wrong somewhere with your camera feed into LoadStar, or with this web UI.";
    getStats(function(stats) {
        function freshStats() {
            return stats;
        }
        let p = document.getElementById("player")
        if (stats.capturing) {
            if (p.getAttribute("src") != "/video") {
                p.setAttribute("src", "/video");
            }
        } else {
            if (p.getAttribute("src") != "#") {
                p.setAttribute("src", "#");
            }
        }
        console.log(stats);
        for (const key in stats) {
            out = `<code>${key}</code> : <code>${stats[key]}</code><br>` + out
        }

        document.getElementById("stats-box").innerHTML = out;
        window.statsInterval = setTimeout(updateStats, 250);
    });
}

window.onload = function() {
    window.logInterval = setInterval(updateLog, 500);
    window.statsInterval = setTimeout(updateStats, 100);
}