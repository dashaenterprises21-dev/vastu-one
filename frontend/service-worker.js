/* ============================================================
   VASTU ONE — Service Worker
   PWA offline-first caching
   ============================================================ */

const CACHE_VERSION = 'vastu-one-v1';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;

// Assets to cache on install
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/login.html',
    '/dashboard.html',
    '/static/design-system.css',
    '/static/api.js',
    '/manifest.json',
];

// Install — cache static assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing...');
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => {
            return cache.addAll(STATIC_ASSETS).catch((err) => {
                console.warn('[SW] Failed to cache some assets:', err);
            });
        })
    );
    self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating...');
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((key) => !key.startsWith(CACHE_VERSION))
                    .map((key) => caches.delete(key))
            );
        })
    );
    self.clients.claim();
});

// Fetch — network-first for API, cache-first for static
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET
    if (request.method !== 'GET') return;
    
    // Skip chrome extensions
    if (!url.protocol.startsWith('http')) return;
    
    // API requests: network-first, no cache fallback (data changes)
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(networkOnly(request));
        return;
    }
    
    // Static assets: cache-first
    if (url.pathname.startsWith('/static/') || 
        url.pathname.endsWith('.css') || 
        url.pathname.endsWith('.js') ||
        url.pathname.endsWith('.woff2')) {
        event.respondWith(cacheFirst(request));
        return;
    }
    
    // HTML pages: network-first, cache fallback
    event.respondWith(networkFirst(request));
});

// Strategy: network only
async function networkOnly(request) {
    try {
        return await fetch(request);
    } catch (err) {
        // Offline: return generic JSON error for API
        return new Response(
            JSON.stringify({ detail: 'Offline — no network connection' }),
            { status: 503, headers: { 'Content-Type': 'application/json' } }
        );
    }
}

// Strategy: cache first
async function cacheFirst(request) {
    const cache = await caches.open(STATIC_CACHE);
    const cached = await cache.match(request);
    if (cached) return cached;
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (err) {
        return new Response('', { status: 503 });
    }
}

// Strategy: network first, fall back to cache
async function networkFirst(request) {
    const cache = await caches.open(RUNTIME_CACHE);
    try {
        const response = await fetch(request);
        if (response.ok && response.type === 'basic') {
            cache.put(request, response.clone());
        }
        return response;
    } catch (err) {
        const cached = await cache.match(request);
        if (cached) return cached;
        
        // Offline page
        return new Response(
            `<!DOCTYPE html><html><head><title>Offline — VASTU ONE</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background: #05060F; color: #F8F7F2; font-family: system-ui, sans-serif; 
                       display: flex; align-items: center; justify-content: center; min-height: 100vh; 
                       margin: 0; text-align: center; padding: 20px; }
                .box { max-width: 400px; }
                .logo { font-family: serif; font-size: 32px; font-weight: 700; margin-bottom: 20px; }
                .logo .gold { color: #D4AF37; }
                .msg { color: rgba(248,247,242,0.65); margin-bottom: 30px; }
                .btn { display: inline-block; padding: 12px 24px; background: #D4AF37; color: #05060F; 
                       text-decoration: none; border-radius: 8px; font-weight: 600; }
            </style>
            </head><body>
            <div class="box">
                <div class="logo">VASTU <span class="gold">ONE</span></div>
                <h2>You're offline</h2>
                <p class="msg">No internet connection. Some features may be limited.</p>
                <a href="/" class="btn">Retry</a>
            </div>
            </body></html>`,
            { status: 200, headers: { 'Content-Type': 'text/html' } }
        );
    }
}

// Skip waiting message
self.addEventListener('message', (event) => {
    if (event.data === 'SKIP_WAITING') self.skipWaiting();
});