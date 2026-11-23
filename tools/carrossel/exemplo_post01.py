"""Gera o carrossel 01 (pauta local RMPA) no template CETMob — 1080x1350."""
import asyncio, pathlib
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).parent  # tools/carrossel
A = (ROOT.parent / "assets").as_uri()
import sys
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "saida"
OUT.mkdir(exist_ok=True)

NAVY, BLUE, ORANGE, INK, PAPER = "#2c2793", "#3488c1", "#fc8b3f", "#1b1849", "#f6f5fb"
TOTAL = 5

CSS = f"""
@font-face {{ font-family: R; src: url('file:///usr/share/fonts/truetype/google-fonts/ofl/roboto/Roboto[wdth,wght].ttf'); font-weight: 100 900; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1350px; overflow: hidden; }}
body {{ font-family: R, sans-serif; position: relative; }}
.dark {{ background: {NAVY}; color: #fff; }}
.light {{ background: {PAPER}; color: {INK}; }}
.pad {{ position: absolute; inset: 0; padding: 96px 88px 150px; display: flex; flex-direction: column; }}
/* faixas da marca no canto */
.bars {{ position: absolute; top: 0; right: 88px; display: flex; gap: 14px; align-items: flex-start; }}
.bars i {{ display: block; width: 22px; border-radius: 0 0 6px 6px; }}
.kicker {{ font-size: 30px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: {ORANGE}; margin-bottom: 28px; }}
h1 {{ font-size: 92px; line-height: 1.02; font-weight: 800; letter-spacing: -1.5px; }}
h2 {{ font-size: 64px; line-height: 1.06; font-weight: 800; letter-spacing: -1px; color: {NAVY}; }}
.dark h2 {{ color: #fff; }}
.lead {{ font-size: 38px; line-height: 1.35; font-weight: 400; margin-top: 36px; }}
.dark .lead {{ color: #dcdaf3; }}
.light .lead {{ color: #3b3870; }}
footer {{ position: absolute; left: 88px; right: 88px; bottom: 56px; display: flex; align-items: center; justify-content: space-between; }}
footer img {{ height: 52px; }}
footer .pg {{ font-size: 26px; font-weight: 600; letter-spacing: 2px; }}
.dark footer .pg {{ color: #b9b6e6; }}
.light footer .pg {{ color: #8a87b8; }}
.chips {{ display: flex; gap: 20px; margin-top: auto; }}
.chip {{ border: 3px solid {ORANGE}; border-radius: 18px; padding: 22px 28px; }}
.chip b {{ display: block; font-size: 26px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: {ORANGE}; }}
.chip span {{ display: block; font-size: 54px; font-weight: 800; margin-top: 4px; }}
.swipe {{ font-size: 28px; font-weight: 600; color: {ORANGE}; margin-top: 40px; letter-spacing: 1px; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 48px; }}
.card {{ background: #fff; border-radius: 22px; padding: 40px 34px 40px; border-top: 10px solid {BLUE}; box-shadow: 0 2px 0 rgba(44,39,147,.06); }}
.card.o {{ border-top-color: {ORANGE}; }}
.card .big {{ font-size: 66px; font-weight: 800; color: {NAVY}; line-height: 1; letter-spacing: -1px; }}
.card .big small {{ font-size: 36px; font-weight: 700; }}
.card p {{ font-size: 28px; line-height: 1.32; color: #3b3870; margin-top: 14px; }}
.note {{ margin-top: 40px; font-size: 31px; line-height: 1.4; color: #3b3870; background: #e9e7f6; border-left: 8px solid {NAVY}; border-radius: 0 14px 14px 0; padding: 22px 26px; }}
.flow {{ margin-top: 44px; display: flex; flex-direction: column; gap: 0; }}
.step {{ display: flex; align-items: center; gap: 28px; background: #fff; border-radius: 20px; padding: 30px 32px; }}
.num {{ flex: 0 0 74px; height: 74px; border-radius: 50%; background: {NAVY}; color: #fff; font-size: 36px; font-weight: 800; display: flex; align-items: center; justify-content: center; }}
.step.o .num {{ background: {ORANGE}; }}
.step.b .num {{ background: {BLUE}; }}
.step h3 {{ font-size: 34px; font-weight: 800; color: {NAVY}; }}
.step p {{ font-size: 29px; line-height: 1.3; color: #3b3870; margin-top: 4px; }}
.arrow {{ width: 6px; height: 36px; background: #c9c6ea; margin-left: 64px; }}
ul.pts {{ list-style: none; margin-top: 56px; display: flex; flex-direction: column; gap: 44px; }}
ul.pts li {{ display: flex; gap: 26px; align-items: flex-start; }}
ul.pts li i {{ flex: 0 0 18px; height: 64px; border-radius: 6px; margin-top: 4px; }}
ul.pts li div b {{ display: block; font-size: 40px; font-weight: 800; color: {NAVY}; }}
ul.pts li div span {{ display: block; font-size: 32px; line-height: 1.35; color: #3b3870; margin-top: 6px; }}
.disc {{ margin-top: auto; background: {NAVY}; color: #fff; border-radius: 20px; padding: 28px 32px; font-size: 31px; line-height: 1.4; }}
.disc b {{ color: {ORANGE}; }}
.tl {{ margin-top: 50px; position: relative; padding-left: 72px; }}
.tl:before {{ content: ''; position: absolute; left: 23px; top: 16px; bottom: 40px; width: 6px; background: rgba(255,255,255,.25); border-radius: 3px; }}
.ev {{ position: relative; margin-bottom: 46px; }}
.ev:before {{ content: ''; position: absolute; left: -72px; top: 6px; width: 40px; height: 40px; border-radius: 50%; background: {NAVY}; border: 6px solid {BLUE}; }}
.ev.now:before {{ border-color: {ORANGE}; background: {ORANGE}; }}
.ev.tbd:before {{ border-style: dashed; border-color: #b9b6e6; }}
.ev b {{ font-size: 40px; font-weight: 800; }}
.ev.now b {{ color: {ORANGE}; }}
.ev span {{ display: block; font-size: 30px; color: #dcdaf3; margin-top: 4px; line-height: 1.3; }}
.cta {{ margin-top: auto; font-size: 34px; line-height: 1.35; font-weight: 600; border-top: 3px solid rgba(255,255,255,.2); padding-top: 30px; }}
.src {{ font-size: 23px; color: #b9b6e6; margin-top: 18px; font-weight: 400; }}
"""

