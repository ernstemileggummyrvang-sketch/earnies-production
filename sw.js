// Earnies Production offline cache. The version changes with every build.
const CACHE = "earnies-26cc11d9ed";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-180.png", "icons/maskable-512.png", "icons/icon-32.png"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", (e) => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url);
  // pages: network first so updates arrive, cache when offline
  if (req.mode === "navigate") { e.respondWith(fetch(req).then((r) => { caches.open(CACHE).then((c) => c.put("./", r.clone())); return r; }).catch(() => caches.match("./"))); return; }
  // everything else, fonts included: cache first, then fill the cache
  if (url.origin === location.origin || /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname))
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((r) => { if (r.ok || r.type === "opaque") { const copy = r.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); } return r; })));
});
