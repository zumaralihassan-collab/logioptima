#!/usr/bin/env node
/* Executes the REAL app JavaScript from index.html inside a stubbed DOM,
   then asserts the core optimization logic. No browser, no network. */
const fs = require('fs');
const path = require('path');

const htmlPath = process.argv[2]
  || (fs.existsSync(path.join(__dirname, 'index.html')) ? path.join(__dirname, 'index.html')
                                                        : path.join(__dirname, '..', 'index.html'));
const html = fs.readFileSync(htmlPath, 'utf8');

// Extract the main inline <script> (the one with the engine).
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const app = scripts.find(s => s.includes('function haversine'));
if (!app) { console.error('Could not find app script in ' + htmlPath); process.exit(2); }

const STUBS = `
var passes=0, failures=0;
function noop(){ return undefined; }
function makeEl(){
  var base={ value:'', innerHTML:'', textContent:'', checked:false, scrollTop:0, scrollHeight:0,
    dataset:{}, files:[], style:new Proxy({},{get:function(){return '';},set:function(){return true;}}),
    classList:{add:noop,remove:noop,toggle:noop,contains:function(){return false;}},
    appendChild:noop, removeChild:noop, remove:noop, setAttribute:noop, getAttribute:function(){return null;},
    addEventListener:noop, removeEventListener:noop, focus:noop, click:noop, blur:noop, select:noop,
    querySelector:function(){return null;}, querySelectorAll:function(){return [];},
    getContext:function(){return {};}, insertBefore:noop, closest:function(){return null;},
    cloneNode:function(){return makeEl();} };
  return new Proxy(base,{ get:function(t,p){ return (p in t)? t[p] : noop; }, set:function(t,p,v){ t[p]=v; return true; } });
}
var document={ getElementById:function(){return makeEl();}, querySelector:function(){return null;},
  querySelectorAll:function(){return [];}, addEventListener:noop, removeEventListener:noop,
  createElement:function(){return makeEl();}, createElementNS:function(){return makeEl();},
  body:makeEl(), documentElement:makeEl() };
var Lmap={ setView:function(){return Lmap;}, addLayer:noop, removeLayer:noop, fitBounds:noop,
  invalidateSize:noop, on:noop, off:noop, panTo:noop, remove:noop, addControl:noop, removeControl:noop };
var Llayer={ addTo:function(){return Llayer;}, clearLayers:noop, addLayer:noop, removeLayer:noop };
var Lmarker={ addTo:function(){return Lmarker;}, bindPopup:function(){return Lmarker;}, on:function(){return Lmarker;}, openPopup:noop };
var L={ map:function(){return Lmap;}, tileLayer:function(){return {addTo:function(){return {};}};},
  layerGroup:function(){return Llayer;}, circleMarker:function(){return Lmarker;}, marker:function(){return Lmarker;},
  polyline:function(){return Lmarker;}, latLngBounds:function(){return {pad:function(){return {};}};},
  divIcon:function(){return {};}, control:function(){return {addTo:noop};}, DomEvent:{stop:noop} };
var localStorage={ _:{}, getItem:function(k){return (k in this._)?this._[k]:null;},
  setItem:function(k,v){this._[k]=String(v);}, removeItem:function(k){delete this._[k];} };
var location={ href:'', hash:'', search:'', origin:'', pathname:'' };
var history={ replaceState:noop, pushState:noop };
var navigator={ language:'en', clipboard:{ writeText:function(){return Promise.resolve();} } };
function fetch(){ return Promise.reject(new Error('no-network-in-test')); }
var window={ addEventListener:noop, removeEventListener:noop, location:location, history:history,
  matchMedia:function(){return {matches:false, addEventListener:noop};}, navigator:navigator,
  URL:{ createObjectURL:function(){return 'blob:'; }, revokeObjectURL:noop } };
var alert=noop, confirm=function(){return true;}, prompt=function(){return null;};
`;

