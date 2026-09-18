// md2slides — requirements unit suite (SPEC.md A1–A28 + v2 features).
// Runs the real app headless (Chrome over CDP) and asserts each requirement.
//
// Usage:
//   python3 -m http.server 8798 --bind 127.0.0.1 --directory <repo-root> &
//   BASE=http://127.0.0.1:8798/apps/md2slides/index.html node apps/md2slides/test/requirements.test.mjs
//
// Depth rule: requirements whose implementing logic is small (~<=5 lines) get a
// single "sanity" assertion; larger logic gets "comprehensive" checks (setup +
// multiple assertions or a rendered measure).
import { spawn } from 'node:child_process';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = process.env.BASE || 'http://127.0.0.1:8798/apps/md2slides/index.html';
const PORT = 9481;
const sleep = ms => new Promise(r => setTimeout(r, ms));

const proc = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-first-run',
  '--no-default-browser-check', `--user-data-dir=/tmp/mdc-req-test`, `--remote-debugging-port=${PORT}`,
  '--window-size=1600,900', BASE], { stdio: 'ignore' });

let pageWs = null;
for (let i = 0; i < 150 && !pageWs; i++) {
  try {
    const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
    const p = l.find(t => t.type === 'page' && t.url.includes('md2slides'));
    if (p?.webSocketDebuggerUrl) pageWs = p.webSocketDebuggerUrl;
  } catch (e) {}
  if (!pageWs) await sleep(200);
}
if (!pageWs) { console.error('no CDP page; is the server running?'); proc.kill('SIGKILL'); process.exit(2); }
const ws = new WebSocket(pageWs);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let id = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
const send = (method, params = {}) => new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async expr => (await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true })).result?.result?.value;
const ready = async () => { for (let i = 0; i < 80; i++) { if (await ev(`document.querySelectorAll('#deck .card').length>0`) === true) return; await sleep(150); } };

await ready();

let pass = 0, fail = 0, sanity = 0, comp = 0;
const rows = [];
const check = (req, kind, name, cond, detail = '') => {
  (cond ? pass++ : fail++);
  (kind === 'comprehensive' ? comp++ : sanity++);
  rows.push({ req, kind, name, ok: !!cond, detail });
};
const setDeck = async md => { await ev(`(() => { document.querySelector('#md').value = ${JSON.stringify(md)}; build(); })()`); };
const deck = (title, closing, lines) => ['---', `title: ${title}`, ...(closing ? [`closing: ${closing}`] : []), '---', '', ...lines].join('\n');
const LAST = 'await new Promise(r=>setTimeout(r,250))';

/* ── A1–A4  Parser & round-trip ───────────────────────── */
await setDeck(deck('Round', '', ['# One', '- a', '# Two', '- b', '# Three', '- c']));
{
  const n = await ev('cards.length');
  check('A1', 'sanity', '# heading starts a card (1 title + 3 content)', n === 4, 'cards=' + n);
  const titles = await ev(`cards.map(c=>c.querySelector('h1')?.textContent.trim())`);
  check('A1', 'sanity', 'card titles equal heading text', titles[1] === 'One' && titles[3] === 'Three', titles.join('|'));
}
await setDeck(deck('Rounded', '', ['# X', '- y']));
check('A2', 'sanity', 'title card comes from frontmatter', (await ev(`cards[0].querySelector('h1')?.textContent.trim()`)) === 'Rounded');
check('A2', 'sanity', 'absent byline leaves no separators', !(await ev(`cards[0].querySelector('.byline')`)));
{
  const md = await ev(`document.querySelector('#md').value`);
  check('A4', 'sanity', 'editor source is unchanged after build (round-trip)', md.startsWith('---\ntitle: Rounded'));
}
await setDeck(deck('Dashes', '', ['para', '---', '# Card', '- b']));
check('A1', 'sanity', 'body `---` is an hr, not a card break (shipped)', (await ev('cards.length')) === 2, 'cards=' + (await ev('cards.length')));

/* ── A5–A7  Content rendering ─────────────────────────── */
await setDeck(deck('Content', '', [
  '# Card', 'Plain text with **bold** and *it* and `code` and [lnk](https://llmstxt.org/) and ~~strike~~',
  '- bullet', '1. ordered', '> quote', '```md', 'code block', '```', '![a](https://picsum.photos/100/100)'
]));
check('A5', 'sanity', 'inline markdown renders (bold/italic/code/link/strike)', await ev(`(() => { const c=cards[1]; return !!c.querySelector('strong')&&!!c.querySelector('em')&&!!c.querySelector('code')&&!!c.querySelector('a')&&!!c.querySelector('del'); })()`));
check('A5', 'comprehensive', 'block content renders (list, blockquote, code, image)', await ev(`(() => { const c=cards[1]; return !!c.querySelector('ul')&&!!c.querySelector('ol')&&!!c.querySelector('blockquote')&&!!c.querySelector('pre>code')&&!!c.querySelector('img'); })()`));
check('A17', 'sanity', 'javascript: link is not clickable', await ev(`(() => { const c=document.createElement('div'); c.innerHTML=inline('[x](javascript:alert(1))'); return !c.querySelector('a'); })()`));

