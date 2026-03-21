# Pitch Negócios Sentivis

## 1. Propósito deste documento
Este documento consolida, de forma coerente e completa, o pitch de negócios da Sentivis Agro com base no texto aprovado ao longo do estudo e na lousa de trabalho do projeto. Seu objetivo é servir como base para apresentação da Sentivis a investidores diretos, sponsors, parceiros potenciais e articuladores que possam encaminhar a solução a públicos estratégicos.

Este material não é campanha de marca, peça promocional ou proposta jurídica final. Ele é uma apresentação estratégica da fase atual da Sentivis, com foco em contexto, proposta, validação, operação, evidência e necessidade de viabilização.

---

## 2. O que é a Sentivis
A Sentivis é uma agtech de inteligência de campo voltada ao monitoramento agroambiental, à organização de dados da fazenda e ao apoio à decisão no contexto rural. Seu foco inicial está nos cafés especiais, sem limitar a possibilidade de adaptação futura para outras culturas de maior valor agregado.

A proposta central da Sentivis não é vender sensores isolados, nem substituir a experiência de quem conhece a fazenda. A Sentivis existe para organizar melhor a leitura da operação rural, conectar sinais do campo a dados confiáveis e apoiar decisões com mais evidência diante do clima, do manejo, da qualidade, da rastreabilidade e do mercado.

Em sua essência, a Sentivis deve ser lida como uma plataforma operacional de dados e inteligência aplicada ao campo.

---

## 3. O problema que a Sentivis enfrenta
No café, o problema não está apenas no clima. O problema está na decisão tomada sob incerteza.

O produtor precisa decidir ao mesmo tempo sobre:
- clima e microclima da própria fazenda;
- irrigação e resposta hídrica do solo;
- adubação e manejo por talhão;
- qualidade, consistência e rastreabilidade;
- custos, timing e leitura de mercado.

Grande parte dessa leitura ainda é fragmentada, macro e pouco aderente à realidade específica de cada fazenda. Há referências amplas disponíveis, mas o que falta é leitura integrada, local, histórica e utilizável para apoiar decisão com mais clareza.

A dor principal do cafeicultor, portanto, não é apenas climática nem apenas técnica. Ela é a incerteza entre o que acontece no talhão, o que o mercado está pagando e a decisão que precisa ser tomada no momento certo.

---

## 4. Por que esse modelo faz sentido
O uso de sensores, conectividade rural, análise de dados e inteligência artificial no agro já deixou de ser hipótese. O que a Sentivis busca agora não é provar que essa direção tecnológica existe, mas validar com método o seu próprio modelo em contexto real de fazenda.

Esse caminho faz sentido porque:
- IoT, conectividade de longo alcance e análise de dados já são tecnologias reconhecidas no agro;
- o café premium exige rastreabilidade, qualidade, leitura local e preparação para mercados mais exigentes;
- produtores e organizações do setor precisam de dados mais organizados, comparáveis e utilizáveis;
- a pressão por eficiência hídrica, energética, documental e operacional tende a crescer.

A diferença da Sentivis está em não se limitar à medição. A proposta é organizar a leitura da fazenda, estruturar evidência e apoiar decisão com base em dados locais e referências confiáveis.

---

## 5. O que a Sentivis faz
A Sentivis organiza a leitura da fazenda para apoiar decisões mais seguras.

Na prática, a solução:
- coleta o que acontece no campo;
- organiza dados, histórico e rastreabilidade;
- ajuda a interpretar sinais do clima, do solo e da operação;
- apoia a decisão sem substituir a experiência do produtor;
- cria uma base mais consistente para manejo, documentação, validação e evolução futura da gestão.

O valor da Sentivis não está em dashboards isolados. Está na capacidade de transformar sinais dispersos em informação utilizável, estruturada e rastreável.

---

## 6. Como a solução funciona
A Sentivis combina coleta local, organização centralizada dos dados, acompanhamento da operação e validação contínua do uso em campo.

### 6.1 No campo
Sensores, pontos de leitura e estruturas de coleta acompanham o que acontece na fazenda em tempo real e ao longo do tempo.

### 6.2 No núcleo local
A operação se organiza em torno de um núcleo local centralizado na fazenda, concebido como Edge. Esse Edge recebe, organiza e prepara os dados vindos do campo. A nuvem complementa, consolida e amplia o processamento, mas a operação nasce no núcleo local.

