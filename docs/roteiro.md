# Roteiro de Implementação — Factory Control

Documento de acompanhamento do grupo. **Consultem e atualizem este arquivo a cada sessão de trabalho**, marcando as tarefas concluídas e registrando decisões na seção "Diário de decisões".

- **Integrantes:** Arthur Antonio Guiraldelli, Luiz Eduardo Figueiredo Campos, Caio Utsch Pedra
- **Repositório:** https://github.com/Guiraldelli-A/Factory-Control-PUC
- **Template obrigatório:** https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template
- **Última atualização:** 22/11/2026 (Entrega 2 implementada)

---

## 1. Cronograma oficial (enunciado)

| Etapa | Prazo | O que entregar | Situação |
|---|---|---|---|
| Atividade individual (docstrings e testes) | 15/11/2026 | Roteiro prático individual (1 ponto) | ✅ prazo encerrado |
| **Entrega 1** — Proposta | dom 15/11/2026 | `docs/proposta.md` preenchido | ✅ entregue |
| **Entrega 2** — Versão parcial executável | dom 22/11/2026 | Jogo rodando para acompanhamento em aula | ✅ jogo pronto — falta enviar o ZIP |
| **Entrega 3** — Versão final | dom 29/11/2026 | Jogo completo + documentação + testes | ⬜ |
| Apresentação | semana de 30/11/2026 | Demonstração em sala | ⬜ |

Todas as entregas são feitas pelo **Canvas**, enviando o **ZIP do repositório do GitHub**.

---

## 2. O que cada entrega exige

### Entrega 2 — Versão parcial executável (22/11)
O enunciado pede:
- [x] Janela do Pygame abrindo.
- [x] Loop principal funcionando.
- [x] Controles básicos (mouse).
- [x] Pelo menos **uma interação ou desafio funcional**.
- [x] Organização inicial em funções.
- [x] **Algum elemento concreto da mecânica temática** (no nosso caso: a recomendação da IA com Aceitar/Rejeitar).
- [x] Atualizar a proposta se o planejamento tiver mudado (seções 15 e 16 de `docs/proposta.md`).

> Não é necessário que todas as regras, telas ou melhorias estejam prontas nesta etapa.

### Entrega 3 — Versão final (29/11)
- [ ] Jogo completo e executável.
- [ ] Regras principais implementadas.
- [ ] Condição de encerramento (vitória e derrota).
- [ ] Indicador de desempenho (produtos, tempo, recursos, pontuação).
- [ ] Integração temática verificável **na jogabilidade** (não só em texto/imagem).
- [ ] Código organizado (funções e módulos).
- [ ] Arquivos auxiliares (ex.: `data/recorde.txt` ou `data/ranking.txt`).
- [ ] `README.md` atualizado.
- [ ] `docs/proposta.md` atualizado.
- [ ] Testes simples de funções de lógica (`pytest`).
- [ ] Recursos externos referenciados no README (origem e licença).

### Requisitos mínimos do jogo (seção 4 do enunciado) × Factory Control

| Requisito | Como o Factory Control atende |
|---|---|
| Tela principal de jogo | Tela da fábrica com 3 máquinas e painel lateral |
| Controle de um elemento principal | O jogador controla as máquinas (ligar/desligar/manutenção) |
| Mecânica central clara | Gerenciar a produção até atingir a meta |
| Pontuação/vidas/tempo/progresso | Produtos (x/10), recursos, cronômetro, pontuação de decisões |
| Vitória/derrota/encerramento | Vitória: 10 produtos. Derrota: tempo ou recursos esgotados |
| Interação com elementos | Cliques nas máquinas e nos botões da recomendação |
| Informações na tela | Painel com recursos, produtos, tempo, status das máquinas |
| Código em funções | Regras em `src/funcoes.py`, loop em `src/jogo.py` |
| Estruturas de dados | Lista de dicionários (máquinas), dicionário (estado do jogo), listas (recomendações) |
| Leitura/escrita de arquivo | Recorde/ranking em `data/` |
| README.md | Atualizar com regras, controles e como executar |
| docs/proposta.md | Já preenchido (atualizar se mudar) |
| Testes | `tests/test_logica.py` com pytest |

---

## 3. Especificação do jogo (versão de referência)

