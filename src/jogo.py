"""Loop principal do Factory Control."""


import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    META_PRODUTOS,
    CAMINHO_RECORDE,
)
from src.funcoes import (
    criar_estado,
    criar_maquinas,
    alternar_maquina,
    iniciar_manutencao,
    responder_recomendacao,
    atualizar_partida,
    verificar_fim,
    calcular_pontuacao,
    definir_mensagem,
    status_maquina,
)
from src.dados import salvar_recorde, carregar_recorde
from src import interface


def tratar_clique_maquinas(posicao, estado, maquinas):
    """Trata cliques nas máquinas e nos botões delas."""
    for indice in range(len(maquinas)):
        maquina = maquinas[indice]
        areas = interface.retangulos_maquina(indice)

        if areas["manutencao"].collidepoint(posicao):
            if maquina["em_manutencao"] > 0:
                definir_mensagem(estado, f"A {maquina['nome']} já está em manutenção.")
                return
            estado["recursos"], iniciou = iniciar_manutencao(maquina, estado["recursos"])
            if iniciou:
                definir_mensagem(estado, f"Manutenção iniciada na {maquina['nome']}.")
            else:
                definir_mensagem(estado, "Recursos insuficientes para a manutenção.", "ruim")
            return

        if areas["ligar"].collidepoint(posicao) or areas["cartao"].collidepoint(posicao):
            if not alternar_maquina(maquina):
                if status_maquina(maquina) == "quebrada":
                    definir_mensagem(estado, f"A {maquina['nome']} está quebrada: faça o conserto.", "ruim")
                else:
                    definir_mensagem(estado, f"Aguarde o fim da manutenção da {maquina['nome']}.")
            return


def tratar_clique_jogo(posicao, estado, maquinas):
    """Trata um clique durante a partida."""
    if estado["recomendacao"] is not None:
        if interface.BOTAO_ACEITAR.collidepoint(posicao):
            responder_recomendacao(estado, maquinas, True)
            return
        if interface.BOTAO_REJEITAR.collidepoint(posicao):
            responder_recomendacao(estado, maquinas, False)
            return
    tratar_clique_maquinas(posicao, estado, maquinas)


def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()
    fontes = interface.carregar_fontes()

    recorde = carregar_recorde(CAMINHO_RECORDE)
    estado = criar_estado()
    maquinas = criar_maquinas()
    tela_atual = "inicio"
    resultado = None
    pontuacao = 0
    novo_recorde = False
    tempo_na_tela_fim = 0.0
    rodando = True

    while rodando:
        dt = relogio.tick(FPS) / 1000
        if dt > 0.1:
            dt = 0.1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif tela_atual == "inicio" and evento.key == pygame.K_RETURN:
                    tela_atual = "jogando"
                elif tela_atual == "fim" and tempo_na_tela_fim > 1 and evento.key == pygame.K_r:
                    estado = criar_estado()
                    maquinas = criar_maquinas()
                    tela_atual = "jogando"

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if tela_atual == "inicio":
                    tela_atual = "jogando"
                elif tela_atual == "jogando":
                    tratar_clique_jogo(evento.pos, estado, maquinas)
                elif tela_atual == "fim" and tempo_na_tela_fim > 1:
                    estado = criar_estado()
                    maquinas = criar_maquinas()
                    tela_atual = "jogando"

        if tela_atual == "jogando":
            atualizar_partida(estado, maquinas, dt)
            pygame.display.set_caption(
                f"{TITULO_JOGO} | Produtos: {estado['produtos']}/{META_PRODUTOS} | "
                f"Recursos: {estado['recursos']} | Tempo: {int(estado['tempo_restante'])}s"
            )

            resultado = verificar_fim(estado, maquinas)
            if resultado is not None:
                pontuacao = calcular_pontuacao(estado, resultado)
                novo_recorde = pontuacao > recorde
                if novo_recorde:
                    recorde = pontuacao
                    salvar_recorde(CAMINHO_RECORDE, recorde)
                tela_atual = "fim"
                tempo_na_tela_fim = 0.0

        elif tela_atual == "fim":
            tempo_na_tela_fim = tempo_na_tela_fim + dt

        piscar = (pygame.time.get_ticks() // 300) % 2 == 0

        if tela_atual == "inicio":
            interface.desenhar_tela_inicio(tela, fontes, recorde)
        elif tela_atual == "jogando":
            interface.desenhar_tela_jogo(tela, fontes, estado, maquinas, recorde, piscar)
        else:
            interface.desenhar_tela_fim(tela, fontes, estado, resultado, pontuacao, recorde, novo_recorde)

        pygame.display.flip()

    pygame.quit()
