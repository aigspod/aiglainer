/* ------------------------------------------------------------ the hero: Port Samudra harbor, raining, at night */
const sky = $('#sky'), sx = sky.getContext('2d');
function rnd(seed){ return () => (seed = (seed * 16807) % 2147483647) / 2147483647 }
let W = 0, H = 0, far = [], near = [], drops = [], lamps = [];
function sizeSky(){
  const r = sky.getBoundingClientRect(), d = Math.min(2, devicePixelRatio || 1);
  W = r.width; H = r.height; sky.width = W*d; sky.height = H*d; sx.setTransform(d,0,0,d,0,0);
  const R = rnd(7), hz = H*0.64;
  far = []; let x = -10;
  while (x < W + 20){ const w = 16 + R()*40, h = H*(0.1 + R()*0.26); far.push({x, w, h, ant: R() < 0.18}); x += w + 1 + R()*3 }
  near = []; x = W*(W < 700 ? 0.42 : 0.5);
  while (x < W + 40){ const w = 40 + R()*70, h = H*(0.2 + R()*0.3), win = [];
    for (let cx = 6; cx < w - 6; cx += 9) for (let cy = 8; cy < h - 6; cy += 12) if (R() < 0.38) win.push([cx, cy, R()]);
    near.push({x, w, h, win, sign: R() < 0.3}); x += w + 4 + R()*10 }
  drops = []; for (let i = 0; i < Math.min(260, W*0.22); i++) drops.push([R()*W, R()*H, 8 + R()*14, 0.5 + R()*0.7]);
  lamps = []; for (let lx = W*0.04; lx < W; lx += Math.max(130, W/9)) lamps.push(lx);
}
function crane(x, base, s, t){
  sx.strokeStyle = '#1b2230'; sx.lineWidth = 3;
  sx.beginPath(); sx.moveTo(x, base); sx.lineTo(x, base - s); sx.moveTo(x + s*0.18, base); sx.lineTo(x + s*0.18, base - s); sx.stroke();
  sx.lineWidth = 1.2; for (let y = base; y > base - s; y -= s/8){ sx.beginPath(); sx.moveTo(x, y); sx.lineTo(x + s*0.18, y - s/8); sx.stroke() }
  sx.lineWidth = 4; sx.beginPath(); sx.moveTo(x - s*0.35, base - s); sx.lineTo(x + s*0.9, base - s); sx.stroke();
  sx.lineWidth = 1; sx.beginPath(); sx.moveTo(x + s*0.6, base - s); sx.lineTo(x + s*0.6, base - s*0.55); sx.stroke();
  sx.fillStyle = (Math.floor(t/700) % 2) ? '#ff3b30' : '#5a1a16'; sx.fillRect(x + s*0.88, base - s - 4, 4, 4);
}
function drawSky(t){
  const hz = H*0.64;
  let g = sx.createLinearGradient(0, 0, 0, hz);
  g.addColorStop(0, '#070a10'); g.addColorStop(.55, '#161c2a'); g.addColorStop(.88, '#3a3433'); g.addColorStop(1, '#5a4434');
  sx.fillStyle = g; sx.fillRect(0, 0, W, hz);
  // low clouds, lit from below by the city
  for (let i = 0; i < 7; i++){ const cx = ((i*W/5 + t/60) % (W + 400)) - 200, cy = H*(0.12 + (i%3)*0.08);
    const cg = sx.createRadialGradient(cx, cy, 10, cx, cy, W*0.22); cg.addColorStop(0, 'rgba(70,64,70,.35)'); cg.addColorStop(1, 'rgba(70,64,70,0)'); sx.fillStyle = cg; sx.fillRect(cx - W*0.25, cy - W*0.25, W*0.5, W*0.5) }
  // far skyline
  for (const b of far){ sx.fillStyle = '#151b27'; sx.fillRect(b.x, hz - b.h, b.w, b.h);
    if (b.ant){ sx.fillRect(b.x + b.w/2 - 1, hz - b.h - 18, 2, 18); if (Math.floor(t/900 + b.x) % 2){ sx.fillStyle = '#ff3b30'; sx.fillRect(b.x + b.w/2 - 2, hz - b.h - 20, 4, 4) } } }
  // harbor cranes on the left
  crane(W*0.03, hz, H*0.34, t); crane(W*0.2, hz, H*0.27, t + 350);
  // elevated railway and a train
  const ry = hz - H*0.06;
  sx.fillStyle = '#0d1219'; sx.fillRect(0, ry, W, 7);
  for (let px = 20; px < W; px += 90) sx.fillRect(px, ry, 6, hz - ry);
  const period = 16000, tx = ((t % period) / period) * (W + 600) - 300;
  sx.fillStyle = '#1d2533'; sx.fillRect(tx, ry - 16, 260, 15);
  sx.fillStyle = '#ffd98a'; for (let k = 8; k < 255; k += 14) if ((k/14|0) % 9 !== 0) sx.fillRect(tx + k, ry - 12, 8, 5);
  sx.fillStyle = '#fff6d0'; sx.fillRect(tx + 258, ry - 10, 3, 4);
  // near buildings with lit windows and the odd neon sign
  for (const b of near){
    sx.fillStyle = '#0c1018'; sx.fillRect(b.x, hz - b.h, b.w, b.h);
    for (const [cx, cy, k] of b.win){ if (Math.sin(t/3000 + k*60) > 0.985) continue; sx.fillStyle = k < 0.15 ? '#9fd0ff' : '#ffcf7a'; sx.globalAlpha = 0.55 + 0.35*k; sx.fillRect(b.x + cx, hz - b.h + cy, 4, 6) }
    sx.globalAlpha = 1;
    if (b.sign && b.w > 60){ const on = Math.sin(t/400 + b.x) > -0.8; sx.fillStyle = on ? '#e0413a' : '#3a1615'; sx.font = '700 12px "Barlow Condensed", sans-serif'; sx.fillText(['HOTEL','BAR','24H','DINER','EAT'][(b.x|0) % 5], b.x + 8, hz - b.h + 18) }
  }
  // water, with the city smeared across it
  g = sx.createLinearGradient(0, hz, 0, H); g.addColorStop(0, '#141a24'); g.addColorStop(1, '#05070b'); sx.fillStyle = g; sx.fillRect(0, hz, W, H - hz);
  for (const b of near){ for (let j = 0; j < 5; j++){ const y = hz + 4 + j*9 + 3*Math.sin(t/600 + j + b.x); sx.fillStyle = 'rgba(255,207,122,.18)'; sx.fillRect(b.x + 4 + 6*Math.sin(t/900 + j*2), y, b.w - 8, 2) } }
  // the quay: road, sodium lamps and their pools of light
  const qy = H - 34; sx.fillStyle = '#10141b'; sx.fillRect(0, qy, W, 34); sx.fillStyle = '#2b3240'; sx.fillRect(0, qy, W, 2);
  for (const lx of lamps){
    const lg = sx.createRadialGradient(lx, qy, 2, lx, qy, 120); lg.addColorStop(0, 'rgba(255,181,71,.38)'); lg.addColorStop(1, 'rgba(255,181,71,0)');
    sx.fillStyle = lg; sx.fillRect(lx - 120, qy - 120, 240, 154);
    sx.fillStyle = '#05070a'; sx.fillRect(lx - 1.5, qy - 70, 3, 70); sx.fillRect(lx - 1.5, qy - 70, 14, 3); sx.fillStyle = '#ffd38a'; sx.fillRect(lx + 8, qy - 67, 7, 3);
  }
  // rain
  sx.strokeStyle = 'rgba(190,205,225,.32)'; sx.lineWidth = 1; sx.beginPath();
  for (const d of drops){ const y = (d[1] + t*0.9*d[3]) % (H + 40) - 20, x = (d[0] - y*0.18 + W) % W; sx.moveTo(x, y); sx.lineTo(x - d[2]*0.18, y + d[2]) }
  sx.stroke();
}
let flipped = false;
function loopSky(t){ drawSky(t || 0); if (!REDUCED) requestAnimationFrame(loopSky) }
sizeSky(); loopSky(0); addEventListener('resize', () => { sizeSky(); if (REDUCED) drawSky(0); drawMap() });