> Valores **já implementados e balanceados por simulação** (22/11). Ficam centralizados em `src/config.py`.
>
> Resultado de 400 partidas simuladas por estratégia: revisar máquinas desgastadas + responder certo à IA → **94% de vitórias**; aceitar tudo que a IA diz → 71%; só consertar quando quebra → 34%; não fazer nada → 14%. Ou seja, a estratégia vencedora é exatamente a mensagem do tema.

### Elementos
- **3 máquinas**, cada uma representada por um dicionário:
  ```python
  {"nome": "Máquina 1", "ligada": False, "quebrada": False,
   "desgaste": 0, "progresso": 0.0, "em_manutencao": 0.0}
  ```
- **Estado da partida** (dicionário): recursos, produtos, tempo restante, pontuação, recomendação atual.

### Regras
| Regra | Valor inicial |
|---|---|
| Recursos iniciais | 100 |
| Tempo da partida | 90 s |
| Meta | 10 produtos |
| Tempo para produzir 1 produto (por máquina ligada) | 12 s |
| Custo de cada produto | 6 recursos |
| Desgaste | Sobe 2%/s enquanto a máquina está ligada (0 a 100) |
| Chance de falha | Zero até 40% de desgaste; depois cresce até 15%/s em 100%. A falha perde o produto em andamento |
| Revisão preventiva | 8 recursos, 3 s, zera o desgaste (a máquina volta ligada) |
| Conserto (máquina quebrada) | 15 recursos, 3 s, zera o desgaste (a máquina volta ligada) |

### IA de recomendações (integração com o tema)
- A cada ~10 s (primeira aos 4 s), o "Assistente IA" sugere uma ação, sempre mostrando "confiança" de 85–98%. Exemplos:
  - "Faça manutenção na Máquina 2" · "Ligue a Máquina 3" · "Desligue a Máquina 1"
- Cerca de **30% das sugestões são inadequadas** (ex.: manutenção em máquina com desgaste baixo, ligar máquina quebrada, desligar a única máquina produzindo).
- O jogador clica em **Aceitar** ou **Rejeitar**; se não responder em ~8 s, a sugestão expira.
- Cada decisão é avaliada: aceitar sugestão boa ou rejeitar sugestão ruim = **+1 decisão correta**; o contrário = decisão errada. Ao aceitar uma sugestão ruim, o efeito negativo acontece de verdade (gasta recursos, para produção etc.).
- Mensagem educativa: **a IA ajuda, mas a supervisão humana é necessária**.

### Fim de partida
- **Vitória:** 10 produtos dentro do tempo.
- **Derrota:** tempo acabou, ou recursos insuficientes para produzir/fazer manutenção.
- Tela final mostra: resultado, produtos, recursos restantes, decisões corretas/erradas, pontuação e recorde.
- **R** reinicia · **ESC** sai.

### Pontuação (implementada)
`pontuação = produtos × 100 + decisões corretas × 50 − decisões erradas × 30`; na vitória soma também `recursos restantes + 2 × segundos restantes`. Nunca fica negativa. O recorde fica em `data/recorde.txt`.

---

## 4. Organização do código (a partir do template)

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada (mantido do template) |
| `src/config.py` | Tela, cores, fontes, constantes de regra (recursos, tempos, custos) |
| `src/funcoes.py` | **Lógica pura e testável**: criar máquinas, produzir, consumir recursos, desgaste, falha, manutenção, gerar/avaliar recomendação, verificar vitória/derrota, calcular pontuação |
| `src/interface.py` | Desenho na tela: máquinas, painel, botões, recomendação, telas de início/fim (✅ criado) |
| `src/jogo.py` | Loop principal: eventos, atualização, desenho, troca de telas |
| `src/dados.py` | Recorde/ranking em arquivo (já existe no template) |
| `src/sprites.py` | Carregar imagens (do template; usar se tivermos sprites) |
| `tests/test_logica.py` | Testes pytest das funções de `src/funcoes.py` |

Regra de ouro: **`funcoes.py` não desenha nada e não depende do Pygame**, assim tudo nele pode ser testado com pytest.

> As funções de exemplo do template (`calcular_pontos`, `limitar_valor` etc.) podem ser mantidas se forem usadas, ou substituídas pelas nossas. Os testes antigos devem acompanhar essa decisão.