def bars(colors=(ORANGE, BLUE, ORANGE), heights=(150, 110, 70)):
    return '<div class="bars">' + "".join(f'<i style="background:{c};height:{h}px"></i>' for c, h in zip(colors, heights)) + "</div>"

def footer(n, dark):
    logo = "CETMob-logo-reduzido-horizontal-BRANCO.svg" if dark else "CETMob-logo-reduzido-horizontal-COLORIDO.svg"
    return f'<footer><img src="{A}/{logo}"><span class="pg">{n:02d} / {TOTAL:02d}</span></footer>'

def page(body, n, dark):
    cls = "dark" if dark else "light"
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{bars()}<div class="pad">{body}</div>{footer(n, dark)}</body></html>'

slides = []

# 1 — capa
slides.append(page(f"""
<div class="kicker">Mobilidade na RMPA</div>
<h1>Pix e cartão no ônibus metropolitano?</h1>
<p class="lead">O Governo do RS está licitando a nova bilhetagem eletrônica dos ônibus da Região Metropolitana de Porto Alegre.</p>
<div style="margin-top:56px;display:flex;align-items:center;gap:44px">
<svg width="300" height="330" viewBox="0 0 300 330">
  <rect x="40" y="10" width="200" height="310" rx="34" fill="#3d38a8" stroke="#5b56c4" stroke-width="4"/>
  <rect x="70" y="44" width="140" height="92" rx="14" fill="#1b1849"/>
  <text x="140" y="104" text-anchor="middle" font-family="R" font-weight="800" font-size="40" fill="#fc8b3f">✓</text>
  <g fill="none" stroke="#3488c1" stroke-width="12" stroke-linecap="round">
    <path d="M118 190 q16 26 0 52"/><path d="M142 176 q26 40 0 80"/><path d="M166 162 q36 54 0 108"/>
  </g>
</svg>
<div style="display:flex;flex-direction:column;gap:18px">
  <span style="background:#fc8b3f;color:#1b1849;font-weight:800;font-size:46px;padding:14px 34px;border-radius:60px">Pix</span>
  <span style="background:#3488c1;color:#fff;font-weight:800;font-size:46px;padding:14px 34px;border-radius:60px">Crédito</span>
  <span style="background:#fff;color:#2c2793;font-weight:800;font-size:46px;padding:14px 34px;border-radius:60px">Débito</span>
</div></div>
<div class="chips">
  <div class="chip"><b>Propostas</b><span>25/11</span></div>
  <div class="chip"><b>Leilão</b><span>02/12</span></div>
</div>
<div class="swipe">Arraste para entender →</div>
""", 1, True))