A base operacional definida para esse núcleo local considera Raspberry Pi 4/5 como referência principal, com redundância e backup por mini computadores quando necessário.

### 6.3 Na nuvem
Os dados seguem para a camada Sentivis Cloud, onde são consolidados, comparados e preparados para visualização, histórico e análises complementares.

### 6.4 No acompanhamento
A operação inclui manutenção, visitas programadas, rotina de verificação e escuta da percepção do fazendeiro.

### 6.5 Na validação
Cada etapa pode ser registrada e evidenciada, transformando a execução do piloto em trilha rastreável de operação e aprendizado.

---

## 7. Diferenciais operacionais da arquitetura
Alguns pontos estruturais já definidos são centrais para o modelo:

### 7.1 Edge como centro local
O Edge deixou de ser hipótese. Ele é peça central da arquitetura operacional da Sentivis, funcionando como continuação lógica do sistema, recebendo e organizando dados do campo.

### 7.2 QR codes distribuídos no talhão
Os QR codes fazem parte do fluxo operacional. Eles servem para:
- identificação exata do ponto;
- vínculo entre imagem, talhão e histórico;
- rastreabilidade visual ao longo do tempo;
- padronização da coleta feita pelos funcionários da fazenda.

### 7.3 Captura de imagens e histórico visual
Os funcionários podem usar os celulares da fazenda para registrar pontos do talhão por meio dos QR codes. Essas imagens entram no fluxo Sentivis, são vinculadas ao contexto do ponto e seguem para o Edge e depois para a Sentivis Cloud, com remoção local após sincronização.

Além disso, a arquitetura prevê câmera voltada para planta modelo na estação, permitindo histórico contínuo de referência.

### 7.4 Reuso do método
A mesma lógica de evidência, rastreabilidade e validação usada para acompanhar manutenção, visitas e coleta de percepção também pode servir, no futuro, como base para observabilidade fase a fase da produção.

---

## 8. O que já existe hoje
A Sentivis não está começando do zero.

Já existe:
- base tecnológica estruturada;
- lógica operacional definida;
- arquitetura de campo e de centralização desenhada;
- etapa inicial de monitoramento e observação de dados;
- preparação clara para a próxima fase de validação.

O passo seguinte não é inventar a solução. É validar com mais profundidade, disciplina e evidência o modelo em campo.

---

## 9. Base atual de dados e calibração
A Sentivis já conta com uma etapa inicial de monitoramento e análise de dados usada para amadurecer a plataforma, ajustar a lógica de leitura e preparar a próxima fase de validação com mais consistência.

Essa base já permitiu:
- calibrar a plataforma;
- refinar a lógica da IA;
- identificar dados prioritários;
- ajustar respostas e inferências;
- estruturar base comparável e rastreável.

Essa etapa não substitui a validação ampliada do próximo ciclo, mas oferece base concreta para seguir com mais método.

---

## 10. Próxima fase de validação
O próximo passo é validar com profundidade, disciplina e evidência.

A próxima fase foi desenhada para ampliar a validação da solução em campo, com operação acompanhada, rotina estruturada e rastreabilidade da execução ao longo de um ciclo completo.

### Estrutura da fase
- até 10 unidades em contexto real de fazenda;
- horizonte de 12 meses;
- base geográfica inicial já definida;
- fazendas já predispostas a participar da etapa;
- possibilidade de composição dentro do limite operacional planejado.

### Objetivo da fase
- validar o modelo da Sentivis com mais profundidade;
- consolidar evidências técnicas, operacionais e de aderência;
- observar comportamento da operação e percepção real do uso;
- transformar execução, aprendizado e evidência em base concreta para a próxima etapa.

---

## 11. Modelo operacional do piloto
A validação não será conduzida como teste solto. Ela será conduzida como operação real.

### 11.1 Frente operacional técnica
Haverá uma pessoa principal responsável pela operação técnica:
- manutenção dos equipamentos;
- verificação dos equipamentos em campo;
- verificação dos equipamentos na sede da fazenda;
- checagem de funcionamento;
- registro do estado técnico da operação.

No início, a rotina operacional prevista é quinzenal por unidade, com agenda pré-definida e possibilidade de ajuste conforme necessidade de campo.