---

## 5. Plano dia a dia

### ✅ Domingo 22/11 — Entrega 2
- [x] Configurar ambiente (Python 3.12 + pygame + pytest instalados no PC do Arthur).
- [x] `config.py` com constantes do Factory Control.
- [x] Lista de máquinas + funções de produção, recursos, desgaste, falha e manutenção.
- [x] 3 máquinas desenhadas (cor por estado, lâmpada piscando, produto andando na esteira, barras de produção e desgaste) e painel de informações.
- [x] Cliques: ligar/desligar, revisar/consertar.
- [x] Cronômetro e contador de produtos.
- [x] Recomendações da IA (Aceitar/Rejeitar, tempo para responder, feedback explicando o acerto/erro).
- [x] Vitória/derrota, tela inicial, tela final, pontuação e recorde em arquivo.
- [x] 37 testes com pytest passando.
- [x] Código revisado para usar só conteúdos da disciplina (sem lambda, enumerate, any, math, os.path etc.) e sem comentários.
- [x] README e proposta atualizados.
- [ ] Commit e push pelo VS Code (Arthur).
- [ ] **Baixar o ZIP no GitHub (Code → Download ZIP) e enviar no Canvas.**
- [ ] Cada integrante clonar, rodar `pip install -r requirements.txt` e `python main.py` e jogar algumas partidas.

### Segunda 23/11 — testes e decisão
- [ ] Jogar várias partidas (cada integrante) e anotar problemas de balanceamento — humanos jogam pior que a simulação, talvez seja preciso aliviar (`src/config.py`).
- [ ] Registrar o feedback do professor na aula (seção 9).
- [ ] Escolher os sprites (sugestão: pacotes gratuitos do Kenney.nl, licença CC0) e anotar origem/licença.

### Entrega 3 — "Tycoon leve" (24/11 a 27/11)
Ideia aprovada pelo grupo: manter tudo o que já funciona e acrescentar a sensação de jogo tycoon, sem colocação livre de máquinas, esteiras montadas pelo jogador ou inimigos (alto risco para o prazo).

**Visual (interface.py)**
- [ ] Trocar as formas geométricas por sprites (máquinas, chão da fábrica, ícones), usando `src/sprites.py` do template.
- [ ] Chão da fábrica em grade (matriz = lista de listas) com vagas para máquinas.
- [ ] Produtos andando na esteira até um caminhão/área de entrega.
- [ ] Efeitos simples: máquina piscando ao quebrar, aviso quando o tempo estiver acabando.

**Economia e loja (funcoes.py)**
- [ ] Dinheiro: vender produtos dá dinheiro; a meta passa a ser faturar um valor ou entregar N pedidos.
- [ ] Loja: comprar a 4ª e a 5ª máquina em vagas vazias.
- [ ] Melhorias: máquina mais rápida ou mais resistente ao desgaste.

**IA mais forte no tema**
- [ ] A IA passa a sugerir também investimentos, às vezes ruins (ex.: "Compre a Máquina Turbo!" sem dinheiro para manter as atuais).
- [ ] Novos tipos de sugestão errada (ex.: "acelerar máquina", que produz mais rápido mas desgasta o dobro).
- [ ] Histórico das últimas sugestões (✔/✘) na tela final.

**Opcional**
- [ ] Ranking com nome do jogador em `data/ranking.txt` (top 5).
- [ ] Sons simples (clique, produto pronto, quebra) — registrar origem/licença no README.

**Sempre**
- [ ] Testes para cada função nova em `funcoes.py`.
- [ ] Manter o código só com conteúdos da disciplina.

### Sexta 27/11
- [ ] README final: descrição, regras, controles, como executar, como testar, estrutura, créditos/licenças de assets, divisão do trabalho.
- [ ] Atualizar `docs/proposta.md` com as mudanças da Entrega 3.

### Sábado 28/11
- [ ] Teste geral do zero (clonar o repo em outra pasta e rodar).
- [ ] Correção de bugs. **Congelar funcionalidades** — a partir daqui só correções.

### 🔴 Domingo 29/11 — Entrega 3 (final)
- [ ] `python -m pytest` passando.
- [ ] Commit final + push, baixar ZIP e enviar no Canvas.

