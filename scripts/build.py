"""Generates /insights, /pt/insights, the home page lists and sitemap.xml.

Run from the project root:  python scripts/build.py
Article images are optional: drop assets/insights/<id>.jpg and re-run.
"""
import html
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://manuelpadrao.com"
COZE = "https://cozecare.com/"
LINKEDIN = "https://www.linkedin.com/in/manuelpadrao"
ACTIVITY = "https://www.linkedin.com/feed/update/urn:li:activity:"

# Each article: id (image name), activity, date, per-language slug/title/summary/body.
# Body paragraphs may use {coze:anchor} to link to cozecare.com.
ARTICLES = [
    {
        "id": "employees-productivity",
        "activity": None,
        "date": date(2026, 10, 23),
        "en": {
            "slug": "mental-health-affects-productivity",
            "title": "Is mental health getting enough attention?",
            "desc": "70% of employees say their mental health affects their productivity.",
            "body": [
                "The impact of mental health struggles often goes unnoticed, but it’s felt every day.",
                "70% of employees say their mental health affects their productivity.",
                "Behind every statistic is a person who deserves to feel supported, understood and heard.",
                "{coze:Cozecare} believes {coze:mental health} deserves attention before things become overwhelming.",
            ],
        },
        "pt": {
            "slug": "saude-mental-afeta-produtividade",
            "title": "A saúde mental recebe atenção suficiente?",
            "desc": "70% dos colaboradores dizem que a sua saúde mental afeta a produtividade.",
            "body": [
                "O impacto das dificuldades de saúde mental passa muitas vezes despercebido, mas sente-se todos os dias.",
                "70% dos colaboradores dizem que a sua saúde mental afeta a sua produtividade.",
                "Por trás de cada estatística está uma pessoa que merece sentir-se apoiada, compreendida e ouvida.",
                "A {coze:Cozecare} acredita que a {coze:saúde mental} merece atenção antes de as coisas se tornarem esmagadoras.",
            ],
        },
    },
    {
        "id": "business-priority",
        "activity": "7515067776110051328",
        "date": date(2026, 10, 11),
        "en": {
            "slug": "mental-health-business-priority",
            "title": "Mental health is a business priority.",
            "desc": "Workplace stress costs Portuguese companies an estimated €36 million per day.",
            "body": [
                "€36 million, every single day. That’s the estimated daily cost of workplace stress and mental health problems in lost productivity for Portuguese companies.",
                "That’s over €13 billion every year.",
                "But behind these numbers are real people struggling with stress, anxiety and burnout.",
                "Mental health isn’t just a personal matter. It’s a business priority.",
                "{coze:Cozecare} believes prevention, accessible psychological support and healthier workplaces are essential to building stronger organisations.",
                "Because taking care of people means taking care of business.",
                "Source: Portuguese Psychologists Association (OPP), 2026.",
            ],
        },
        "pt": {
            "slug": "saude-mental-prioridade-empresarial",
            "title": "Saúde mental é uma prioridade de negócio.",
            "desc": "O stress no trabalho custa às empresas portuguesas cerca de 36 milhões de euros por dia.",
            "body": [
                "36 milhões de euros, todos os dias. Este é o custo diário estimado do stress e dos problemas de saúde mental no trabalho, em produtividade perdida, para as empresas portuguesas.",
                "São mais de 13 mil milhões de euros por ano.",
                "Mas por trás destes números estão pessoas reais a lidar com stress, ansiedade e burnout.",
                "A saúde mental não é apenas um assunto pessoal. É uma prioridade de negócio.",
                "A {coze:Cozecare} acredita que prevenção, apoio psicológico acessível e locais de trabalho mais saudáveis são essenciais para construir organizações mais fortes.",
                "Porque cuidar das pessoas é cuidar do negócio.",
                "Fonte: Ordem dos Psicólogos Portugueses (OPP), 2026.",
            ],
        },
    },
    {
        "id": "presenteeism",
        "activity": "7514772860406480896",
        "date": date(2026, 10, 10),
        "en": {
            "slug": "being-present-is-not-being-well",
            "title": "Being present doesn’t always mean being well.",
            "desc": "Presenteeism costs Portuguese companies an estimated €8.9 billion a year.",
            "body": [
                "Presenteeism is costing Portuguese companies an estimated €8.9 billion every year in lost productivity, according to the Portuguese Psychologists Association.",
                "That’s nearly twice the estimated cost of absenteeism. Employees may be physically present but struggling with stress, exhaustion or mental health challenges that affect their performance.",
                "Being present doesn’t always mean being well.",
                "{coze:Cozecare} believes {coze:workplace mental health} should go beyond reactive solutions, focusing on prevention, continuous support and accessible psychological care.",
                "Because employee wellbeing shouldn’t be addressed only when people reach breaking point.",
                "Source: Portuguese Psychologists Association (OPP), 2026.",
            ],
        },
        "pt": {
            "slug": "estar-presente-nao-e-estar-bem",
            "title": "Estar presente nem sempre significa estar bem.",
            "desc": "O presentismo custa às empresas portuguesas cerca de 8,9 mil milhões de euros por ano.",
            "body": [
                "O presentismo custa às empresas portuguesas cerca de 8,9 mil milhões de euros por ano em produtividade perdida, segundo a Ordem dos Psicólogos Portugueses.",
                "É quase o dobro do custo estimado do absentismo. Os colaboradores podem estar fisicamente presentes, mas a lidar com stress, exaustão ou desafios de saúde mental que afetam o seu desempenho.",
                "Estar presente nem sempre significa estar bem.",
                "A {coze:Cozecare} acredita que a {coze:saúde mental no trabalho} deve ir além das soluções reativas, com foco em prevenção, acompanhamento contínuo e cuidado psicológico acessível.",
                "Porque o bem-estar dos colaboradores não deve ser tratado só quando as pessoas chegam ao limite.",
                "Fonte: Ordem dos Psicólogos Portugueses (OPP), 2026.",
            ],
        },
    },
    {
        "id": "biggest-challenge",
        "activity": "7514250913935572992",
        "date": date(2026, 10, 9),
        "en": {
            "slug": "mental-health-biggest-health-challenge",
            "title": "Mental health is now perceived as the biggest health challenge of this era.",
            "desc": "45% of adults across 30 countries rank mental health issues ahead of cancer, obesity and cardiovascular disease.",
            "body": [
                "45% of adults across 30 countries identify mental health issues as one of the main health challenges in their societies today, ahead of cancer, obesity and cardiovascular disease.",
                "This reinforces something Cozecare strongly believes: mental healthcare cannot remain something people only turn to when they are already struggling.",
                "It needs to become more accessible, continuous and proactive.",
                "That’s what {coze:Cozecare} is building: {coze:mental health support} that goes beyond isolated moments of care and becomes part of everyday life.",
                "Source: Ipsos Health Service Report 2025. 23,172 adults online (under age 75) surveyed in 30 countries between July and August 2025.",
            ],
        },
        "pt": {
            "slug": "saude-mental-maior-desafio",
            "title": "A saúde mental é hoje vista como o maior desafio de saúde da atualidade.",
            "desc": "45% dos adultos em 30 países colocam a saúde mental à frente do cancro, da obesidade e das doenças cardiovasculares.",
            "body": [
                "45% dos adultos em 30 países identificam os problemas de saúde mental como um dos principais desafios de saúde das suas sociedades, à frente do cancro, da obesidade e das doenças cardiovasculares.",
                "Isto reforça algo em que a {coze:Cozecare} acredita muito: os cuidados de saúde mental não podem ser algo a que as pessoas só recorrem quando já estão a sofrer.",
                "Têm de ser mais acessíveis, contínuos e proativos.",
                "É isso que a {coze:Cozecare} está a construir: {coze:apoio em saúde mental} que vai além de momentos isolados de cuidado e passa a fazer parte do dia a dia.",
                "Fonte: Ipsos Health Service Report 2025. 23.172 adultos online (menos de 75 anos) inquiridos em 30 países entre julho e agosto de 2025.",
            ],
        },
    },
    {
        "id": "300-psychologists",
        "activity": "7510771334272987141",
        "date": date(2026, 9, 29),
        "en": {
            "slug": "300-psychologists-300k-people",
            "title": "300+ psychologists. 300K+ people covered.",
            "desc": "How Cozecare became one of the largest mental health platforms in Portugal.",
            "body": [
                "{coze:Cozecare} now has a network of 300+ psychologists and solutions that cover 300K+ people, one of the largest mental health platforms in Portugal.",
                "For individuals, Cozecare helps people find the right psychologist, access online sessions and stay supported between appointments with check-ins, personalised exercises and mindfulness.",
                "For companies, Cozecare combines access to professional care with prevention, burnout prevention and actionable wellbeing data for People teams.",
                "The goal is simple: make mental healthcare easier to access, continuous and personalised.",
            ],
        },
        "pt": {
            "slug": "300-psicologos-300-mil-pessoas",
            "title": "300+ psicólogos. 300 mil+ pessoas cobertas.",
            "desc": "Como a Cozecare se tornou uma das maiores plataformas de saúde mental em Portugal.",
            "body": [
                "A {coze:Cozecare} tem hoje uma rede de 300+ psicólogos e soluções que cobrem mais de 300 mil pessoas, uma das maiores plataformas de saúde mental em Portugal.",
                "Para pessoas, a Cozecare ajuda a encontrar o psicólogo certo, a aceder a sessões online e a manter apoio entre consultas, com check-ins, exercícios personalizados e mindfulness.",
                "Para empresas, a Cozecare combina acesso a cuidado profissional com prevenção, prevenção de burnout e dados de bem-estar acionáveis para as equipas de People.",
                "O objetivo é simples: uma saúde mental mais acessível, contínua e personalizada.",
            ],
        },
    },
    {
        "id": "burnout-risk",
        "activity": "7510023236953444352",
        "date": date(2026, 9, 27),
        "en": {
            "slug": "portugal-burnout-risk",
            "title": "Portugal ranked #1 for burnout risk in this European study.",
            "desc": "Why companies should move from reactive support to burnout prevention.",
            "body": [
                "Portugal ranked #1 for burnout risk in this European study.",
                "Burnout should not be something companies only address once employees are already struggling.",
                "{coze:Cozecare} helps organisations move from reactive support to prevention, continuous employee wellbeing and accessible workplace mental health care.",
                "Its approach works as a {coze:modern EAP alternative}, combining employee mental health support, online psychology, burnout prevention, wellbeing tools and actionable data for People teams.",
                "Because healthier workplaces are built before burnout happens.",
                "If you’re looking for an {coze:EAP in Portugal}, corporate mental health solution or workplace wellbeing platform, get in touch.",
            ],
        },
        "pt": {
            "slug": "portugal-risco-de-burnout",
            "title": "Portugal em 1.º lugar no risco de burnout neste estudo europeu.",
            "desc": "Porque as empresas devem passar do apoio reativo à prevenção do burnout.",
            "body": [
                "Portugal ficou em 1.º lugar no risco de burnout neste estudo europeu.",
                "O burnout não deve ser algo que as empresas só tratam quando os colaboradores já estão a sofrer.",
                "A {coze:Cozecare} ajuda as organizações a passar do apoio reativo para a prevenção, o bem-estar contínuo dos colaboradores e o acesso a cuidados de saúde mental no trabalho.",
                "A sua abordagem funciona como uma {coze:alternativa moderna a um EAP}, combinando apoio de saúde mental para colaboradores, psicologia online, prevenção de burnout, ferramentas de bem-estar e dados acionáveis para as equipas de People.",
                "Porque locais de trabalho mais saudáveis constroem-se antes de o burnout acontecer.",
                "Se procuras um {coze:EAP em Portugal}, uma solução de saúde mental corporativa ou uma plataforma de bem-estar no trabalho, entre em contacto.",
            ],
        },
    },
]