### 11.2 Frente de feedback e percepção
Uma segunda pessoa será responsável pela coleta estruturada de percepção do fazendeiro:
- contato recorrente;
- leitura de valor percebido;
- registro de ruídos, dificuldades e melhorias;
- manutenção de vínculo humano de confiança.

A coleta de percepção deve acontecer mensalmente em todas as 10 unidades, prioritariamente por ligação direta e pesquisa simples via WhatsApp. Visitas presenciais de feedback terão prioridade para unidades com problema, ruído de percepção ou necessidade específica.

### 11.3 Instrumento simplificado de feedback
A lógica de feedback deve ser simples, acessível e aderente à rotina do produtor, com perguntas curtas sobre:
- percepção geral do produto;
- utilidade percebida;
- propensão a recomendar.

### 11.4 Princípio central
A validação da Sentivis depende de duas coisas distintas:
- o estado técnico da operação;
- a percepção real do fazendeiro.

Essa separação é parte central da seriedade do modelo.

---

## 12. Evidência e rastreabilidade da execução
Cada etapa da validação precisa deixar evidência.

A Sentivis foi pensada para que a execução do piloto não dependa apenas de relato. Visitas, manutenções, entrevistas, coletas e verificações podem ser registradas de forma estruturada, criando uma trilha rastreável da operação.

### Elementos centrais
- painel de realizações;
- registros de campo;
- identificação da unidade e do local atendido;
- vínculo entre visita, coleta e evidência;
- histórico operacional organizado.

### Finalidade
Esse painel deve permitir acompanhamento por parceiros autorizados, demonstrando:
- o que foi feito;
- onde foi feito;
- quando foi feito;
- que dados foram coletados;
- que pendências ou correções surgiram.

O objetivo não é apenas comprovar presença. É transformar cada etapa da execução em evidência rastreável da operação.

---

## 13. Leitura de valor por público

### 13.1 Para o cafeicultor
A Sentivis apoia decisões com mais evidência, ajuda a organizar a leitura da fazenda e contribui para uma visão mais clara diante do clima, do manejo e do mercado.

O primeiro valor percebido não deve ser comunicado como substituição da experiência do produtor nem como promessa de controle total. A formulação correta é a de apoio: a Sentivis ajuda o cafeicultor a agir com mais evidência, com informação correta para decisão na hora certa.

### 13.2 Para a cooperativa
A Sentivis pode apoiar a qualificação coletiva da base produtiva, fortalecer rastreabilidade, organizar documentação e preparar melhor os cooperados para mercados mais exigentes.

A cooperativa não entra por “mais uma inovação”. Ela entra pela possibilidade de elevar padrão, documentação e inteligência coletiva da produção, respeitando a autonomia do produtor e os limites de governança sobre dados.

### 13.3 Para o investidor direto
A Sentivis se apresenta como uma operação séria, rastreável e acompanhada, com validação estruturada em campo e potencial de evolução comercial após o primeiro ciclo corretamente executado.

Para esse público, os sinais principais de maturidade são:
1. operação disciplinada;
2. rastreabilidade da execução;
3. proximidade real com o usuário;
4. tecnologia validável em campo.

O investidor deve enxergar primeiro método, controle e evidência, antes da camada tecnológica propriamente dita.

---

## 14. O que está sendo buscado agora
A fase atual exige viabilização para validar o modelo do jeito certo.

O foco desta etapa não é ampliar discurso nem antecipar escala. É garantir as condições necessárias para executar, acompanhar e comprovar a próxima fase da Sentivis com disciplina, método e rastreabilidade.

### O que se busca agora
- viabilização da operação do piloto ampliado;
- sustentação da infraestrutura, manutenção, deslocamento e rotina de campo;
- suporte à validação com profundidade suficiente para gerar evidência útil;
- capital para transformar base tecnológica funcional em operação validada e comercialmente legível.

### Público prioritário nesta fase
O principal público para viabilizar essa etapa é o investidor direto.

Cooperativas, fornecedores e entidades setoriais podem se beneficiar futuramente dos desdobramentos da solução, mas não devem sustentar o discurso principal do piloto neste momento.

---

