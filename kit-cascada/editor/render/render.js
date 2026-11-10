// Renderiza overlay.html cuadro por cuadro (PNG con transparencia) para una línea de tiempo.
// Uso: node render.js timeline.json carpeta_salida [fps]
const fs = require('fs'), path = require('path'), puppeteer = require('puppeteer-core');

// Chrome instalado (Mac, Windows o Linux); CHROME_PATH manda si está definido.
function chrome() {
  const c = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean);
  const p = c.find(x => fs.existsSync(x));
  if (!p) throw new Error('No encontré Google Chrome: instálalo o pon su ruta en CHROME_PATH');
  return p;
}

(async () => {
  const [tlPath, outDir, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 30), TL = JSON.parse(fs.readFileSync(tlPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: chrome(),
    headless: true, args: ['--hide-scrollbars'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920 });
  await page.goto('file://' + path.join(__dirname, 'overlay.html'));
  await page.evaluate(tl => { window.TL = tl; }, TL);
  const n = Math.ceil(TL.duration * fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.setTime(t), i / fps);
    await page.screenshot({ path: path.join(outDir, `f${String(i).padStart(5, '0')}.png`), omitBackground: true });
    if (i % 300 === 0) console.log(`cuadro ${i}/${n}`);
  }
  await browser.close();
})();