LANGS = {
    "en": {
        "prefix": "", "locale": "en_US", "html": "en", "other": "pt", "other_label": "PT",
        "label": "Insights", "title": "Insights", "back": "← Back", "all": "All insights",
        "read": "Read ↗", "linkedin": "Shared on LinkedIn ↗", "discover": "Discover Cozecare ↗",
        "idx_desc": "Notes by Manuel Padrão, Founder & CEO of Cozecare, on workplace mental health, burnout prevention and healthcare technology.",
        "nav": [("Insights", "/insights/")],
        "role": "Founder & CEO",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "fmt": lambda d, m: f"{m[d.month - 1]} {d.day}, {d.year}",
    },
    "pt": {
        "prefix": "/pt", "locale": "pt_PT", "html": "pt-PT", "other": "en", "other_label": "EN",
        "label": "Insights", "title": "Insights", "back": "← Voltar", "all": "Todos os insights",
        "read": "Ler ↗", "linkedin": "Partilhado no LinkedIn ↗", "discover": "Conhecer a Cozecare ↗",
        "idx_desc": "Notas de Manuel Padrão, Founder & CEO da Cozecare, sobre saúde mental no trabalho, prevenção de burnout e tecnologia na saúde.",
        "nav": [("Insights", "/pt/insights/")],
        "role": "Founder & CEO",
        "months": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
        "fmt": lambda d, m: f"{d.day} de {m[d.month - 1]} de {d.year}",
    },
}