# 2 — números
slides.append(page(f"""
<div class="kicker">O que está sendo licitado</div>
<h2>Uma PPP só para cobrar e registrar as viagens</h2>
<div class="grid">
  <div class="card"><div class="big">R$ 100 <small>mi</small></div><p>valor estimado do contrato</p></div>
  <div class="card"><div class="big">10 <small>anos</small></div><p>de concessão administrativa (PPP)</p></div>
  <div class="card o"><div class="big" style="font-size:44px;line-height:1.1">Menor contra&shy;prestação</div><p>mensal paga pelo Estado vence a disputa</p></div>
  <div class="card o"><div class="big" style="font-size:44px;line-height:1.1">Crédito, débito e Pix</div><p>outros meios podem ser credenciados depois</p></div>
</div>
<div class="note">É um contrato <b>separado</b> da concessão das linhas de ônibus, que tem edital próprio. A bilhetagem não define quem vai operar as linhas.</div>
""", 2, False))

# 3 — como funciona ABT
slides.append(page(f"""
<div class="kicker">Por dentro do sistema</div>
<h2>Bilhetagem baseada em contas (ABT)</h2>
<p class="lead" style="font-size:31px;margin-top:22px">No modelo tradicional, o saldo fica gravado no cartão. No ABT, o cartão ou o celular é só um identificador: a conta e as regras de tarifa ficam no servidor.</p>
<div class="flow">
  <div class="step b"><div class="num">1</div><div><h3>Passageiro</h3><p>Paga com cartão de crédito, débito ou Pix</p></div></div>
  <div class="arrow"></div>
  <div class="step b"><div class="num">2</div><div><h3>Validador no ônibus</h3><p>Só identifica o meio e registra a viagem</p></div></div>
  <div class="arrow"></div>
  <div class="step"><div class="num">3</div><div><h3>Plataforma na nuvem</h3><p>Calcula a tarifa, aplica as regras e checa fraudes</p></div></div>
  <div class="arrow"></div>
  <div class="step o"><div class="num">4</div><div><h3><i>Clearing house</i></h3><p>Compensa os valores e repassa às operadoras</p></div></div>
</div>
""", 3, False))

# 4 — por que importa
slides.append(page(f"""
<div class="kicker">Olhar de engenharia</div>
<h2>Por que isso vai além da catraca</h2>
<ul class="pts">
  <li><i style="background:{BLUE}"></i><div><b>Integração tarifária</b><span>Com as regras no servidor, pode ficar mais simples configurar descontos e integrações entre linhas e municípios.</span></div></li>
  <li><i style="background:{ORANGE}"></i><div><b>Dados para planejar</b><span>Viagens, pagamentos e dados de passageiros numa só plataforma ajudam a entender a demanda real da rede.</span></div></li>
  <li><i style="background:{NAVY}"></i><div><b>Antifraude × privacidade</b><span>O edital prevê biometria facial. Como equilibrar controle e proteção de dados (LGPD)?</span></div></li>
</ul>
<div class="disc">No CETMob, esse tema passa por <b>Sistemas Inteligentes de Transporte</b>, <b>Programação voltada à Mobilidade</b> e <b>Transporte Público de Passageiros</b>.</div>
""", 4, False))

# 5 — linha do tempo + CTA
slides.append(page(f"""
<div class="kicker">Próximos passos</div>
<h2>Linha do tempo</h2>
<div class="tl">
  <div class="ev"><b>29/09</b><span>Edital publicado</span></div>
  <div class="ev now"><b>25/11</b><span>Entrega das propostas</span></div>
  <div class="ev now"><b>02/12 · 14h</b><span>Disputa na Central de Licitações do Estado (Celic)</span></div>
  <div class="ev tbd"><b>Implantação</b><span>Sem data definida: depende da contratação e da instalação dos equipamentos</span></div>
</div>
<div class="cta">Pagar com Pix ou cartão mudaria o seu deslocamento na RMPA? Conta pra gente nos comentários.
<div class="src">Fontes: Governo do RS (RS Parcerias) · Diário do Transporte (29/09/2026)</div></div>
""", 5, True))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, html in enumerate(slides, 1):
            f = OUT / f"slide{i:02d}.html"
            f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri())
            await pg.wait_for_timeout(400)
            png = OUT / f"slide{i:02d}.png"
            await pg.screenshot(path=str(png))
            Image.open(png).convert("RGB").save(OUT / f"slide{i:02d}.jpg", "JPEG", quality=92)  # Instagram exige JPEG
        await b.close()

asyncio.run(main())
print("ok")
