# Instagram @ufpel_uergs.cetmob: guia editorial e de produção

Perfil oficial do Curso de Engenharia de Transporte e Mobilidade (CETMob), oferecido em conjunto pela UERGS e pela UFPel. Este repositório é público e guarda as mídias publicadas (o Instagram só aceita link público), os modelos de produção e este guia.

## Cadência e formato

| Dia | Pauta | Semana ISO par | Semana ISO ímpar |
|---|---|---|---|
| Segunda | **Local**: Região Metropolitana de Porto Alegre (RMPA) | Carrossel | Reel |
| Quinta | **Internacional: novidade tecnológica** em mobilidade urbana nos grandes centros do mundo | Reel | Carrossel |

Para saber a semana, use `date +%V` no fuso America/Sao_Paulo. Exemplo: a semana 48 de 2026 teve carrossel local e Reel internacional.

**Nenhuma publicação acontece sem o "aprovado" explícito do coordenador (Fábio).**

## Escolha da pauta

- Fato **recente**, dos últimos 7 a 10 dias de preferência, ou um marco iminente: licitação, inauguração, resultado divulgado.
- Mobilidade urbana em sentido amplo: transporte coletivo, trilhos, tarifação, segurança viária, mobilidade ativa, logística urbana, eletrificação, ITS, acessibilidade.
- Prefira pautas que rendam uma **lição de engenharia** concreta.
- **Pauta internacional = sempre novidade tecnológica**: veículos autônomos, sensores e ITS, IA aplicada a semáforos e operação, bilhetagem e pagamentos, eletrificação e recarga, novos materiais, automação ferroviária, dados em tempo real, gêmeos digitais, drones e logística urbana. Notícias só de obra, política tarifária ou cronograma não servem, a menos que o foco seja a tecnologia. Explique **como a tecnologia funciona** (componentes, números) e qual é o estágio dela (piloto, teste com passageiros, operação comercial).
- Não repita assunto já publicado: consulte o `LOG.md`.
- Evite polêmica partidária. Atribua declarações a quem as fez e não emita opinião sobre políticos.

## Apuração (obrigatório)

- Cada número, data e nome deve vir de fonte oficial (governo, operador, órgão) ou de **2 veículos** independentes. Leia a página e não confie só no snippet da busca.
- Se as fontes divergirem, use a informação mais recente e deixe claro o que ainda não está definido ("sem data oficial").
- Datas sempre com dia e mês no conteúdo ("até 23/11").
- Conexão com o curso: cite **somente** componentes curriculares que existem no PPC do CETMob. Exemplos verificados: Sistemas Inteligentes de Transporte 1 e 2; Programação voltada à Mobilidade; Transporte Público de Passageiros; Introdução ao Controle e Automação; Infraestrutura e Operação de Transportes 1 e 2; Engenharia de Tráfego; Segurança Viária; Planejamento de Transportes; Mobilidade Urbana e Sustentável; Mobilidade Ativa; Logística 1 e 2.

## Identidade visual

- Cores: azul-marinho `#2c2793` (fundo escuro), azul `#3488c1`, laranja `#fc8b3f` (destaques), papel `#f6f5fb` (fundo claro), texto `#1b1849`.
- Fonte: Roboto (`/usr/share/fonts/truetype/google-fonts/ofl/roboto/`).
- Logos em `tools/assets/`: versão BRANCO em fundo escuro, COLORIDO em fundo claro.
- Assinatura: as 3 barras verticais da marca no canto superior direito.
- **Somente arte original**: tipografia, diagramas e ícones desenhados. Nada de fotos de matérias nem de terceiros, e nada de pessoas reais.

### Carrossel
- 1080×1350 (4:5), 5 slides, JPEG qualidade 92.
- Estrutura: capa escura com gancho em pergunta e 1 ou 2 datas-chave; 2 ou 3 slides claros com números, explicação técnica e "olhar de engenharia" ligado ao PPC; slide final escuro com linha do tempo ou próximos passos, chamada para comentário e fontes.
- Modelo: `tools/carrossel/exemplo_post01.py <pasta_saida>`.

### Reel
- 1080×1920, 30 fps, 25 a 35 s, H.264 com trilha AAC silenciosa (sem música).
- Texto dentro da área segura: y entre 250 e 1550 px, margens de 90 px.
- Estrutura: gancho (cerca de 4 s), 3 a 4 cenas de explicação, "lição de engenharia" com disciplinas do PPC e assinatura com o @.
- Modelo: `tools/reel/exemplo_reel01.html`, com cenas em `render(id, t)`. Renderize com `tools/reel/render.py`, que grava um MP4 por cena, junta com concat e gera a capa.
- Antes de renderizar, confira quadros estáticos de cada cena no tamanho real.

## Legenda

- Primeira linha: o gancho. Depois, 2 ou 3 parágrafos curtos com os fatos, a explicação técnica, a lição de engenharia e uma pergunta para comentários.
- Linha de "Fontes:" com o nome do veículo e a data.
- De 8 a 12 hashtags, sempre com #MobilidadeUrbana #EngenhariaDeTransporte #CETMob #UFPel #UERGS.
- Máximo de 2.200 caracteres.

## Publicação (técnico)

1. Mídia em `AAAA-MM/postNN/` (carrossel) ou `AAAA-MM/reelNN/` (Reel), com `legenda.txt`. Numeração sequencial global: veja o `LOG.md`.
2. Antes da aprovação: enviar ao Fábio a prévia (imagens ou vídeo, capa e legenda) e **aguardar "aprovado"**.
3. Depois da aprovação: `git push` para `main` do repositório `cetmob-midia/cetmob-midia`. Confirmar com curl que cada `https://raw.githubusercontent.com/cetmob-midia/cetmob-midia/main/<caminho>` responde HTTP 200 com o tipo de conteúdo correto.
4. Publicar pelo conector Windsor.ai for Social Media: `connector=instagram`, `account=17841471698455486`.
   - Carrossel: `create_carousel_post`, com `items` (image_url + alt_text) e `caption`.
   - Reel: `create_video_post`, com `video_url`, `cover_url`, `caption` e `share_to_feed=true`.
5. Registrar no `LOG.md` a data, o tipo, a pauta e o media id, e fazer o push.