e = html.escape

SOCIAL = '<div class="nav-social">\n          <a href="https://www.linkedin.com/in/manuelpadrao" target="_blank" rel="me noopener" aria-label="LinkedIn" title="LinkedIn">\n            <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452z"/></svg>\n          </a>\n          <a href="mailto:manuel@cozecare.com" aria-label="Email" title="manuel@cozecare.com">\n            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7.5 8 6 8-6"/></svg>\n          </a>\n        </div>\n\n        '


# Back goes to the page the reader came from (home or list); falls back to the list.
BACK_JS = """  <script>
    document.getElementById("back").addEventListener("click", function (ev) {
      try {
        if (history.length > 1 && document.referrer &&
            new URL(document.referrer).origin === location.origin) {
          ev.preventDefault();
          history.back();
        }
      } catch (err) {}
    });
  </script>
"""


def write(rel, content):
    path = os.path.join(ROOT, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def fmt_date(lang, d):
    L = LANGS[lang]
    return L["fmt"](d, L["months"])


def image_url(a):
    rel = f"assets/insights/{a['id']}.jpg"
    return f"/{rel}" if os.path.exists(os.path.join(ROOT, *rel.split("/"))) else None


def url_of(lang, a=None):
    p = LANGS[lang]["prefix"]
    return f"{p}/insights/" + (f"{a[lang]['slug']}/" if a else "")


def body_html(paras):
    def link(m):
        return f'<a href="{COZE}" target="_blank" rel="noopener">{e(m.group(1))}</a>'
    out = []
    for p in paras:
        parts = re.split(r"(\{coze:[^}]+\})", p)
        s = "".join(link(re.match(r"\{coze:([^}]+)\}", x)) if x.startswith("{coze:") else e(x) for x in parts)
        out.append(f"<p>{s}</p>")
    return "\n          ".join(out)


def head(lang, title, desc, path, alt_path, og_type="website", image=None, ld=""):
    L = LANGS[lang]
    other = LANGS[L["other"]]
    canon = SITE + path
    alt = f'<link rel="alternate" hreflang="{L["other"]}" href="{SITE}{alt_path}" />' if alt_path else ""
    self_alt = f'<link rel="alternate" hreflang="{lang}" href="{canon}" />' if alt_path else ""
    img = image or "/assets/manuel-padrao.jpg"
    return f"""<!DOCTYPE html>
<html lang="{L['html']}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <meta name="author" content="Manuel Padrão" />
  <meta name="robots" content="index, follow, max-image-preview:large" />

  <link rel="canonical" href="{canon}" />
  {self_alt}
  {alt}

  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="{SITE}{img}" />
  <meta property="og:locale" content="{L['locale']}" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="stylesheet" href="/assets/style.css" />
{ld}
</head>
"""


def header_html(lang, alt_path):
    L = LANGS[lang]
    links = "\n          ".join(f'<a href="{h}">{e(t)}</a>' for t, h in L["nav"])
    return f"""<body>

  <header>
    <div class="container">
      <nav>
        {SOCIAL}<a href="{L['prefix'] or ''}/" class="logo">Manuel Padrão</a>

        <div class="nav-links">
          {links}
          <a href="{alt_path}" class="lang" hreflang="{L['other']}" lang="{L['other']}">{L['other_label']}</a>
        </div>
      </nav>
    </div>
  </header>
"""


def footer_html():
    return f"""
  <footer>
    <div class="container footer-content">
      <div>© <span id="year"></span> Manuel Padrão</div>
      <div>
        Founder & CEO ·
        <a href="{COZE}" target="_blank" rel="noopener">Cozecare</a>
      </div>
    </div>
  </footer>

  <script>
    document.getElementById("year").textContent = new Date().getFullYear();
  </script>

</body>
</html>
"""


def list_html(lang):
    L = LANGS[lang]
    items = []
    for a in ARTICLES:
        t = a[lang]
        items.append(f"""            <a href="{url_of(lang, a)}" class="insight-item">{e(t['title'])}</a>""")
    return "\n".join(items)


def index_page(lang):
    L = LANGS[lang]
    path = url_of(lang)
    alt_path = url_of(L["other"])
    title = f"Insights — Manuel Padrão"
    ld = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Insights",
    "url": "{SITE}{path}",
    "inLanguage": "{L['html']}",
    "author": {{ "@id": "{SITE}/#person" }}
  }}
  </script>"""
    return (
        head(lang, title, L["idx_desc"], path, alt_path, ld=ld)
        + header_html(lang, alt_path)
        + f"""
  <main>
    <section class="page-top">
      <div class="container">
        <a href="{L['prefix'] or ''}/" class="back" id="back">{L['back']}</a>
        <h1 class="page-title">Insights</h1>
        <div class="insight-list">
{list_html(lang)}
        </div>
      </div>
    </section>
  </main>
