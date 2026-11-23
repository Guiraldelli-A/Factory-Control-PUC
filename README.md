# Factory Control

Projeto prático da disciplina de **Introdução a Algoritmos** (PUC Minas), desenvolvido em **Python e Pygame**.

**Situação do projeto:** Entrega 2 — versão parcial **executável e jogável** (22/11/2026). O jogo já tem início, partida completa, IA de recomendações, vitória/derrota, pontuação, recorde em arquivo e testes automatizados. Os próximos passos estão em [`docs/roteiro.md`](docs/roteiro.md).

## Integrantes do grupo

- Arthur Antonio Guiraldelli
- Luiz Eduardo Figueiredo Campos
- Caio Utsch Pedra

## Descrição do jogo

**Factory Control** é um jogo 2D de gerenciamento de uma pequena fábrica com três máquinas. O jogador liga e desliga as máquinas, faz manutenção e administra recursos limitados para cumprir uma meta de produção dentro do tempo.

Um **Assistente de IA** dá sugestões durante a partida, sempre com alta "confiança" — mas cerca de **30% das sugestões estão erradas**. O jogador precisa conferir o estado real das máquinas antes de aceitar ou rejeitar cada sugestão. Aceitar uma sugestão ruim tem consequências reais na partida (gasta recursos, para a produção). O objetivo é mostrar a importância da **supervisão humana e do uso responsável da IA**.

A IA é **simulada com regras** (condicionais, listas e dicionários), sem treinamento de modelos.

## Tema: IA no Cotidiano e Uso Responsável

Recorte escolhido: **confiabilidade de sistemas de recomendação na indústria**. O tema afeta diretamente as regras:

- as sugestões da IA alteram o estado da fábrica quando aceitas;
- decisões corretas (aceitar sugestão boa / rejeitar sugestão ruim) somam pontos e decisões erradas tiram pontos;
- o painel **Supervisão Humana** mostra quantos erros da IA o jogador detectou;
- a tela final reforça que sistemas de IA podem errar com muita confiança.

## Objetivo

Fabricar **10 produtos em 90 segundos** sem esgotar os recursos.

## Regras

| Regra | Valor |
|---|---|
| Recursos iniciais | 100 |
| Tempo da partida | 90 s |
| Meta | 10 produtos |
| Tempo de produção (por máquina ligada) | 12 s por produto |
| Custo de cada produto | 6 recursos |
| Desgaste | Sobe 2% por segundo enquanto a máquina está ligada |
| Falha | Acima de 40% de desgaste a máquina pode quebrar (o risco cresce com o desgaste) e perde o produto em andamento |
| Revisão preventiva (máquina funcionando) | 8 recursos, 3 s, zera o desgaste |
| Conserto (máquina quebrada) | 15 recursos, 3 s, zera o desgaste |
| Sugestões da IA | A cada ~10 s; o jogador tem 8 s para responder; ~30% são inadequadas |

- **Vitória:** fabricar 10 produtos dentro do tempo.
- **Derrota:** o tempo acabar, ou os recursos não serem suficientes para continuar produzindo.
- **Pontuação:** 100 por produto + 50 por decisão correta − 30 por decisão errada; na vitória, soma os recursos restantes e 2 pontos por segundo restante. O recorde fica salvo em `data/recorde.txt`.

Todos os valores ficam em `src/config.py` e podem ser ajustados.

## Controles

- **Mouse (clique esquerdo):**
  - clicar na máquina ou em **Ligar/Desligar** liga ou desliga a máquina;
  - **Revisar / Consertar** inicia a manutenção;
  - **Aceitar / Rejeitar** responde à sugestão do Assistente IA.
- **ENTER ou clique:** começar a partida (tela inicial).
- **R ou clique:** jogar novamente (tela final).
- **ESC:** sair do jogo.

## Como executar

Requisitos: **Python 3.10+** (testado com Python 3.12 e Pygame 2.6).

```bash
git clone https://github.com/Guiraldelli-A/Factory-Control-PUC.git
cd Factory-Control-PUC
pip install -r requirements.txt
python main.py
```

> No Windows, se o comando `python` não for encontrado, instale o Python pelo site oficial marcando a opção **"Add python.exe to PATH"**.

## Como executar os testes

```bash
python -m pytest
```

Os testes ficam em `tests/test_logica.py` e cobrem produção, consumo de recursos, desgaste e falhas, manutenção, recomendações da IA, decisões do jogador, vitória/derrota, pontuação e leitura/escrita do recorde.

## Estrutura do projeto

Organização baseada no template oficial da disciplina:

| Caminho | Conteúdo |
|---|---|
| `main.py` | Ponto de entrada (`python main.py`) |
| `src/config.py` | Tela, cores, regras e caminhos de arquivos |
| `src/funcoes.py` | Regras do jogo (sem Pygame, testáveis com pytest) |
| `src/interface.py` | Desenho das telas, botões e painéis |
| `src/jogo.py` | Loop principal: eventos, atualização e desenho |
| `src/dados.py` | Leitura e gravação do recorde |
| `src/sprites.py` | Recorte de spritesheet (do template; ainda não utilizado) |
| `data/` | Arquivos de dados (`recorde.txt`) |
| `tests/` | Testes automatizados com pytest |
| `docs/` | Proposta (`proposta.md`) e roteiro de implementação (`roteiro.md`) |

### Conceitos da disciplina utilizados

Variáveis e constantes, condicionais, laços (`for`/`while`), **listas** (máquinas, sugestões), **dicionários** (cada máquina, estado da partida, recomendação), **tuplas** (cores, retorno de `iniciar_manutencao`), funções com docstrings, modularização em arquivos, **leitura e escrita de arquivo** (recorde) e **testes** com pytest.

## Checklist de entregas

### Entrega 1 — Proposta (15/11/2026)

- [x] Conceito, objetivo e regras previstas.
- [x] Integrantes identificados.
- [x] `docs/proposta.md` preenchido.
- [x] ZIP enviado pelo Canvas.

### Entrega 2 — Versão parcial executável (22/11/2026)

- [x] Janela do Pygame, loop principal e controles com mouse.
- [x] Produção, recursos, desgaste, falhas e manutenção.
- [x] Recomendações automáticas da IA com Aceitar/Rejeitar.
- [x] Vitória, derrota, pontuação e recorde em arquivo.
- [x] Testes com pytest.
- [ ] ZIP enviado pelo Canvas.

### Entrega 3 — Versão final (29/11/2026)

- [ ] Balanceamento a partir de testes com jogadores.
- [ ] Melhorias de interface (ver `docs/roteiro.md`).
- [ ] README e proposta revisados.
- [ ] Teste completo do jogo e envio do ZIP.

## Recursos externos e créditos

- Estrutura de pastas, `main.py`, `src/dados.py`, `src/sprites.py` e `assets/imagens/spritesheet.bmp`: [template oficial da disciplina](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template).
- Biblioteca [Pygame](https://www.pygame.org/) (licença LGPL).
- Fontes: fontes do sistema operacional (Segoe UI/Arial), carregadas com `pygame.font.SysFont`.
- Todos os elementos visuais do jogo (máquinas, engrenagens, barras e painéis) são desenhados com formas geométricas do próprio Pygame.
- Desenvolvimento com apoio do assistente de IA Claude (Anthropic) para planejamento, código e testes; o código foi revisado e testado pelo grupo.