### Semana de 30/11 — Apresentação
- [ ] Ensaiar a demonstração (2–3 partidas: uma vitória, uma derrota por aceitar IA ruim).
- [ ] Cada integrante preparado para explicar sua parte e o código geral.

---

## 6. Divisão de tarefas (sugestão — ajustar entre o grupo)

| Integrante | Foco principal | Na apresentação explica |
|---|---|---|
| Arthur | Loop principal, integração e telas (`jogo.py`, `interface.py`) | Como o jogador interage e como o código foi organizado |
| Luiz Eduardo | Regras e IA de recomendações (`funcoes.py`, `config.py`) | Regras principais e a relação com o tema IA responsável |
| Caio | Testes, arquivos e documentação (`tests/`, `dados.py`, README) | Conceitos da disciplina usados, testes e uso do template |

Todos devem conseguir explicar o projeto inteiro (exigência do enunciado, seção 9).

---

## 7. Preparação da apresentação (seção 7 do enunciado)

Responder de forma curta:
1. **Proposta do jogo:** gerenciar uma fábrica com ajuda de uma IA que nem sempre acerta.
2. **Interação:** mouse nas máquinas e nos botões da recomendação; ESC sai.
3. **Regras principais:** ver seção 3.
4. **Conceitos da disciplina:** variáveis, condicionais, laços, listas, dicionários, funções, módulos, arquivos, docstrings, testes.
5. **Organização do código:** ver seção 4.
6. **Desafios encontrados:** (preencher ao longo do desenvolvimento)
7. **Uso do template:** mantivemos a estrutura de pastas, `main.py`, `dados.py`, `config.py` e a pasta de testes, adaptando ao nosso jogo.

---

## 8. Critérios de avaliação — checklist final

- [ ] Funcionamento, jogabilidade e estabilidade (sem travar/fechar com erro).
- [ ] Conceitos da disciplina aplicados.
- [ ] Código claro, organizado e modularizado.
- [ ] Três entregas cumpridas com evolução entre elas (commits frequentes ajudam a mostrar isso).
- [ ] Documentação, testes e apresentação.
- [ ] Criatividade, originalidade e integração do tema IA no Cotidiano e Uso Responsável nas mecânicas.

---

## 9. Diário de decisões e feedback

| Data | Decisão / feedback | Quem |
|---|---|---|
| 15/11/2026 | Proposta entregue: Factory Control, IA de recomendações com supervisão humana | Grupo |
| 22/11/2026 | Criado este roteiro; especificação de referência da seção 3 definida | Grupo |
| 22/11/2026 | Entrega 2 implementada. Balanceamento por simulação: tempo 120→90 s; manutenção dividida em revisão (8) e conserto (15); sem risco de falha abaixo de 40% de desgaste; falha perde o produto em andamento | Grupo |
| 22/11/2026 | Proposta renomeada para `docs/proposta.md`; adicionadas seções de atualização e declaração de originalidade | Grupo |
| 22/11/2026 | Código simplificado para usar só conteúdos da disciplina e publicado sem comentários (versão comentada para estudo fica fora do repositório) | Grupo |
| 22/11/2026 | Entrega 3: grupo escolheu o "tycoon leve" (sprites, dinheiro, loja, melhorias e IA sugerindo investimentos) | Grupo |
|  |  |  |

## 10. Pendências e dúvidas em aberto

- [ ] Confirmar se os valores de balanceamento (seção 3) estão bons com jogadores humanos.
- [ ] Decidir se usaremos sprites próprios/externos ou só formas geométricas (hoje: só formas; se externos, registrar fonte e licença no README).
- [x] Renomear `docs/proposta.MD` para `docs/proposta.md`.
- [x] Declaração de originalidade adicionada (`docs/proposta.md`, seção 16) — **o grupo deve revisar o texto**.
- [ ] O README declara o uso de assistente de IA no desenvolvimento (seção de créditos) — **o grupo deve confirmar/ajustar**, já que o enunciado exige identificar recursos externos.
- [ ] `src/sprites.py` e `assets/imagens/spritesheet.bmp` vieram do template e não são usados: decidir se usamos ou removemos.