## 15. Pitch financeiro do piloto
O piloto da Sentivis foi consolidado, em leitura financeira macro, para 10 unidades ao longo de 12 meses.

### Resumo executivo financeiro
- CAPEX inicial estimado: **R$ 69.100**
- OPEX mensal estimado: **R$ 10.863**
- OPEX anual estimado: **R$ 130.352**
- Valor-base do piloto (12 meses): **R$ 199.452**
- Faixa recomendada de apresentação: **R$ 220 mil a R$ 230 mil**

### Leitura executiva correta
O capital buscado nesta fase não é para financiar escala ampla nem estrutura fabril completa. O objetivo é:
- colocar o piloto em pé;
- sustentar 12 meses de operação e validação;
- garantir conectividade, Edge, sensores, estações, deslocamento, manutenção e formalização mínima;
- gerar evidência disciplinada da execução.

### Arquitetura financeira por módulos
O desenho financeiro do piloto considera:
- produção eletrônica aplicada;
- estações meteorológicas principais;
- sensores distribuídos e HiGrow;
- Edge com redundância por fazenda;
- operação digital com infraestrutura, banco, armazenamento e IA;
- operação de campo, manutenção e deslocamento;
- jurídico, formalização e contingência.

### Contrapartida interna dos sócios
Os valores consolidados não incluem como demanda principal de capital externo alguns itens já absorvidos internamente pelos sócios, como espaço fabril disponível, parte da infraestrutura física já existente e parte da capacidade própria de preparação do lote.

### Aviso metodológico
Os valores possuem caráter estimativo e macroeconômico. Eles não representam orçamento executivo final, mas referência estruturada para dimensionamento do capital necessário ao primeiro ciclo do projeto.

---

## 16. Limites, seriedade e leitura correta do material
A Sentivis se apresenta com base real, método operacional e validação estruturada. Ao mesmo tempo, reconhece os limites do estágio atual da solução e evita transformar potencial em promessa.

### O que a Sentivis já sustenta
- base tecnológica estruturada;
- lógica operacional definida;
- etapa inicial de monitoramento;
- plano claro de validação ampliada;
- método de rastreabilidade da execução;
- proximidade real com o usuário final.

### O que a Sentivis não promete agora
A Sentivis não deve prometer:
- retorno garantido;
- produtividade assegurada;
- qualidade premium garantida;
- certificação automática;
- escala já comprovada;
- maturidade comercial plena antes da validação do primeiro ciclo;
- acurácia absoluta;
- controle total do talhão ou da cadeia.

### Como este material deve ser lido
Como documento institucional e estratégico da fase atual da solução, com foco em:
- contexto;
- problema real;
- método;
- operação;
- evidência;
- necessidade de viabilização.

---

## 17. Status institucional
A marca **Sentivis** possui pedido formal depositado junto ao INPI, com os seguintes dados institucionais:
- número do processo: **940625911**
- protocolo: **850250460676**
- situação: **Aguardando exame de mérito**
- apresentação: **Mista**
- natureza: **Produtos e/ou Serviço**

Esse registro deve ser usado apenas como fato institucional verificável, e não como promessa de proteção total da tecnologia.

---

## 18. O que permanece como estudo futuro
Os pontos ainda não fechados e que não são indispensáveis ao entregável atual devem permanecer explicitamente abertos como estudo futuro.

Entre os principais temas que continuam fora deste pitch principal estão:
- instrumento jurídico final de investimento;
- modelo econômico definitivo de parceria;
- métricas financeiras finais de retorno por arranjo societário;
- aprofundamento comercial pós-validação;
- detalhamento completo de expansão futura;
- camadas mais avançadas de análise por imagem e automação interpretativa.

---

## 19. Síntese final
A Sentivis não pede capital para inflar promessa. Pede capital para viabilizar um ciclo real, rastreável e disciplinado de validação em campo.

A tese central é simples:
- há um problema real no campo;
- há uma base tecnológica já estruturada;
- há método operacional definido;
- há percepção clara de valor por público;
- há plano de validação ampliada;
- e há um pitch financeiro coerente para sustentar o primeiro ciclo.

O que está sendo buscado agora é viabilização séria de uma fase crítica. A expansão de discurso e de mercado só deve acontecer depois da validação do primeiro ano.

Sentivis Agro. Base real, método operacional e validação disciplinada em campo.