"""
        + footer_html().replace("</body>", BACK_JS + "</body>")
    )


def article_page(lang, a):
    L = LANGS[lang]
    t = a[lang]
    path = url_of(lang, a)
    alt_path = url_of(L["other"], a)
    img = image_url(a)
    iso = a["date"].isoformat()
    title = f"{t['title']} — Manuel Padrão"
    ld = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {json.dumps(t['title'], ensure_ascii=False)},
    "description": {json.dumps(t['desc'], ensure_ascii=False)},
    "datePublished": "{iso}",
    "dateModified": "{iso}",
    "inLanguage": "{L['html']}",
    "mainEntityOfPage": "{SITE}{path}",
    "image": "{SITE}{img or '/assets/manuel-padrao.jpg'}",
    "author": {{ "@id": "{SITE}/#person" }},
    "publisher": {{ "@id": "{COZE}#organization" }},
    "about": {{ "@id": "{COZE}#organization" }}
  }}
  </script>"""
    linkedin = (
        f'<a href="{ACTIVITY}{a["activity"]}/" target="_blank" rel="noopener" class="text-link">{L["linkedin"]}</a>'
        if a["activity"] else ""
    )
    figure = (
        f'\n        <img class="article-image" src="{img}" alt="{e(t["title"])}" />' if img else ""
    )
    return (
        head(lang, title, t["desc"], path, alt_path, og_type="article", image=img, ld=ld)
        + header_html(lang, alt_path)
        + f"""
  <main>
    <article class="page-top">
      <div class="container article">
        <a href="{url_of(lang)}" class="back" id="back">{L['back']}</a>

        <time class="article-date" datetime="{iso}">{e(fmt_date(lang, a['date']))}</time>
        <h1 class="article-title">{e(t['title'])}</h1>{figure}

        <div class="article-body">
          {body_html(t['body'])}
        </div>

        <div class="article-links">
          <a href="{COZE}" target="_blank" rel="noopener" class="text-link">{L['discover']}</a>
          {linkedin}
        </div>
      </div>
    </article>
  </main>
"""
        + footer_html().replace("</body>", BACK_JS + "</body>")
    )


