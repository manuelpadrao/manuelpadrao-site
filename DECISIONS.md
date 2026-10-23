# Decisões do projeto

Registo das escolhas do Manuel. Atualizar sempre que algo mudar.

## Regras gerais
- Dúvidas: perguntar sempre com perguntas de seleção múltipla.
- UI: não mudar o estilo existente. Clean, simples, premium, nada "AI".
- Texto: pouco. Sem subtítulos descritivos.

## Escolhas
| Tema | Decisão |
|---|---|
| Língua | Bilingue: EN (`/`) e PT (`/pt/`), com hreflang |
| Foto | Hero, ao lado do nome (`assets/manuel-padrao.jpg`) |
| Domínio | manuelpadrao.com |
| Backlinks | Links contextuais com anchor variado para cozecare.com, sem nofollow |

| Foto hero | Retrato completo, sem cortes, altura limitada ao ecrã (sem scroll no hero) |
| Blog | Secção "Insights" (`/insights/`, `/pt/insights/`), um artigo por post do LinkedIn, EN + PT |
| Texto dos artigos | Reescrito em nome do Manuel, curto, a partir dos resumos dos posts |
| Fotos dos artigos | O Manuel envia pelo chat; guardar em `assets/insights/<id>.jpg` e correr o build |

## Como editar os artigos
- Conteúdo em `scripts/build.py` (lista ARTICLES). Depois: `python scripts/build.py`.
- O script gera os artigos, as listas das homes e o sitemap. Não editar esses ficheiros à mão.
- Só falta o artigo 300-psychologists (texto e foto originais por enviar; o texto atual é resumido).

## Dados
- LinkedIn: https://www.linkedin.com/in/manuelpadrao
- Cozecare: https://cozecare.com/
- Email: manuel@cozecare.com

## SEO / backlinks
- Todos os links para cozecare.com são dofollow (sem `rel="nofollow"`), com `rel="noopener"`.
- Anchors variados: Cozecare, mental health platform, employee mental health solution.
- Schema.org: ProfilePage + Person + Organization (founder / worksFor / sameAs).
- Evitar spam: poucos links, em contexto, sem repetir o mesmo anchor em excesso.
- Pendente: link de volta da cozecare.com (página About/Team) para manuelpadrao.com.
- Pendente: links para páginas internas da Cozecare (precisa dos URLs reais).

## Pendente
- Secção Press removida (tinha placeholders). Voltar a adicionar quando houver links reais.
- Publicar o site em manuelpadrao.com e submeter o sitemap no Google Search Console.
