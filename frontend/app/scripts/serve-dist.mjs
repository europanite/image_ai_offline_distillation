import { createServer } from 'node:http';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(fileURLToPath(new URL('..', import.meta.url)), 'dist');
const host = process.env.FRONTEND_HOST || '0.0.0.0';
const port = Number(process.env.FRONTEND_PORT || 8081);

const contentTypes = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.png', 'image/png'],
  ['.jpg', 'image/jpeg'],
  ['.jpeg', 'image/jpeg'],
  ['.svg', 'image/svg+xml'],
  ['.ico', 'image/x-icon'],
  ['.webp', 'image/webp'],
]);

function resolvePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split('?')[0] || '/');
  const safePath = normalize(decoded).replace(/^([.][.][\/\\])+/, '');
  let candidate = join(root, safePath);
  if (existsSync(candidate) && statSync(candidate).isDirectory()) {
    candidate = join(candidate, 'index.html');
  }
  if (!existsSync(candidate)) {
    candidate = join(root, 'index.html');
  }
  return candidate;
}

if (!existsSync(join(root, 'index.html'))) {
  console.error(`Missing ${join(root, 'index.html')}. Run npm run export:web first.`);
  process.exit(1);
}

const server = createServer((req, res) => {
  const filePath = resolvePath(req.url || '/');
  const ext = extname(filePath).toLowerCase();
  res.setHeader('Content-Type', contentTypes.get(ext) || 'application/octet-stream');
  createReadStream(filePath)
    .on('error', (error) => {
      res.statusCode = 500;
      res.end(String(error));
    })
    .pipe(res);
});

server.listen(port, host, () => {
  console.log(`Expo web export is available at http://${host}:${port}`);
});
