const { chromium } = require('playwright');
const fs = require('fs'); const { spawn } = require('child_process');
const OUT = '/tmp/claude-0/-home-user-IRFAN/5f71c68f-ddee-5e8c-829e-7bc2274d951d/scratchpad';
(async () => {
  const mode = process.argv[2] || 'test';
  const b = await chromium.launch({ args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const pg = await b.newPage({ viewport: { width: 540, height: 960 } });
  pg.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  pg.on('pageerror', e => console.log('pageerror:', e.message));
  await pg.goto('file:///home/user/IRFAN/anim/index.html'); await pg.evaluate(() => window.ready);
  const total = await pg.evaluate(() => TL.total);
  if (mode === 'test') {
    const times = process.argv.slice(3).map(Number);
    for (const t of times) { const d = await pg.evaluate(t => frameURL(t), t); fs.writeFileSync(`${OUT}/f_${t}.jpg`, Buffer.from(d.split(',')[1], 'base64')); }
  } else {
    const FPS = 30, n = Math.ceil(total * FPS);
    const ff = spawn('ffmpeg', ['-v','error','-y','-f','image2pipe','-framerate',String(FPS),'-vcodec','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','video_only.mp4'], { stdio: ['pipe','inherit','inherit'] });
    for (let i = 0; i < n; i++) {
      const d = await pg.evaluate(t => frameURL(t), i / FPS);
      if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log('frame', i, '/', n);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('video_only.mp4 siap');
  }
  await b.close();
})();
