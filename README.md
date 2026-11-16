# Factory Control

Projeto prático da disciplina de **Introdução a Algoritmos**, desenvolvido em **Python e Pygame**.

**Situação do projeto:** fase de planejamento (Ponto de Controle 01). As funcionalidades descritas abaixo são previstas para a versão final e ainda não representam um jogo implementado.

## Integrantes do grupo

- Arthur Antonio Guiraldelli
- Luiz Eduardo Figueiredo Campos
- Caio Utsch Pedra

## Estrutura do projeto

A organização inicial segue o template oficial da disciplina:

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, interface e dados).
- `assets/`: imagens, fontes e sons, caso sejam utilizados.
- `data/`: arquivos persistentes, como recordes, caso sejam implementados.
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação, incluindo a proposta inicial do jogo.

## Descrição do jogo

**Factory Control** será um jogo 2D de gerenciamento de uma pequena fábrica. O jogador acompanhará uma linha de produção e controlará máquinas por meio de cliques do mouse, decidindo quando iniciar a produção e quando realizar manutenção.

A fábrica terá recursos limitados, e as máquinas poderão apresentar falhas. Um sistema de recomendações automáticas, representando uma aplicação simples de inteligência artificial na indústria, poderá sugerir ações. Algumas recomendações poderão não ser adequadas; o jogador terá de avaliar a situação antes de aceitá-las. O objetivo é destacar a importância da **supervisão humana e do uso responsável da IA**.

O sistema de recomendações será simulado com regras de programação, sem necessidade de treinar uma IA real.

## Objetivo do jogador

Produzir **10 produtos** antes do fim do tempo, administrando os recursos disponíveis e evitando que problemas nas máquinas interrompam a produção. Os valores poderão ser ajustados durante o desenvolvimento e os testes.

## Regras do jogo

- A partida começará com **100 unidades de recursos** e um tempo limitado.
- O jogador poderá clicar nas máquinas para iniciar ações de produção ou manutenção.
- Produzir itens consumirá recursos; cada produto concluído aumentará o progresso da partida.
- As máquinas poderão apresentar falhas e precisar de manutenção para voltar a produzir normalmente.
- O sistema automatizado poderá sugerir decisões, mas caberá ao jogador avaliá-las e escolher como agir.
- A vitória ocorrerá ao fabricar 10 produtos dentro do tempo previsto. A partida terminará sem vitória se o tempo acabar ou se os recursos necessários se esgotarem antes de atingir a meta.

## Controles

- **Mouse (clique esquerdo):** selecionar máquinas e acionar botões de produção, manutenção e decisões.
- **ESC:** sair do jogo, se esse comando for implementado na interface final.

Não haverá personagem controlado por teclado: a interação principal será feita diretamente com a interface da fábrica.

## Como executar o projeto

> **PC01:** nesta etapa, o projeto está em planejamento. Os comandos abaixo serão usados para executar o jogo conforme a implementação avançar.

### 1. Clonar o repositório

No GitHub do grupo, clique em **Code**, copie a URL HTTPS e use:

```bash
git clone URL_DO_REPOSITORIO_DO_GRUPO
cd Factory-Control-PUC
pip install -r requirements.txt
python main.py
```

Se o nome da pasta criada pelo clone for diferente, ajuste o comando `cd`.

## Como executar os testes

Os testes automatizados serão desenvolvidos ao longo do projeto, principalmente para verificar regras de produção, consumo de recursos, manutenção e condições de vitória ou derrota.

```bash
python -m pytest
```

## Checklist de entregas

### Ponto de Controle 01 — Proposta inicial

- [x] Definir o conceito, o objetivo e as regras previstas do jogo.
- [x] Identificar os três integrantes do grupo.
- [x] Atualizar o README com o planejamento do Factory Control.
- [X] Conferir se o arquivo `docs/proposta.MD` (ou `docs/proposta.md`, se renomeado) está preenchido no repositório.
- [X] Baixar o repositório completo em ZIP e enviá-lo pelo Canvas.

### Etapas posteriores — Desenvolvimento

- [ ] Implementar a interface e os controles com o mouse.
- [ ] Implementar produção, recursos e manutenção.
- [ ] Implementar as recomendações automáticas e decisões do jogador.
- [ ] Implementar vitória, derrota e encerramento.
- [ ] Criar e executar testes com `pytest`.
- [ ] Revisar a documentação e testar o jogo completo.

## Observações para os alunos

- O projeto será desenvolvido a partir do template oficial da disciplina.
- A versão inicial será simples e funcional, priorizando as regras e a jogabilidade, não a complexidade visual.
- O grupo deverá organizar o código em funções e módulos, documentar decisões importantes e registrar a origem e as licenças de eventuais assets externos.
- As características descritas neste README são **planejadas** e poderão ser refinadas durante a implementação.
