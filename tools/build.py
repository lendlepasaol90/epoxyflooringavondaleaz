#!/usr/bin/env python3
"""Builds the static site into ../public.

Edit BUSINESS below (phone, email) or tools/content.json (service copy), then run:
    python3 tools/build.py
Shared styles and scripts live in public/assets/.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, '..', 'public')

BUSINESS = {
    'name': 'Epoxy Flooring Avondale AZ',
    'phone': '(623) 555-0148',
    'phone_href': '+16235550148',
    'email': 'hello@epoxyflooringavondaleaz.com',
    'city': 'Avondale, AZ 85323',
    'domain': 'https://epoxyflooringavondaleaz.com',
}

ICONS = {
    '01': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M3 10l9-6 9 6v10H3z"/><path d="M7 20v-6h10v6M7 17h10"/></svg>',
    '02': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M3 21V9l9-6 9 6v12"/><path d="M9 21v-7h6v7"/></svg>',
    '03': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="3" y="7" width="18" height="14"/><path d="M3 11h18M8 7V3h8v4M8 15h2M14 15h2"/></svg>',
    '04': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M2 21V8l10-5 10 5v13"/><path d="M6 21v-8h12v8M6 17h12"/></svg>',
    '05': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M3 20h18M5 20V10h14v10"/><path d="M3 10l9-6 9 6"/><path d="M9 14h6"/></svg>',
    '06': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="7" cy="8" r="1.4"/><circle cx="15" cy="6" r="1.1"/><circle cx="17" cy="14" r="1.6"/><circle cx="9" cy="16" r="1.1"/><circle cx="12" cy="11" r="1"/><rect x="3" y="3" width="18" height="18" rx="3"/></svg>',
    '07': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    '08': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
    '09': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 15c3-4 5 2 9-2s6 1 9-3"/><path d="M3 19c3-3 6 1 9-2s6 1 9-2"/><path d="M3 10c3-4 6 1 9-3s5 0 9-3"/></svg>',
}

# number, menu name, short description
SERVICES = [
    ('01', 'Garage Floor Coatings', 'Resist hot-tire pickup, oil and dust so the garage feels like part of the house.'),
    ('02', 'Residential Epoxy Flooring', 'Garages, workshops, home gyms and suitable concrete living spaces.'),
    ('03', 'Commercial Epoxy Flooring', 'Retail, showrooms, auto shops and offices that need durability and a sharp look.'),
    ('04', 'Warehouse Floor Coatings', 'Built for forklifts, pallet jacks, racking, striping and daily operations.'),
    ('05', 'Patio & Concrete Coatings', 'Outdoor systems for patios, pool decks and walkways in Arizona sun.'),
    ('06', 'Decorative Flake Flooring', 'Multicolor vinyl chips broadcast into the base coat for texture and depth.'),
    ('07', 'Polyaspartic Floor Coatings', 'UV-stable, fast-curing topcoats for sun-exposed garages.'),
    ('08', 'Polyurea Floor Coatings', 'Flexible, rapid-reacting coatings for temperature swings and heavy use.'),
    ('09', 'Metallic Epoxy Flooring', 'Pearlescent pigments that swirl into a one-of-a-kind, high-gloss floor.'),
]

CONTENT = json.load(open(os.path.join(ROOT, 'content.json')))
SVC = {}
for num, name, short in SERVICES:
    slug = CONTENT[num]['seo']['Recommended URL Slug'].strip('/')
    SVC[num] = dict(num=num, name=name, short=short, slug=slug, href='/' + slug + '/', icon=ICONS[num])


def norm(s):
    return re.sub(r'[^a-z]', '', s.lower().replace('patio/concrete', 'patioconcrete').replace('&', ''))

BY_NAME = {norm(s['name']): s for s in SVC.values()}


def esc(s):
    return html.escape(s, quote=False)


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>'
B = BUSINESS
CUR = ' aria-current="page"'


def head(title, desc, path):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{B['domain']}{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
'''


def header(active=None):
    items = ''.join(
        f'<a href="{s["href"]}"{CUR if s["num"] == active else ""}><span class="dd-ico">{s["icon"]}</span><span><b>{esc(s["name"])}</b><small>{esc(s["short"])}</small></span></a>'
        for s in SVC.values())
    return f'''<div class="topbar"><div class="wrap">
  <span>Serving Avondale, Goodyear, Tolleson &amp; the West Valley</span>
  <div style="display:flex;gap:22px;flex-wrap:wrap"><a href="tel:{B['phone_href']}">{B['phone']}</a><a href="mailto:{B['email']}">{B['email']}</a></div>
</div></div>

<header class="nav" id="nav"><div class="wrap">
  <a class="logo" href="/" aria-label="{B['name']} home">
    <span class="logo-mark">LOGO</span>
    <span><b>Epoxy Flooring</b><small>Avondale · AZ</small></span>
  </a>
  <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  <ul class="menu" id="menu">
    <li><a href="/"{' aria-current="page"' if active == 'home' else ''}>Home</a></li>
    <li class="has-dd"><button class="dd-toggle" aria-expanded="false" aria-haspopup="true">Services {CHEV}</button>
      <div class="dd" role="menu">{items}<a class="dd-all" href="/#services"><span>View all services</span>{ARROW}</a></div></li>
    <li><a href="/#process">Process</a></li>
    <li><a href="/#why">Why Us</a></li>
    <li><a href="/#faq">FAQ</a></li>
    <li><a class="btn btn-primary" href="#estimate">Free Estimate</a></li>
  </ul>
</div></header>
'''


def footer():
    links = ''.join(f'<li><a href="{s["href"]}">{esc(s["name"])}</a></li>' for s in SVC.values())
    return f'''
<footer><div class="wrap">
  <div class="foot">
    <div>
      <a class="logo" href="/"><span class="logo-mark" style="border-color:var(--orange)">LOGO</span><span><b>Epoxy Flooring</b><small>Avondale · AZ</small></span></a>
      <p>Garage, residential, commercial and warehouse floor coatings for Avondale and the West Valley.</p>
    </div>
    <div><h4>Services</h4><ul>{links}</ul></div>
    <div><h4>Contact</h4><ul>
      <li><a href="tel:{B['phone_href']}">{B['phone']}</a></li><li><a href="mailto:{B['email']}" style="word-break:break-all">{B['email']}</a></li><li style="opacity:.8">{B['city']}</li><li><a href="#estimate">Request an Estimate</a></li></ul></div>
  </div>
  <div class="copy"><span>© 2026 {B['name']}</span><span>Epoxy · Flake · Metallic · Polyaspartic · Polyurea</span></div>
</div></footer>

<div class="callbar"><a class="btn btn-ghost" href="tel:{B['phone_href']}">Call Now</a><a class="btn btn-primary" href="#estimate">Free Estimate</a></div>
<script src="/assets/site.js"></script>
'''


def tail(jsonld=None):
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j)}</script>\n' for j in (jsonld or []))
    return footer() + ld + '</body>\n</html>\n'


def contact_lines():
    return f'''<div class="contact-lines reveal">
        <div><span class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/></svg></span><a href="tel:{B['phone_href']}">{B['phone']}</a></div>
        <div><span class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span><a href="mailto:{B['email']}" style="word-break:break-all">{B['email']}</a></div>
        <div><span class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s-7-6.5-7-12a7 7 0 0114 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg></span><span>{B['city']}</span></div>
      </div>'''


def callback_form(service):
    return f'''<form class="form-card lead-form" id="callback" novalidate data-ok="We received your request and will call you back soon.">
      <h3>Request a Callback</h3>
      <p class="sub">Tell us about your floor and we will reach out to talk through {esc(service.lower())} options.</p>
      <div class="field"><label for="cb-name">Name</label><input id="cb-name" name="name" autocomplete="name" required placeholder="Jane Smith"></div>
      <div class="field"><label for="cb-email">Email Address</label><input id="cb-email" name="email" type="email" autocomplete="email" required placeholder="jane@email.com"></div>
      <div class="field"><label for="cb-phone">Phone Number</label><input id="cb-phone" name="phone" type="tel" autocomplete="tel" placeholder="(623) 555-0100"></div>
      <button class="btn btn-primary" type="submit">Request My Callback</button>
      <div class="form-ok" hidden role="status"></div>
    </form>'''


def estimate_form(prefill=''):
    return f'''<form class="form-card reveal lead-form" id="estimate-form" novalidate data-ok="Your estimate request is in. We will be in touch within one business day.">
      <h3>Request a Free Estimate</h3>
      <p class="sub">Share the location, approximate square footage, current floor condition and how you use the space.</p>
      <div class="field"><label for="es-name">Name</label><input id="es-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="es-email">Email Address</label><input id="es-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="es-phone">Phone Number</label><input id="es-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="es-msg">Project details or question</label><textarea id="es-msg" name="message" rows="3" placeholder="{html.escape(prefill)}"></textarea></div>
      <button class="btn btn-primary" type="submit">Send Request</button>
      <div class="form-ok" hidden role="status"></div>
    </form>'''


def svc_card(s, cls='svc reveal'):
    return f'<a class="{cls}" href="{s["href"]}"><span class="num">{s["num"]}</span><span class="ico">{s["icon"]}</span><h3>{esc(s["name"])}</h3><p>{esc(s["short"])}</p></a>'


def marquee():
    names = ''.join(f'<span>{esc(s["name"])}</span>' for s in SVC.values())
    return f'<div class="marquee" aria-hidden="true"><div class="track">{names}{names}</div></div>\n'


def paras(items):
    return '\n'.join(f'<p>{esc(t)}</p>' for k, t in items if k == 'p')


def pairs(items):
    out, cur = [], None
    for k, t in items:
        if k == 'h3':
            cur = [t, []]; out.append(cur)
        elif cur:
            cur[1].append(t)
    return out


CALLOUTS = ('Why Professional Installation Matters', 'Why Choose Epoxy Flooring Avondale AZ')
AREAS = ['Avondale', 'Goodyear', 'Litchfield Park', 'Tolleson', 'Glendale', 'Phoenix', 'Buckeye', 'Laveen']


def service_page(s):
    c = CONTENT[s['num']]
    seo = c['seo']
    secs = {x['h']: x for x in c['sections']}
    order = [x['h'] for x in c['sections']]
    intro = c['intro'][-1]
    h1 = c['h1'].split(' | ')[0]
    m = re.match(r'(.*?) in (Avondale, AZ)$', h1)
    if m:
        h1_html = (' '.join(f'<span class="w" style="animation-delay:{i*0.06:.2f}s">{esc(w)}</span>' for i, w in enumerate(m.group(1).split()))
                   + f' <span class="w" style="animation-delay:{len(m.group(1).split())*0.06:.2f}s">in</span> <span class="w hl" style="animation-delay:{(len(m.group(1).split())+1)*0.06:.2f}s">Avondale,&nbsp;AZ<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M4 14 C 80 4, 200 4, 296 12"/></svg></span>')
    else:
        h1_html = esc(h1)

    intro_sec = secs[order[0]]
    pro_sec = secs[order[1]]
    pro_text = [[k, t[len(intro):].strip() if t.startswith(intro) else t] for k, t in pro_sec['items']]
    pro_text = [x for x in pro_text if x[1]]
    ben_sec = secs[order[2]]
    tail_names = ['Why Choose Epoxy Flooring Avondale AZ', 'Service Areas', 'Frequently Asked Questions', 'Ready to Discuss Your Floor?']
    body_names = [n for n in order[3:] if n not in tail_names] + ['Why Choose Epoxy Flooring Avondale AZ']
    faqs = pairs(secs['Frequently Asked Questions']['items'])

    blocks, toc = [], []
    for n in body_names:
        bid = slugify(n)
        toc.append(f'<li><a href="#{bid}">{esc(n)}</a></li>')
        cls = 'block callout reveal' if n in CALLOUTS else 'block reveal'
        blocks.append(f'<div class="{cls}" id="{bid}"><h2>{esc(n)}</h2>{paras(secs[n]["items"])}</div>')
    toc.append('<li><a href="#faq">Frequently Asked Questions</a></li>')

    bens = ''.join(
        f'<div class="ben-card reveal"><span class="num">{i+1:02d}</span><h3>{esc(h)}</h3>{"".join("<p>"+esc(p)+"</p>" for p in ps)}</div>'
        for i, (h, ps) in enumerate(pairs(ben_sec['items'])))
    faq_html = ''.join(
        f'<details class="reveal"{" open" if i == 0 else ""}><summary>{esc(q)}<span class="pm"></span></summary><div class="ans">{"".join("<p>"+esc(a)+"</p>" for a in ans)}</div></details>'
        for i, (q, ans) in enumerate(faqs))

    related = []
    for n in seo['Suggested Internal Links'].split(','):
        r = BY_NAME.get(norm(n))
        assert r, n
        related.append(svc_card(r))

    areas = ''.join(f'<span>{a}</span>' for a in AREAS)
    ready = secs['Ready to Discuss Your Floor?']
    ready_p = [t.replace(' Visit epoxyflooringavondaleaz.com to learn more or inquire about your project.', '') for k, t in ready['items'] if k == 'p']

    jsonld = [
        {'@context': 'https://schema.org', '@type': 'Service', 'name': h1, 'serviceType': s['name'],
         'areaServed': {'@type': 'City', 'name': 'Avondale, AZ'},
         'provider': {'@type': 'LocalBusiness', 'name': B['name'], 'telephone': B['phone'], 'email': B['email'],
                      'url': B['domain'], 'address': {'@type': 'PostalAddress', 'addressLocality': 'Avondale', 'addressRegion': 'AZ', 'postalCode': '85323', 'addressCountry': 'US'}},
         'url': B['domain'] + s['href'], 'description': seo['Meta Description']},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(a)}} for q, a in faqs]},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': B['domain'] + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': s['name'], 'item': B['domain'] + s['href']}]},
    ]

    page = head(seo['SEO Title'], seo['Meta Description'], s['href']) + '<div id="progress" aria-hidden="true"></div>\n' + header(s['num']) + f'''
<main id="top">
<section class="hero page-hero">
  <canvas id="flakes" aria-hidden="true"></canvas>
  <div class="wrap">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/#services">Services</a><span>/</span><span aria-current="page">{esc(s["name"])}</span></nav>
      <h1>{h1_html}</h1>
      <p class="lead">{esc(intro)}</p>
      <div class="ctas">
        <a class="btn btn-primary" href="#estimate">Get a Free Estimate {ARROW}</a>
        <a class="btn btn-ghost" href="tel:{B['phone_href']}">Call {B['phone']}</a>
      </div>
    </div>
    {callback_form(s['name'])}
  </div>
</section>

{marquee()}
<section class="svc-intro" id="overview">
  <div class="wrap split">
    <div style="display:grid;gap:22px">
      <span class="eyebrow reveal">{esc(order[0].split(':')[0])}</span>
      <h2 class="h2 reveal">{esc(order[0].split(': ')[-1])}</h2>
      <div class="prose reveal">{paras(intro_sec['items'])}</div>
      <h3 class="reveal" style="font-size:26px;font-weight:800;margin-top:10px">{esc(order[1])}</h3>
      <div class="prose reveal">{paras(pro_text)}</div>
    </div>
    <div class="photo-wrap reveal">
      <div class="photo tall"><span>Photo · {esc(s['name'])}</span></div>
      <div class="badge">Prep first. Coating second. That order is the whole job.</div>
    </div>
  </div>
</section>

<section class="services" id="benefits">
  <div class="wrap">
    <span class="eyebrow reveal">Benefits</span>
    <h2 class="h2 reveal" style="margin-top:14px">{esc(order[2])}</h2>
    <div class="ben-grid">{bens}</div>
  </div>
</section>

<section id="details">
  <div class="wrap layout">
    <article class="article">
      {''.join(blocks)}
    </article>
    <aside class="aside">
      <nav class="toc" aria-label="On this page"><h4>On this page</h4><ol>{''.join(toc)}</ol></nav>
      <div class="side-cta">
        <h4>Get a free {esc(s['name'].lower())} estimate</h4>
        <p>Call or send the form and we will talk through preparation, finish and timing.</p>
        <a class="tel" href="tel:{B['phone_href']}">{B['phone']}</a>
        <a class="btn btn-primary" href="#estimate">Request Estimate</a>
      </div>
    </aside>
  </div>
</section>

<section class="band" id="area">
  <div class="wrap">
    <span class="eyebrow reveal">Service Areas</span>
    <h2 class="h2 reveal" style="margin-top:14px;max-width:22ch">{esc(s['name'])} across the West Valley</h2>
    <p class="lead reveal" style="margin-top:18px">{esc(' '.join(t for k, t in secs['Service Areas']['items'] if k == 'p'))}</p>
    <div class="areas reveal">{areas}</div>
  </div>
</section>

<section id="faq">
  <div class="wrap faq">
    <div style="display:grid;gap:18px;position:sticky;top:110px">
      <span class="eyebrow reveal">FAQ</span>
      <h2 class="h2 reveal">{esc(s['name'])} questions</h2>
      <p class="lead reveal">Have a different question? Send it with the estimate form below and we will answer it directly.</p>
      <div class="reveal"><a class="btn btn-primary" href="#estimate">Ask a Question</a></div>
    </div>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>

<section class="services" id="related">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:0">
      <div><span class="eyebrow reveal">Related Services</span><h2 class="h2 reveal">You may also be considering</h2></div>
      <a class="btn btn-ghost reveal" href="/#services">All Services</a>
    </div>
    <div class="related">{''.join(related)}</div>
  </div>
</section>

<section class="cta" id="estimate">
  <span class="ring" style="width:520px;height:520px;right:-160px;top:-180px"></span>
  <span class="ring" style="width:340px;height:340px;left:-120px;bottom:-140px;animation-delay:-3s"></span>
  <div class="wrap">
    <div>
      <h2 class="reveal">Ready to discuss your floor?</h2>
      {''.join('<p class="reveal">' + esc(p) + '</p>' for p in ready_p)}
      {contact_lines()}
    </div>
    {estimate_form('e.g. ' + s['name'].lower() + ', about 450 sq ft, current floor condition')}
  </div>
</section>
</main>
''' + tail(jsonld)
    out = os.path.join(PUBLIC, s['slug'])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w').write(page)


def home_page():
    main = open(os.path.join(ROOT, 'home-main.html')).read()
    grid = '\n      '.join(svc_card(s) for s in SVC.values())
    main = re.sub(r'(<div class="grid-svc">).*?(\n    </div>\n  </div>\n</section>)', lambda m: m.group(1) + '\n      ' + grid + m.group(2), main, count=1, flags=re.S)
    main = main.replace('<a class="btn btn-primary" href="#estimate">Price My Garage', f'<a class="btn btn-primary" href="{SVC["01"]["href"]}">Garage Floor Coatings')
    main = main.replace('<form class="form-card"', '<form class="form-card lead-form" data-ok="We received your request and will call you back soon."')
    main = main.replace('<form class="form-card reveal"', '<form class="form-card reveal lead-form" data-ok="Your estimate request is in. We will be in touch within one business day."')
    main = main.replace('(623) 555-0148', B['phone']).replace('tel:+16235550148', 'tel:' + B['phone_href']).replace('hello@epoxyflooringavondaleaz.com', B['email'])
    page = head('Epoxy Flooring Avondale AZ | Garage & Commercial Floor Coatings',
                'Garage, residential, commercial and warehouse epoxy flooring in Avondale, AZ. Flake, metallic, polyaspartic and polyurea floor coatings.', '/') + header('home') + main + tail([
        {'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': B['name'], 'telephone': B['phone'], 'email': B['email'], 'url': B['domain'],
         'address': {'@type': 'PostalAddress', 'addressLocality': 'Avondale', 'addressRegion': 'AZ', 'postalCode': '85323', 'addressCountry': 'US'}}])
    open(os.path.join(PUBLIC, 'index.html'), 'w').write(page)


def not_found():
    page = head('Page Not Found | Epoxy Flooring Avondale AZ', 'This page could not be found.', '/404') + header() + f'''
<main id="top"><section><div class="wrap page-404">
  <h1>404</h1>
  <h2 class="h2">This page isn't here.</h2>
  <p class="lead">The link may be old or mistyped. Head back home or pick a service.</p>
  <div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center"><a class="btn btn-primary" href="/">Back to Home {ARROW}</a><a class="btn btn-ghost" href="/#services">View Services</a></div>
</div></section></main>
''' + tail()
    open(os.path.join(PUBLIC, '404.html'), 'w').write(page)


def sitemap():
    urls = ['/'] + [s['href'] for s in SVC.values()]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{B["domain"]}{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(PUBLIC, 'sitemap.xml'), 'w').write(xml)
    open(os.path.join(PUBLIC, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {B["domain"]}/sitemap.xml\n')


if __name__ == '__main__':
    home_page()
    for s in SVC.values():
        service_page(s)
    not_found()
    sitemap()
    print('Built home +', len(SVC), 'service pages')