def inject_home(rel, lang):
    path = os.path.join(ROOT, *rel.split("/"))
    with open(path, encoding="utf-8") as f:
        s = f.read()
    new = f"<!--INSIGHTS-->\n{list_html(lang)}\n            <!--/INSIGHTS-->"
    s = re.sub(r"<!--INSIGHTS-->.*?<!--/INSIGHTS-->", lambda _: new, s, flags=re.S)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def sitemap():
    urls = [("/", "/pt/"), ("/pt/", "/"), ("/insights/", "/pt/insights/"), ("/pt/insights/", "/insights/")]
    entries = []
    for a in ARTICLES:
        entries.append((url_of("en", a), url_of("pt", a), a["date"]))
        entries.append((url_of("pt", a), url_of("en", a), a["date"]))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for loc, alt, *d in [(u, o, None) for u, o in urls] + entries:
        lm = d[0] if d and d[0] else None
        en, pt = (loc, alt) if not loc.startswith("/pt") else (alt, loc)
        out.append("  <url>")
        out.append(f"    <loc>{SITE}{loc}</loc>")
        if lm:
            out.append(f"    <lastmod>{lm.isoformat()}</lastmod>")
        out.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}" />')
        out.append(f'    <xhtml:link rel="alternate" hreflang="pt" href="{SITE}{pt}" />')
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    for lang in LANGS:
        write(url_of(lang).strip("/") + "/index.html", index_page(lang))
        for a in ARTICLES:
            write(url_of(lang, a).strip("/") + "/index.html", article_page(lang, a))
    inject_home("index.html", "en")
    inject_home("pt/index.html", "pt")
    write("sitemap.xml", sitemap())
    print("ok")


if __name__ == "__main__":
    main()
