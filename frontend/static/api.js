/* VASTU ONE - API CLIENT v2 */

const API_BASE = 'http://localhost:8000';

const Auth = {
    getToken: function() { return localStorage.getItem('vastu_access_token'); },
    getRefreshToken: function() { return localStorage.getItem('vastu_refresh_token'); },
    setTokens: function(access, refresh) {
        localStorage.setItem('vastu_access_token', access);
        if (refresh) localStorage.setItem('vastu_refresh_token', refresh);
    },
    clear: function() {
        localStorage.removeItem('vastu_access_token');
        localStorage.removeItem('vastu_refresh_token');
        localStorage.removeItem('vastu_user');
    },
    getUser: function() {
        var u = localStorage.getItem('vastu_user');
        return u ? JSON.parse(u) : null;
    },
    setUser: function(user) { localStorage.setItem('vastu_user', JSON.stringify(user)); },
    isLoggedIn: function() { return !!this.getToken(); },
};

async function apiCall(endpoint, options) {
    options = options || {};
    var url = endpoint.indexOf('http') === 0 ? endpoint : (API_BASE + endpoint);
    
    var headers = { 'Accept': 'application/json' };
    if (options.headers) {
        for (var k in options.headers) headers[k] = options.headers[k];
    }
    
    var token = Auth.getToken();
    if (token && !options.noAuth) {
        headers['Authorization'] = 'Bearer ' + token;
    }
    
    if (options.body && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(options.body);
    }
    
    try {
        var response = await fetch(url, Object.assign({}, options, { headers: headers }));
        
        if (response.status === 401 && Auth.getRefreshToken() && !options.noAuth) {
            var refreshed = await refreshAccessToken();
            if (refreshed) {
                headers['Authorization'] = 'Bearer ' + Auth.getToken();
                var retry = await fetch(url, Object.assign({}, options, { headers: headers }));
                return handleResponse(retry);
            } else {
                Auth.clear();
                window.location.href = '/login.html';
                throw new Error('Session expired');
            }
        }
        
        return handleResponse(response);
    } catch (err) {
        if (err.name === 'TypeError') {
            throw new Error('Network error');
        }
        throw err;
    }
}

async function handleResponse(response) {
    var contentType = response.headers.get('content-type') || '';
    var data;
    
    if (contentType.indexOf('application/json') >= 0) {
        data = await response.json();
    } else if (contentType.indexOf('application/pdf') >= 0) {
        return await response.blob();
    } else {
        data = await response.text();
    }
    
    if (!response.ok) {
        var message = (data && data.detail) || (data && data.message) || ('HTTP ' + response.status);
        var error = new Error(typeof message === 'string' ? message : JSON.stringify(message));
        error.status = response.status;
        error.data = data;
        throw error;
    }
    
    return data;
}

async function refreshAccessToken() {
    try {
        var refresh = Auth.getRefreshToken();
        if (!refresh) return false;
        
        var res = await fetch(API_BASE + '/api/auth/refresh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_token: refresh }),
        });
        
        if (!res.ok) return false;
        var data = await res.json();
        Auth.setTokens(data.access_token, data.refresh_token);
        return true;
    } catch (e) { return false; }
}

var UI = {
    toast: function(message, type) {
        type = type || 'info';
        var el = document.createElement('div');
        el.className = 'toast ' + type;
        el.textContent = message;
        document.body.appendChild(el);
        setTimeout(function() { el.remove(); }, 4000);
    },
    loading: function(show) {
        show = show !== false;
        var el = document.getElementById('vastu-loading');
        if (show) {
            if (!el) {
                el = document.createElement('div');
                el.id = 'vastu-loading';
                el.className = 'loading-overlay';
                el.innerHTML = '<div class="spinner"></div>';
                document.body.appendChild(el);
            }
        } else if (el) {
            el.remove();
        }
    },
    formatDate: function(iso) {
        if (!iso) return '-';
        try {
            return new Date(iso).toLocaleDateString('en-IN', {
                day: '2-digit', month: 'short', year: 'numeric'
            });
        } catch (e) { return '-'; }
    },
    formatDateTime: function(iso) {
        if (!iso) return '-';
        try {
            return new Date(iso).toLocaleString('en-IN', {
                day: '2-digit', month: 'short', year: 'numeric',
                hour: '2-digit', minute: '2-digit'
            });
        } catch (e) { return '-'; }
    },
    formatTime: function(sec) {
        var m = Math.floor(sec / 60);
        var s = Math.floor(sec % 60);
        return m + ':' + (s < 10 ? '0' : '') + s;
    },
};

