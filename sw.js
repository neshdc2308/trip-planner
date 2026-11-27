// Offline support: the app and its data keep working with no signal (ghats, forts, jungles).
var C="tp-v8",CORE=["./","index.html","manifest.webmanifest","icon.svg","https://unpkg.com/leaflet@1.9.4/dist/leaflet.css","https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"].concat(["spots", "routes", "alerts", "research", "requests", "trips", "stays", "prep", "notes", "kit", "photos", "family", "watch", "weather", "deals"].map(function(c){return"data/"+c+".json"}));
self.addEventListener("install",function(e){e.waitUntil(caches.open(C).then(function(c){return Promise.all(CORE.map(function(u){return c.add(u).catch(function(){})}))}).then(function(){return self.skipWaiting()}))});
self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(x){return x!==C}).map(function(x){return caches.delete(x)}))}).then(function(){return self.clients.claim()}))});
self.addEventListener("fetch",function(e){var r=e.request;if(r.method!=="GET")return;var u=new URL(r.url);
  var mine=u.origin===location.origin,tile=/tile\.openstreetmap\.org$/.test(u.hostname),cdn=u.hostname==="unpkg.com"||/wikimedia\.org$/.test(u.hostname)||/overpass/.test(u.hostname);
  if(!mine&&!tile&&!cdn)return;
  if(mine){e.respondWith(fetch(r).then(function(res){var cp=res.clone();caches.open(C).then(function(c){c.put(r,cp)});return res}).catch(function(){return caches.match(r,{ignoreSearch:true}).then(function(m){return m||caches.match("index.html")})}));return}
  e.respondWith(caches.match(r).then(function(m){return m||fetch(r).then(function(res){if(res.ok||res.type==="opaque"){var cp=res.clone();caches.open(C).then(function(c){c.put(r,cp)})}return res})}));
});