const TESTS = `
;(function(){
  function ok(c,m){ if(c){passes++; console.log('  \\u2713 '+m);} else {failures++; console.log('  \\u2717 FAIL: '+m);} }
  // 1) haversine accuracy
  var d1=haversine({lat:40.71,lon:-74.01},{lat:51.51,lon:-0.13});
  ok(Math.abs(d1-5570)<90, 'haversine NY->London ~5570 km (got '+d1.toFixed(0)+')');
  var d2=haversine({lat:40.71,lon:-74.01},{lat:1.35,lon:103.82});
  ok(Math.abs(d2-15300)<200, 'haversine NY->Singapore ~15300 km (got '+d2.toFixed(0)+')');
  ok(haversine({lat:0,lon:0},{lat:0,lon:0})===0, 'haversine identical points = 0');
  // build a global test set
  locations=[["New York",40.71,-74.01],["London",51.51,-0.13],["Singapore",1.35,103.82],["Tokyo",35.68,139.69],["Sydney",-33.87,151.21],["Dubai",25.20,55.27],["Mumbai",19.08,72.88],["Sao Paulo",-23.55,-46.63],["Los Angeles",34.05,-118.24]].map(function(c){return {name:c[0],lat:c[1],lon:c[2],role:'stop'};});
  locations[0].role='origin'; locations[1].role='origin'; locations[2].role='origin';
  // 2) TSP
  var o=tspOrder();
  ok(o[0]===o[o.length-1], 'TSP tour returns to origin');
  ok(new Set(o).size===locations.length, 'TSP visits every city exactly once');
  var km=routeKm(o);
  var naive=locations.map(function(_,i){return i;}); naive.push(0);
  ok(km<=routeKm(naive)+1, 'TSP km <= naive-order km ('+km.toFixed(0)+' <= '+routeKm(naive).toFixed(0)+')');
  ok(km>0 && isFinite(km), 'TSP km is positive & finite');
  // 3) hub / facility
  var h=hubSolve(2);
  ok(h.chosen.length===2, 'hubSolve opens requested 2 hubs');
  ok(h.assign.length===locations.length, 'hubSolve assigns all cities');
  ok(h.total>0 && isFinite(h.total), 'hubSolve total finite');
  // 4) centroid
  var c=centroid();
  ok(c && c.nearest && c.nearest.length===4, 'centroid returns a nearest city');
  // 5) mode economics sanity
  ok(PLANMODES.air.rate>PLANMODES.ocean.rate, 'air pricier per km than ocean');
  ok(PLANMODES.air.speed>PLANMODES.ocean.speed, 'air faster than ocean');
  ok(PLANMODES.air.co2>PLANMODES.rail.co2, 'air emits more CO2/km than rail');
  // 6) optional: great-circle interpolation (added feature)
  if (typeof greatCircle==='function'){
    var gc=greatCircle({lat:40.71,lon:-74.01},{lat:51.51,lon:-0.13},32);
    ok(Array.isArray(gc)&&gc.length>=2, 'greatCircle returns a polyline path');
    ok(Math.abs(gc[0][0]-40.71)<0.01 && Math.abs(gc[gc.length-1][0]-51.51)<0.01, 'greatCircle endpoints match input');
  }
  // 6b) optional: arcPts great-circle (this app's curve function)
  if (typeof arcPts==='function'){
    var ap=arcPts({lat:40.71,lon:-74.01},{lat:51.51,lon:-0.13},32);
    ok(Array.isArray(ap)&&ap.length>=2, 'arcPts returns a great-circle path');
  }
  // 7) optional: CSV parse (added feature)
  if (typeof parseCSV==='function'){
    var rows=parseCSV('name,lat,lon\\nTestburg,10,20\\n');
    ok(rows.length===1 && Math.abs(rows[0].lat-10)<0.001 && Math.abs(rows[0].lon-20)<0.001, 'parseCSV reads name,lat,lon');
  }
  // 8) optional: share-link round trip (added feature)
  if (typeof encodePlan==='function' && typeof decodePlan==='function'){
    var enc=encodePlan(); var dec=decodePlan(enc);
    ok(dec && Array.isArray(dec.locations) && dec.locations.length===locations.length, 'encode/decode plan round-trips locations');
  }
  console.log('\\nLOGIC: '+passes+' passed, '+failures+' failed.');
  if(failures>0) process.exitCode=1;
})();
`;

try {
  new Function(STUBS + '\n' + app + '\n' + TESTS)();
} catch (e) {
  console.error('  ✗ RUNTIME/SYNTAX ERROR while executing app script:');
  console.error('    ' + (e && e.stack ? e.stack.split('\n').slice(0,3).join('\n    ') : e));
  process.exit(1);
}