/* ── A8–A10 Geometry & page model ─────────────────────── */
{
  const ratios = await ev(`(() => {
    const out = {};
    for (const g of ['16:9','1:1','4:5']) {
      document.querySelector('#geoSeg button[data-geo="'+g+'"]').click();
      const c=cards[0], cs=getComputedStyle(c);
      out[g] = { w: cs.getPropertyValue('--cw').trim(), h: cs.getPropertyValue('--ch').trim() };
    }
    $('#geoSeg button[data-geo="16:9"]').click(); return out;
  })()`);
  check('A8', 'comprehensive', 'geometry drives exact card boxes', ratios['16:9'].w === '1920px' && ratios['1:1'].w === '1080px' && ratios['4:5'].h === '1350px', JSON.stringify(ratios));
  const typing = await ev(`(() => { const t=document.querySelector('#md'); const s=t.value.indexOf('# '); t.setSelectionRange(s,s+1); return caretCard(); })()`);
  check('A11', 'sanity', 'typing a # card switches preview', typing >= 0);
}
await setDeck(deck('Bookends', 'none', ['# A', '- x', '# B', '- y']));
check('A19', 'comprehensive', 'closing:none makes last card a numbered content card',
  (await ev(`(() => { const c=cards[cards.length-1]; return c.dataset.kind==='content' && !!c.querySelector('.foot'); })()`)) === true);
await setDeck(deck('Bookends2', '', ['# A', '- x', '# B', '- y']));
{
  const b = await ev(`(() => { const c=cards[cards.length-1]; return { kind:c.dataset.kind, foot:!!c.querySelector('.foot') }; })()`);
  check('A19', 'sanity', 'closing card (default auto) has no footer', b.kind === 'closing' && !b.foot, JSON.stringify(b));
  check('A20', 'sanity', 'title card first child is the h1', await ev(`cards[0].firstElementChild?.tagName === 'H1'`));
}

/* ── Storage ──────────────────────────────────────────── */
{
  await setDeck(deck('Persist', '', ['# K', '- v']));
  await ev(`save()`); await sleep(260);
  check('A13', 'sanity', 'save writes the live v2 key with the deck', await ev(`(() => { const d=JSON.parse(localStorage.getItem('janalogy.mdcards.v2')); return d && d.md.includes('# K'); })()`));
  await ev(`localStorage.setItem('janalogy.mdcards.v2', '{ not json')`);
  const loaded = await ev(`document.querySelector('#md').value = load()`);
  check('A14', 'sanity', 'corrupt storage falls back to starter, does not crash', typeof loaded === 'string' && loaded.includes('md2slides — every feature in one deck'));
  await ev(`localStorage.removeItem('janalogy.mdcards.v2'); document.querySelector('#md').value = '';`);
  await setDeck(deck('V1migrate', '', ['# A', '- b']));
  await ev(`save()`); await sleep(260);
  await ev(`(() => { const d=JSON.parse(localStorage.getItem('janalogy.mdcards.v2')); localStorage.setItem('janalogy.mdcards.v1', JSON.stringify(d)); localStorage.removeItem('janalogy.mdcards.v2'); })()`);
  await ev(`document.querySelector('#md').value = load()`);
  check('A13', 'sanity', 'load falls back to the frozen v1 key (one-time migration)', (await ev(`document.querySelector('#md').value`)).includes('# A'));
}

/* ── v2: two-column (A24) ─────────────────────────────── */
await setDeck(deck('TwoCol', '', ['# Two', '## Left', '- a', '- b', '## Right', '- c', '- d']));
check('A24', 'sanity', 'two ## under one # → two-column grid', (await ev(`document.querySelectorAll('.cols').length`)) === 1);
check('A24', 'sanity', 'each column is a .col', (await ev(`document.querySelectorAll('.col').length`)) === 2);
await setDeck(deck('OneCol', '', ['# One', '## Solo', '- a', '- b']));
check('A24', 'sanity', 'one ## renders a normal card', (await ev(`document.querySelectorAll('.cols').length`)) === 0);
await setDeck(deck('Fence', '', ['# F', 'intro', '```', '## InsideFence', '```', '## Left', '- a', '## Right', '- b']));
check('A24', 'comprehensive', '## inside a code fence is ignored (fence-aware)', (await ev(`document.querySelectorAll('.cols').length`)) === 1);

