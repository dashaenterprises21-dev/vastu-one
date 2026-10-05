// Vastu One Enterprise - Shared API Client
// Ye file saare frontend pages ke liye common hai

const API_BASE = 'http://localhost:8001';

// ═══════════════════════════════════════════
// CORE API CLIENT
// ═══════════════════════════════════════════
const API = {
    async get(endpoint) {
        try {
            const res = await fetch(API_BASE + endpoint);
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return await res.json();
        } catch (err) {
            console.error('GET ' + endpoint + ' failed:', err);
            throw err;
        }
    },

    async post(endpoint, data) {
        try {
            const res = await fetch(API_BASE + endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return await res.json();
        } catch (err) {
            console.error('POST ' + endpoint + ' failed:', err);
            throw err;
        }
    }
};

// ═══════════════════════════════════════════
// ASTRO API
// ═══════════════════════════════════════════
const AstroAPI = {
    kundli: (dob, tob, place) => API.post('/api/astro/kundli', { dob, tob, place }),
    planets: () => API.get('/api/astro/planets'),
    planetsByDirection: (direction) => API.post('/api/astro/planets/direction', { direction }),
    house: (n) => API.post('/api/astro/house', { house_number: n }),
    dasha: (nakshatra) => API.get('/api/astro/dasha?nakshatra=' + (nakshatra || 'Ashwini')),
    fullReport: (dob, tob, place) => API.post('/api/astro/full-report', { dob, tob, place })
};

// ═══════════════════════════════════════════
// NUMEROLOGY API
// ═══════════════════════════════════════════
const NumerologyAPI = {
    mulank: (dob) => API.post('/api/numerology/mulank', { dob }),
    bhagyank: (dob) => API.post('/api/numerology/bhagyank', { dob }),
    nameNumber: (name, system) => API.post('/api/numerology/name-number', { name, system: system || 'chaldean' }),
    property: (property_number) => API.post('/api/numerology/property', { property_number }),
    compatibility: (num1, num2) => API.post('/api/numerology/compatibility', { num1, num2 }),
    fullReport: (dob, name, property_number) => API.post('/api/numerology/full-report', { dob, name, property_number })
};

// ═══════════════════════════════════════════
// MARMA API
// ═══════════════════════════════════════════
const MarmaAPI = {
    point: (row, col) => API.post('/api/marma/point', { row, col }),
    all: () => API.get('/api/marma/all'),
    byType: (marma_type) => API.post('/api/marma/by-type', { marma_type }),
    remedy: (row, col) => API.post('/api/marma/remedy', { row, col }),
    fullReport: () => API.get('/api/marma/full-report')
};

// ═══════════════════════════════════════════
// OCCULT API
// ═══════════════════════════════════════════
const OccultAPI = {
    remedy: (remedy_name) => API.post('/api/occult/remedy', { remedy_name }),
    byPurpose: (purpose) => API.post('/api/occult/by-purpose', { purpose }),
    dailySchedule: () => API.get('/api/occult/daily-schedule'),
    expertGuidance: (item) => API.post('/api/occult/expert-guidance', { item }),
    avoidList: () => API.get('/api/occult/avoid-list'),
    remedyPlan: (issues) => API.post('/api/occult/remedy-plan', { issues }),
    fullReport: () => API.get('/api/occult/full-report')
};

// ═══════════════════════════════════════════
// POOJA API
// ═══════════════════════════════════════════
const PoojaAPI = {
    all: () => API.get('/api/pooja/all'),
    byPurpose: (purpose) => API.post('/api/pooja/by-purpose', { purpose }),
    mantra: (planet) => API.post('/api/pooja/mantra', { planet })
};

// ═══════════════════════════════════════════
// PACKAGES API
// ═══════════════════════════════════════════
const PackagesAPI = {
    list: () => API.get('/api/packages/list'),
    get: (name) => API.get('/api/packages/' + name),
    analyze: (data) => API.post('/api/packages/analyze', data),
    quickScore: (data) => API.post('/api/packages/quick-score', data),
    recommend: (data) => API.post('/api/packages/recommend', data),
    enterpriseReport: (data) => API.post('/api/packages/enterprise-report', data),
    systemInfo: () => API.get('/api/packages/system/info')
};

// ═══════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════
const UI = {
    showLoading: (id) => {
        const el = document.getElementById(id);
        if (el) el.classList.add('show');
    },

    hideLoading: (id) => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('show');
    },

    showError: (id, msg) => {
        const el = document.getElementById(id);
        if (el) {
            el.textContent = msg;
            el.classList.add('show');
        }
    },

    hideError: (id) => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('show');
    },

    showResult: (id) => {
        const el = document.getElementById(id);
        if (el) el.classList.add('show');
    },

    formatCurrency: (n) => '' + Number(n).toLocaleString('en-IN'),

    gradeColor: (grade) => {
        if (grade.includes('A+')) return '#10b981';
        if (grade.includes('A')) return '#22c55e';
        if (grade.includes('B')) return '#f59e0b';
        if (grade.includes('C')) return '#ef4444';
        return '#dc2626';
    }
};

// ═══════════════════════════════════════════
// HEALTH CHECK
// ═══════════════════════════════════════════
async function checkAPIHealth() {
    try {
        const res = await fetch(API_BASE + '/health');
        const data = await res.json();
        console.log('API Health:', data);
        return data.status === 'ok';
    } catch (err) {
        console.error('API not reachable:', err);
        return false;
    }
}

// Auto-check on load
window.addEventListener('load', () => {
    checkAPIHealth().then(ok => {
        if (!ok) {
            console.warn('API server is not running on ' + API_BASE);
        }
    });
});

// Export to window
window.API = API;
window.AstroAPI = AstroAPI;
window.NumerologyAPI = NumerologyAPI;
window.MarmaAPI = MarmaAPI;
window.OccultAPI = OccultAPI;
window.PoojaAPI = PoojaAPI;
window.PackagesAPI = PackagesAPI;
window.UI = UI;

console.log('Vastu One app.js loaded. API_BASE =', API_BASE);
