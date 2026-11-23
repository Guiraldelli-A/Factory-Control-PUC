# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na etapa inicial do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com **Python e Pygame** dentro do prazo disponível. Consulte o enunciado publicado no Canvas para conhecer o eixo temático e as orientações vigentes.

## 1. Nome provisório do jogo

Informe o nome provisório do jogo.

**Nome:**

> Factory Control

## 2. Integrantes do grupo

- Nome 1: Arthur Antonio Guiraldelli
- Nome 2: Luiz Eduardo Figueiredo Campos
- Nome 3: Caio Utsch Pedra

## 3. Tema escolhido

Indique qual tema específico o grupo escolheu **dentro do eixo temático definido no enunciado**.

**Tema:**

> Inteligência artificial no gerenciamento industrial: recomendações automatizadas e supervisão humana responsável.

**Como esse tema se relaciona com o jogo?** Explique brevemente (2 a 4 linhas) como ele aparecerá nos objetivos, nas regras ou nos desafios, e não apenas nas imagens ou no cenário.

> O jogador administra uma fábrica e recebe sugestões de um sistema automatizado para manter a produção. Algumas recomendações podem não ser adequadas, por isso ele precisa verificar as condições das máquinas antes de aceitá-las. As escolhas influenciam os recursos e o resultado da partida, destacando a importância da análise crítica de sistemas de IA.

## 4. Tipo de jogo

Indique o estilo do jogo. Exemplos: desviar de obstáculos, coleta de itens, labirinto, perguntas e respostas, memória, Pong, Snake, Breakout, corrida ou sobrevivência simples.

**Tipo escolhido:**

> Simulação simples de gerenciamento e tomada de decisões em 2D, com interação por cliques do mouse.

## 5. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará. O que aparece na tela? O que o jogador controla? O que ele precisa fazer e quais desafios encontrará?

**Descrição:**

> O jogador visualiza três máquinas, os recursos disponíveis, a quantidade de produtos fabricados e um contador de tempo. Pelo mouse, pode ligar, desligar ou realizar manutenção nas máquinas. Durante a partida, surgem falhas e recomendações automáticas que precisam ser avaliadas. O desafio é cumprir a meta sem desperdiçar recursos.

## 6. Objetivo do jogador

Descreva o objetivo principal. Por exemplo: coletar itens, sobreviver por determinado tempo, chegar ao final de um percurso ou completar desafios.

**Objetivo:**

> Produzir 10 unidades de produto antes do tempo acabar, administrando os recursos da fábrica e evitando falhas nas máquinas.

## 7. Regras principais

Liste até cinco regras que expliquem o funcionamento do jogo. Exemplos: o jogador começa com três vidas; acertos somam pontos; colisões retiram vidas.

- Regra 1: O jogador começa com 100 unidades de recursos e três máquinas disponíveis.
- Regra 2: Cada máquina ligada fabrica produtos ao longo do tempo e consome recursos.
- Regra 3: Uma máquina com falha para de produzir até receber manutenção, que também consome recursos.
- Regra 4: O sistema apresenta recomendações automáticas; cabe ao jogador aceitar ou rejeitar cada sugestão, considerando o estado da fábrica.
- Regra 5: A partida tem tempo limitado, e a quantidade produzida e os recursos restantes aparecem na tela.

## 8. Condição de vitória

Explique como o jogador vence ou conclui a partida. Exemplos: alcançar uma pontuação, finalizar uma fase ou completar todas as tarefas.

**Condição de vitória:**

> Fabricar 10 produtos antes do término do tempo da partida.

## 9. Condição de derrota ou encerramento

Explique quando a partida termina ou como o jogador perde. Exemplos: esgotar as vidas, acabar o tempo ou atingir o limite de erros.

**Condição de derrota ou encerramento:**

> A partida termina em derrota se o tempo acabar antes da meta ou se os recursos se esgotarem sem possibilidade de concluir a produção.

## 10. Elementos previstos no jogo

Descreva brevemente os elementos mais importantes, sem precisar detalhar a implementação.

- **Personagem ou elemento principal:** Três máquinas e um painel de controle da fábrica.
- **Obstáculos ou desafios:** Falhas, consumo de recursos, limite de tempo e sugestões automáticas potencialmente inadequadas.
- **Itens ou objetos de interação (se houver):** Máquinas e botões para operação, manutenção e resposta às recomendações.
- **Pontuação, vidas, tempo ou progresso:** Contagem de produtos (meta de 10), recursos restantes e tempo disponível.

## 11. Controles previstos

Informe como o jogador vai interagir com o jogo (por exemplo, setas para movimentar, espaço para agir ou mouse para selecionar).

**Controles:**

> O jogador usará o mouse para clicar nas máquinas e nos botões de ligar, desligar, fazer manutenção e aceitar ou rejeitar recomendações. O teclado poderá ser usado apenas para sair do jogo (Esc).

## 12. Principais dificuldades esperadas

Cite até três dificuldades que o grupo espera enfrentar. Exemplos: movimentação, colisões, controle de tempo, testes ou uso do GitHub.

- Dificuldade 1: Programar os cliques do mouse e atualizar corretamente o estado de cada máquina.
- Dificuldade 2: Controlar o tempo, a produção e o consumo de recursos sem inconsistências.
- Dificuldade 3: Organizar o código e os testes e trabalhar em conjunto pelo GitHub.

## 13. Escopo mínimo para a entrega final

Descreva a **versão mais simples que já seria jogável**, com as interações e regras essenciais. Evite planejar funcionalidades demais.

**Escopo mínimo:**

> A versão mínima terá uma única tela com três máquinas clicáveis, recursos limitados, fabricação de produtos, um contador de tempo, pelo menos uma situação de falha e recomendações automáticas que exigem decisão do jogador, além de telas ou mensagens de vitória e derrota. O código será organizado em funções e poderá usar uma lista de dicionários para guardar o estado das máquinas, condicionais para aplicar regras e um laço principal do Pygame para processar eventos e atualizar a tela. Inicialmente, as configurações podem ficar no próprio código; se houver uso de arquivos, poderá ser salvo um recorde ou registro de resultados em formato texto. Serão planejados testes de funções de produção, consumo de recursos e condições de vitória/derrota, preferencialmente com pytest.

## 14. Possíveis melhorias, caso haja tempo

Liste até três funcionalidades extras para implementar somente depois que a versão mínima estiver funcionando. Exemplos: sons, fases, ranking, animações ou menu inicial.

- Melhoria 1: Animações simples das máquinas e efeitos sonoros.
- Melhoria 2: Novas fases com metas de produção progressivamente maiores.
- Melhoria 3: Registro da melhor pontuação em arquivo local.