var API = {
    auth: {
        signup: async function(payload) {
            var data = await apiCall('/api/auth/signup', { method: 'POST', body: payload, noAuth: true });
            Auth.setTokens(data.access_token, data.refresh_token);
            return data;
        },
        login: async function(email, password) {
            var data = await apiCall('/api/auth/login', { method: 'POST', body: { email: email, password: password }, noAuth: true });
            Auth.setTokens(data.access_token, data.refresh_token);
            return data;
        },
        me: async function() { return await apiCall('/api/auth/me'); },
        logout: function() { Auth.clear(); },
    },
    clients: {
        list: async function(skip, limit) {
            skip = skip || 0; limit = limit || 50;
            return await apiCall('/api/clients?skip=' + skip + '&limit=' + limit);
        },
        get: async function(id) { return await apiCall('/api/clients/' + id); },
        create: async function(payload) { return await apiCall('/api/clients', { method: 'POST', body: payload }); },
        update: async function(id, payload) { return await apiCall('/api/clients/' + id, { method: 'PUT', body: payload }); },
        remove: async function(id) { return await apiCall('/api/clients/' + id, { method: 'DELETE' }); },
    },
    properties: {
        list: async function(clientId) {
            var q = clientId ? ('?client_id=' + clientId) : '';
            return await apiCall('/api/properties' + q);
        },
        get: async function(id) { return await apiCall('/api/properties/' + id); },
        create: async function(payload) { return await apiCall('/api/properties', { method: 'POST', body: payload }); },
        update: async function(id, payload) { return await apiCall('/api/properties/' + id, { method: 'PUT', body: payload }); },
        remove: async function(id) { return await apiCall('/api/properties/' + id, { method: 'DELETE' }); },
    },
    reports: {
        list: async function(propertyId) {
            var q = propertyId ? ('?property_id=' + propertyId) : '';
            return await apiCall('/api/reports' + q);
        },
        get: async function(id) { return await apiCall('/api/reports/' + id); },
        generate: async function(payload) { return await apiCall('/api/reports/generate', { method: 'POST', body: payload }); },
        updateStatus: async function(id, status) { return await apiCall('/api/reports/' + id + '/status', { method: 'PUT', body: { status: status } }); },
        remove: async function(id) { return await apiCall('/api/reports/' + id, { method: 'DELETE' }); },
        downloadPDF: async function(id) {
            var blob = await apiCall('/api/reports/' + id + '/pdf');
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'vastu_one_report_' + id.slice(0, 8) + '.pdf';
            a.click();
            URL.revokeObjectURL(url);
        },
    },
    lms: {
        listCourses: async function(publishedOnly) {
            var q = publishedOnly ? '?published_only=true' : '';
            return await apiCall('/api/lms/courses' + q);
        },
        getCourse: async function(id) { return await apiCall('/api/lms/courses/' + id); },
        createCourse: async function(payload) { return await apiCall('/api/lms/courses', { method: 'POST', body: payload }); },
        listModules: async function(courseId) { return await apiCall('/api/lms/courses/' + courseId + '/modules'); },
        createModule: async function(courseId, payload) { return await apiCall('/api/lms/courses/' + courseId + '/modules', { method: 'POST', body: payload }); },
        listLessons: async function(moduleId) { return await apiCall('/api/lms/modules/' + moduleId + '/lessons'); },
        createLesson: async function(moduleId, payload) { return await apiCall('/api/lms/modules/' + moduleId + '/lessons', { method: 'POST', body: payload }); },
        enroll: async function(courseId) { return await apiCall('/api/lms/courses/' + courseId + '/enroll', { method: 'POST' }); },
        myEnrollments: async function() { return await apiCall('/api/lms/enrollments'); },
        markProgress: async function(payload) { return await apiCall('/api/lms/progress', { method: 'POST', body: payload }); },
    },
};

window.VastuAPI = { API: API, Auth: Auth, UI: UI, apiCall: apiCall };