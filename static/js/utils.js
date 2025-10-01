async function httpRequest(method, url = '', body = {}, headers = {}) {
    const requestHeaders = { ...headers };
    if (!requestHeaders['Content-Type']) {
        requestHeaders['Content-Type'] = 'application/json';
    }

    const options = {
        method: method.toUpperCase(),
        headers: requestHeaders,
    };

    if (['POST', 'PUT', 'PATCH'].includes(options.method) && Object.keys(body).length) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
        data.status_code = response.status;
    }

    return data;
}

async function cookieNoticeAccepted() {
    const banner = document.getElementsByClassName('cookie-banner')[0];

    // user preferences
    const preferences = {
        "functional": "ok"
    };

    const response = await httpRequest("PUT", "/cookies", {}, { "X-COOKIES-Preference": preferences });
    if (response.message == "ok") {
        // hide cookie banner
        banner.style.display = 'none';
    }
}