/* ── v2: search (A25) ─────────────────────────────────── */
await setDeck(deck('Search', '', ['# Alpha', '- Beta bullet', 'Para with Gamma.', '```js', 'delta_in_fence = 1', '```', '```mermaid', 'flowchart LR', '  P[ZetaNode]', '```']));
{
  const has = (q, card, kind) => ev(`searchRows(${JSON.stringify(q)}).some(r=>r.card===${card} && r.kind===${JSON.stringify(kind)})`);
  check('A25', 'sanity', 'search finds a bullet with its slide number', await has('beta', 1, 'bullet'));
  check('A25', 'sanity', 'search finds a paragraph', await has('gamma', 1, 'text'));
  check('A25', 'sanity', 'search finds text inside a code fence', await has('delta_in_fence', 1, 'code'));
  check('A25', 'sanity', 'search finds diagram source', await has('ZetaNode', 1, 'code'));
  check('A25', 'sanity', 'search opens only in slideshow', await ev(`(() => { closeSearch(); window.dispatchEvent(new KeyboardEvent('keydown',{key:'/'})); const inEdit=$('#search').hidden; slideshow(true); window.dispatchEvent(new KeyboardEvent('keydown',{key:'/'})); const inShow=!$('#search').hidden; closeSearch(); slideshow(false); return inEdit && inShow; })()`));
}

/* ── v2: panes, navigation, shortcuts (A26–A28) ───────── */
check('A26', 'sanity', 'pane splitter element present', await ev(`(() => { const s=document.querySelector('.splitter'); return !!s && getComputedStyle(s).cursor === 'col-resize'; })()`));
{
  await setDeck(deck('Nav', '', ['# A', '- 1', '# B', '- 2', '# C', '- 3']));
  const nw = await ev(`(() => { active = cards.length-1; stepSlide(1); const last = active === cards.length-1; active = 0; stepSlide(-1); const first = active === 0; return last && first; })()`);
  check('A27', 'sanity', 'no-wrap at both ends', nw);
}
check('A28', 'sanity', 'fresh load (empty storage) opens the superset default deck',
  await ev(`(() => { const t=$('#starter').textContent; return t.includes('every feature in one deck'); })()`));
await setDeck(await ev(`$('#starter').textContent`));
check('A28', 'comprehensive', 'default deck has no overflow (10 cards audit)',
  await ev(`(() => { return cards.length===10 && cards.every(c=>{ const b=c.querySelector('.body'); return !b || b.scrollHeight-b.clientHeight<=0; }); })()`));
{
  await setDeck(deck('Short', '', ['# One', '- a', '# Two', '- b', '# Three', '- c']));
  const sh = await ev(`(() => { const before=active; active=1; slideshow(true); window.dispatchEvent(new KeyboardEvent('keydown',{key:'2'})); const bufShow=!$('#gotoNum').hidden && $('#gotoNum').textContent==='2'; slideshow(false); return bufShow; })()`);
  check('v2', 'sanity', 'slideshow digit keys buffer the number on screen', sh);
}

/* ── type scale (A21) & mobile fit (A23) ──────────────── */
{
  const t = await ev(`(() => {
    const m = {};
    for (const g of ['16:9','1:1','4:5']) {
      document.querySelector('#geoSeg button[data-geo="'+g+'"]').click();
      const c=cards[0], cs=getComputedStyle(c); m[g]={ fs: parseFloat(cs.fontSize), cw: parseFloat(cs.getPropertyValue('--cw')) };
    }
    $('#geoSeg button[data-geo="16:9"]').click(); return m;
  })()`);
  check('A21', 'comprehensive', 'reading type clears budget in every profile',
    (t['1:1'].fs/t['1:1'].cw >= 0.0395) && (t['4:5'].fs/t['4:5'].cw >= 0.0395) && Math.abs(t['16:9'].fs/t['16:9'].cw - 0.0225) < 0.003,
    '16:9 ' + (t['16:9'].fs/t['16:9'].cw).toFixed(4) + ' · 1:1 ' + (t['1:1'].fs/t['1:1'].cw).toFixed(4) + ' · 4:5 ' + (t['4:5'].fs/t['4:5'].cw).toFixed(4));
}
await setDeck(deck('FenceOnly', '', ['# Only', '```', 'a', 'b', 'c', '```']));
check('A22', 'comprehensive', 'fence-only card fits without overflow', await ev(`(() => { const c=cards[1], b=c.querySelector('.body'); return !b || b.scrollHeight-b.clientHeight <= 0; })()`));

/* ── summary ──────────────────────────────────────────── */
console.log('\n=== md2slides requirements suite ===');
let req = ''; const table = [];
for (const r of rows) {
  if (r.req !== req) { table.push([r.req, '—', '', ''].join('\t')); req = r.req; }
  table.push(['', r.kind === 'comprehensive' ? 'comp' : 'sanity', (r.ok ? 'PASS' : 'FAIL') + '  ' + r.name, r.detail].join('\t'));
}
console.log(table.map(x => x.split('\t').join('  |  ')).join('\n'));
console.log(`\nSUMMARY  ${pass} pass / ${fail} fail   (${sanity} sanity · ${comp} comprehensive)`);
proc.kill('SIGKILL');
process.exit(fail ? 1 : 0);