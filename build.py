"""Wrap src/earnies-production.html into the installable web app (PWA) served from this folder by GitHub Pages."""
import pathlib, hashlib
here = pathlib.Path(__file__).parent
out = here
src = (here / "src" / "earnies-production.html").read_text()
ver = hashlib.sha1(src.encode()).hexdigest()[:10]
head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Your beats, projects and collaborations in one glassy studio.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Earnies">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
"""
(out / "index.html").write_text(head + src.replace("<style>", "<style>\nhtml, body { margin: 0; background: #F7F6F2; }", 1).replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")
(out / "manifest.webmanifest").write_text("""{
  "name": "Earnies Production",
  "short_name": "Earnies",
  "description": "Your beats, projects and collaborations in one glassy studio.",
  "id": "./",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#BFE3F7",
  "theme_color": "#F7F6F2",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
""")
(out / "sw.js").write_text("""// Earnies Production offline cache. The version changes with every build.
const CACHE = "earnies-%s";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-180.png", "icons/maskable-512.png", "icons/icon-32.png"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", (e) => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url);
  // pages: network first so updates arrive, cache when offline
  if (req.mode === "navigate") { e.respondWith(fetch(req).then((r) => { caches.open(CACHE).then((c) => c.put("./", r.clone())); return r; }).catch(() => caches.match("./"))); return; }
  // everything else, fonts included: cache first, then fill the cache
  if (url.origin === location.origin || /fonts\\.(googleapis|gstatic)\\.com$/.test(url.hostname))
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((r) => { if (r.ok || r.type === "opaque") { const copy = r.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); } return r; })));
});
""" % ver)
print("built", ver)
