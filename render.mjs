// render.mjs: Deterministic Frame Renderer for Cerita Syehan Episode 0
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const [W, H] = (process.env.RES || '1080x1920').split('x').map(Number);
const FPS = parseInt(process.env.FPS || '30', 10);
const MAXF = parseInt(process.env.MAX_FRAMES || '0', 10);
const FRAMES_DIR = 'frames';
const OUT_DIR = 'out';

fs.rmSync(FRAMES_DIR, { recursive: true, force: true });
fs.mkdirSync(FRAMES_DIR, { recursive: true });
fs.mkdirSync(OUT_DIR, { recursive: true });

console.log(`🎬 Memulai render: Resolusi ${W}x${H} @ ${FPS} FPS`);

const browser = await chromium.launch({
  args: [
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--ignore-gpu-blocklist',
    '--autoplay-policy=no-user-gesture-required',
    '--no-sandbox'
  ]
});

const page = await browser.newPage({ viewport: { width: 400, height: 720 } });
page.on('console', (m) => console.log('[browser]', m.text()));
page.on('pageerror', (e) => console.error('[pageerror]', e.message));

const htmlPath = 'file://' + path.resolve('index.html');
console.log('Membuka file:', htmlPath);
await page.goto(htmlPath);

await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
const duration = await page.evaluate(() => window.DUR || 72.36);
console.log(`Durasi animasi: ${duration} detik`);

await page.evaluate(([w, h]) => window.setResolution(w, h), [W, H]);

let totalFrames = Math.ceil(duration * FPS);
if (MAXF > 0) totalFrames = Math.min(totalFrames, MAXF);
console.log(`Total frame yang akan dirender: ${totalFrames} frame`);

const t0 = Date.now();
for (let i = 0; i < totalFrames; i++) {
  const t = i / FPS;
  const dataUrl = await page.evaluate((currTime) => {
    window.renderAt(currTime);
    return window.getCanvasDataURL('image/jpeg', 0.95);
  }, t);
  
  const base64Data = dataUrl.split(',')[1];
  const frameFile = path.join(FRAMES_DIR, `f${String(i).padStart(5, '0')}.jpg`);
  fs.writeFileSync(frameFile, Buffer.from(base64Data, 'base64'));
  
  if (i % 60 === 0 || i === totalFrames - 1) {
    const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
    const speed = ((Date.now() - t0) / (i + 1) / 1000).toFixed(2);
    console.log(`[Frame ${i + 1}/${totalFrames}] ${elapsed}s elapsed (${speed} s/frame)`);
  }
}

await browser.close();
console.log('✅ Semua frame berhasil dirender!');

// 1. Jalankan mix audio (Voice + SFX + BGM)
console.log('🎵 Menjalankan audio mix...');
execSync('python3 mix.py', { stdio: 'inherit' });

// 2. Encode MP4 dengan FFmpeg
console.log('🎥 Menggabungkan video + audio menjadi out/video.mp4...');
const ffmpegCmd = `ffmpeg -y -framerate ${FPS} -i ${FRAMES_DIR}/f%05d.jpg -i ${OUT_DIR}/mix.wav \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high \
  -c:a aac -b:a 192k -movflags +faststart -shortest ${OUT_DIR}/video.mp4`;
execSync(ffmpegCmd, { stdio: 'inherit' });

// 3. Buat contact sheet preview
console.log('🖼️ Membuat gambar contact sheet preview...');
const step = Math.max(1, Math.floor(totalFrames / 12));
execSync(`ffmpeg -y -framerate ${FPS} -i ${FRAMES_DIR}/f%05d.jpg -vf "select='not(mod(n,${step}))',scale=270:-1,tile=6x2" -frames:v 1 ${OUT_DIR}/preview.jpg`, { stdio: 'inherit' });

console.log('🎉 RENDER SELESAI LENGKAP!');
