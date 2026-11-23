"""Desenho das telas do Factory Control com Pygame."""


import pygame

from src.config import (
    LARGURA_TELA,
    META_PRODUTOS,
    TEMPO_PARTIDA,
    TEMPO_PRODUCAO,
    CUSTO_PRODUTO,
    CUSTO_MANUTENCAO,
    CUSTO_CONSERTO,
    TEMPO_RESPOSTA_IA,
    LIMITE_DESGASTE_ALTO,
    LIMITE_DESGASTE_BAIXO,
    RECURSOS_INICIAIS,
    PRETO,
    COR_FUNDO,
    COR_PAINEL,
    COR_PAINEL_CLARO,
    COR_BORDA,
    COR_TEXTO,
    COR_TEXTO_SUAVE,
    COR_VERDE,
    COR_VERMELHO,
    COR_AMARELO,
    COR_AZUL,
    COR_ROXO,
    COR_DESLIGADA,
    COR_REVISAR,
)
from src.funcoes import status_maquina, custo_manutencao

MARGEM = 35
LARGURA_CARTAO = 290
ALTURA_CARTAO = 280
ESPACO_CARTOES = 30
TOPO_CARTOES = 80

CAIXA_IA = pygame.Rect(35, 380, 600, 200)
CAIXA_SUPERVISAO = pygame.Rect(655, 380, 310, 200)
CAIXA_MENSAGEM = pygame.Rect(35, 592, 930, 36)

BOTAO_ACEITAR = pygame.Rect(55, 525, 150, 40)
BOTAO_REJEITAR = pygame.Rect(220, 525, 150, 40)

TEXTO_STATUS = {
    "ligada": "Produzindo",
    "desligada": "Desligada",
    "quebrada": "QUEBRADA",
    "manutencao": "Em manutenção",
}

COR_STATUS = {
    "ligada": COR_VERDE,
    "desligada": COR_DESLIGADA,
    "quebrada": COR_VERMELHO,
    "manutencao": COR_AMARELO,
}

COR_MENSAGEM = {
    "boa": COR_VERDE,
    "ruim": COR_VERMELHO,
    "neutra": COR_AZUL,
}

TITULOS_FIM = {
    "vitoria": ("META CUMPRIDA!", COR_VERDE, "A fábrica produziu tudo dentro do prazo."),
    "derrota_tempo": ("O TEMPO ACABOU", COR_VERMELHO, "A meta de produção não foi atingida a tempo."),
    "derrota_recursos": ("RECURSOS ESGOTADOS", COR_VERMELHO, "Não há recursos suficientes para continuar produzindo."),
}


def retangulos_maquina(indice):
    """Retorna os retângulos do cartão e dos botões da máquina."""
    x = MARGEM + indice * (LARGURA_CARTAO + ESPACO_CARTOES)
    cartao = pygame.Rect(x, TOPO_CARTOES, LARGURA_CARTAO, ALTURA_CARTAO)
    ligar = pygame.Rect(x + 15, cartao.bottom - 48, 125, 36)
    manutencao = pygame.Rect(x + 150, cartao.bottom - 48, 125, 36)
    return {"cartao": cartao, "ligar": ligar, "manutencao": manutencao}


def carregar_fontes():
    """Carrega as fontes do jogo."""
    nomes = "segoeui,arial,dejavusans"
    fontes = {
        "titulo": pygame.font.SysFont(nomes, 56, bold=True),
        "grande": pygame.font.SysFont(nomes, 30, bold=True),
        "media": pygame.font.SysFont(nomes, 21, bold=True),
        "normal": pygame.font.SysFont(nomes, 19),
        "pequena": pygame.font.SysFont(nomes, 16),
    }
    return fontes


def desenhar_texto(tela, texto, fonte, cor, posicao, centralizado=False):
    """Desenha um texto na tela."""
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()
    if centralizado:
        retangulo.center = posicao
    else:
        retangulo.topleft = posicao
    tela.blit(imagem, retangulo)


def quebrar_texto(texto, fonte, largura_maxima):
    """Divide um texto em linhas que caibam na largura."""
    linhas = []
    linha_atual = ""
    for palavra in texto.split():
        if linha_atual == "":
            tentativa = palavra
        else:
            tentativa = linha_atual + " " + palavra

        largura_tentativa = fonte.size(tentativa)[0]
        if largura_tentativa <= largura_maxima:
            linha_atual = tentativa
        else:
            if linha_atual != "":
                linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual != "":
        linhas.append(linha_atual)
    return linhas


def cortar_texto(texto, fonte, largura):
    """Corta o texto com reticências para caber em uma linha."""
    if fonte.size(texto)[0] <= largura:
        return texto
    while len(texto) > 4 and fonte.size(texto + "...")[0] > largura:
        texto = texto[:-1]
    return texto + "..."


def desenhar_painel(tela, retangulo, borda=COR_BORDA):
    """Desenha um painel com cantos arredondados."""
    pygame.draw.rect(tela, COR_PAINEL, retangulo, border_radius=12)
    pygame.draw.rect(tela, borda, retangulo, width=2, border_radius=12)


def desenhar_barra(tela, retangulo, fracao, cor):
    """Desenha uma barra de progresso (fracao de 0 a 1)."""
    if fracao < 0:
        fracao = 0
    if fracao > 1:
        fracao = 1
    pygame.draw.rect(tela, COR_FUNDO, retangulo, border_radius=6)
    largura = int(retangulo.width * fracao)
    if largura > 0:
        preenchido = pygame.Rect(retangulo.x, retangulo.y, largura, retangulo.height)
        pygame.draw.rect(tela, cor, preenchido, border_radius=6)


def desenhar_botao(tela, retangulo, texto, fonte, cor, ativo=True):
    """Desenha um botão (mais claro quando o mouse está em cima)."""
    if not ativo:
        cor = COR_PAINEL_CLARO
    elif retangulo.collidepoint(pygame.mouse.get_pos()):
        cor = (min(255, cor[0] + 35), min(255, cor[1] + 35), min(255, cor[2] + 35))

    pygame.draw.rect(tela, cor, retangulo, border_radius=8)

    cor_texto = COR_TEXTO
    if not ativo:
        cor_texto = COR_TEXTO_SUAVE
    desenhar_texto(tela, texto, fonte, cor_texto, retangulo.center, True)


def cor_do_desgaste(desgaste):
    """Verde (baixo), amarelo (médio) ou vermelho (alto)."""
    if desgaste >= LIMITE_DESGASTE_ALTO:
        return COR_VERMELHO
    if desgaste >= LIMITE_DESGASTE_BAIXO:
        return COR_AMARELO
    return COR_VERDE


def desenhar_barra_superior(tela, fontes, estado):
    """Desenha o topo: título, tempo, recursos e produtos."""
    pygame.draw.rect(tela, COR_PAINEL, (0, 0, LARGURA_TELA, 62))
    pygame.draw.line(tela, COR_BORDA, (0, 62), (LARGURA_TELA, 62), 2)
    desenhar_texto(tela, "FACTORY CONTROL", fontes["grande"], COR_TEXTO, (35, 12))

    cor_tempo = COR_TEXTO
    if estado["tempo_restante"] <= 20:
        cor_tempo = COR_VERMELHO
    desenhar_texto(tela, "Tempo", fontes["pequena"], COR_TEXTO_SUAVE, (370, 6))
    desenhar_texto(tela, f"{int(estado['tempo_restante'])}s", fontes["media"], cor_tempo, (370, 26))
    desenhar_barra(tela, pygame.Rect(420, 34, 40, 10), estado["tempo_restante"] / TEMPO_PARTIDA, COR_AMARELO)

    cor_recursos = COR_TEXTO
    if estado["recursos"] < 20:
        cor_recursos = COR_VERMELHO
    desenhar_texto(tela, "Recursos", fontes["pequena"], COR_TEXTO_SUAVE, (490, 6))
    desenhar_texto(tela, str(estado["recursos"]), fontes["media"], cor_recursos, (490, 26))
    desenhar_barra(tela, pygame.Rect(545, 34, 100, 10), estado["recursos"] / RECURSOS_INICIAIS, COR_AZUL)

    desenhar_texto(tela, "Produtos", fontes["pequena"], COR_TEXTO_SUAVE, (680, 6))
    desenhar_texto(tela, f"{estado['produtos']}/{META_PRODUTOS}", fontes["media"], COR_TEXTO, (680, 26))
    desenhar_barra(tela, pygame.Rect(750, 34, 215, 10), estado["produtos"] / META_PRODUTOS, COR_VERDE)


def desenhar_desenho_maquina(tela, cartao, maquina, status, piscar):
    """Desenha a máquina, a lâmpada e o produto andando na esteira."""
    cor = COR_STATUS[status]

    corpo = pygame.Rect(cartao.x + 95, cartao.y + 76, 100, 42)
    chamine = pygame.Rect(corpo.x + 15, corpo.y - 12, 16, 12)
    pygame.draw.rect(tela, cor, chamine)
    pygame.draw.rect(tela, cor, corpo, border_radius=6)
    pygame.draw.rect(tela, COR_PAINEL, (corpo.x + 12, corpo.y + 11, 44, 20), border_radius=4)

    cor_lampada = COR_PAINEL
    if status == "ligada" and piscar:
        cor_lampada = COR_AMARELO
    if status == "quebrada" and piscar:
        cor_lampada = COR_VERMELHO
    pygame.draw.circle(tela, cor_lampada, (corpo.right - 18, corpo.y + 21), 8)

    esteira = pygame.Rect(cartao.x + 25, corpo.bottom + 16, LARGURA_CARTAO - 50, 5)
    pygame.draw.rect(tela, COR_BORDA, esteira, border_radius=3)
    if maquina["progresso"] > 0:
        x_produto = esteira.x + int(maquina["progresso"] * (esteira.width - 12))
        pygame.draw.rect(tela, COR_AZUL, (x_produto, esteira.y - 12, 12, 12), border_radius=3)


def desenhar_maquina(tela, fontes, maquina, indice, piscar, destacada):
    """Desenha o cartão de uma máquina com barras e botões."""
    areas = retangulos_maquina(indice)
    cartao = areas["cartao"]
    status = status_maquina(maquina)
    cor_status = COR_STATUS[status]

    pygame.draw.rect(tela, COR_PAINEL, cartao, border_radius=12)
    if destacada:
        pygame.draw.rect(tela, COR_ROXO, cartao, width=4, border_radius=12)
    else:
        pygame.draw.rect(tela, cor_status, cartao, width=2, border_radius=12)

    x = cartao.x + 15
    desenhar_texto(tela, maquina["nome"], fontes["media"], COR_TEXTO, (x, cartao.y + 10))
    desenhar_texto(tela, TEXTO_STATUS[status], fontes["normal"], cor_status, (x, cartao.y + 36))
    if status == "manutencao":
        restante = f"{round(maquina['em_manutencao'], 1)}s"
        desenhar_texto(tela, restante, fontes["normal"], COR_AMARELO, (cartao.right - 70, cartao.y + 36))

    desenhar_desenho_maquina(tela, cartao, maquina, status, piscar)

    y = cartao.y + 145
    segundos = int(maquina["progresso"] * TEMPO_PRODUCAO)
    desenhar_texto(tela, f"Produção ({segundos}/{TEMPO_PRODUCAO}s)", fontes["pequena"], COR_TEXTO_SUAVE, (x, y))
    desenhar_barra(tela, pygame.Rect(x, y + 22, LARGURA_CARTAO - 30, 12), maquina["progresso"], COR_AZUL)

    y = y + 42
    desgaste = maquina["desgaste"]
    desenhar_texto(tela, f"Desgaste ({int(desgaste)}%)", fontes["pequena"], COR_TEXTO_SUAVE, (x, y))
    desenhar_barra(tela, pygame.Rect(x, y + 22, LARGURA_CARTAO - 30, 12), desgaste / 100, cor_do_desgaste(desgaste))

    pode_operar = status == "ligada" or status == "desligada"
    if maquina["ligada"]:
        desenhar_botao(tela, areas["ligar"], "Desligar", fontes["normal"], COR_DESLIGADA, pode_operar)
    else:
        desenhar_botao(tela, areas["ligar"], "Ligar", fontes["normal"], COR_VERDE, pode_operar)

    custo = custo_manutencao(maquina)
    if status == "quebrada":
        desenhar_botao(tela, areas["manutencao"], f"Consertar -{custo}", fontes["normal"], COR_VERMELHO)
    else:
        desenhar_botao(tela, areas["manutencao"], f"Revisar -{custo}", fontes["normal"], COR_REVISAR,
                       status != "manutencao")


def desenhar_caixa_ia(tela, fontes, estado):
    """Desenha a caixa do Assistente IA."""
    desenhar_painel(tela, CAIXA_IA, COR_ROXO)
    x = CAIXA_IA.x + 20
    desenhar_texto(tela, "ASSISTENTE IA", fontes["media"], COR_ROXO, (x, CAIXA_IA.y + 12))

    recomendacao = estado["recomendacao"]
    if recomendacao is None:
        desenhar_texto(tela, "Analisando a fábrica...", fontes["normal"], COR_TEXTO_SUAVE, (x, CAIXA_IA.y + 50))
        proxima = f"Próxima sugestão em {int(estado['tempo_para_recomendacao']) + 1}s"
        desenhar_texto(tela, proxima, fontes["pequena"], COR_TEXTO_SUAVE, (x, CAIXA_IA.y + 78))
        desenhar_texto(tela, "Lembre-se: a IA pode errar. Confira as máquinas antes de aceitar.",
                       fontes["pequena"], COR_TEXTO_SUAVE, (x, CAIXA_IA.bottom - 40))
        return

    desenhar_texto(tela, f"Confiança: {recomendacao['confianca']}%", fontes["pequena"], COR_TEXTO_SUAVE,
                   (CAIXA_IA.right - 140, CAIXA_IA.y + 15))

    y = CAIXA_IA.y + 48
    for linha in quebrar_texto(f"\"{recomendacao['texto']}\"", fontes["normal"], CAIXA_IA.width - 40):
        desenhar_texto(tela, linha, fontes["normal"], COR_TEXTO, (x, y))
        y = y + 28

    x_barra = BOTAO_REJEITAR.right + 20
    desenhar_texto(tela, f"{int(recomendacao['tempo_restante']) + 1}s para responder", fontes["pequena"],
                   COR_TEXTO_SUAVE, (x_barra, BOTAO_REJEITAR.y - 14))
    fracao = recomendacao["tempo_restante"] / TEMPO_RESPOSTA_IA
    desenhar_barra(tela, pygame.Rect(x_barra, BOTAO_REJEITAR.centery - 5, 200, 10), fracao, COR_ROXO)

    desenhar_botao(tela, BOTAO_ACEITAR, "Aceitar", fontes["media"], COR_VERDE)
    desenhar_botao(tela, BOTAO_REJEITAR, "Rejeitar", fontes["media"], COR_VERMELHO)


def desenhar_caixa_supervisao(tela, fontes, estado, recorde):
    """Desenha o painel de desempenho do jogador."""
    desenhar_painel(tela, CAIXA_SUPERVISAO)
    x = CAIXA_SUPERVISAO.x + 20
    y = CAIXA_SUPERVISAO.y + 12
    desenhar_texto(tela, "SUPERVISÃO HUMANA", fontes["media"], COR_TEXTO, (x, y))
    desenhar_texto(tela, f"Decisões corretas: {estado['decisoes_corretas']}", fontes["normal"], COR_VERDE, (x, y + 38))
    desenhar_texto(tela, f"Decisões erradas: {estado['decisoes_erradas']}", fontes["normal"], COR_VERMELHO, (x, y + 64))
    erros = f"Erros da IA detectados: {estado['ia_erros_detectados']}/{estado['ia_erros_recebidos']}"
    desenhar_texto(tela, erros, fontes["normal"], COR_TEXTO, (x, y + 90))
    desenhar_texto(tela, f"Recorde: {recorde} pts", fontes["pequena"], COR_TEXTO_SUAVE, (x, y + 124))
    custos = f"Produto: -{CUSTO_PRODUTO}  |  Revisão: -{CUSTO_MANUTENCAO}  |  Conserto: -{CUSTO_CONSERTO}"
    desenhar_texto(tela, custos, fontes["pequena"], COR_TEXTO_SUAVE, (x, y + 146))


def desenhar_mensagem(tela, fontes, estado):
    """Desenha a faixa de aviso (ou uma dica, se não houver aviso)."""
    if estado["mensagem"] == "":
        dica = "Ligue as máquinas para produzir. Revise as desgastadas antes que quebrem. ESC: sair"
        desenhar_texto(tela, dica, fontes["pequena"], COR_TEXTO_SUAVE, (CAIXA_MENSAGEM.x + 10, CAIXA_MENSAGEM.y + 8))
        return

    pygame.draw.rect(tela, COR_MENSAGEM[estado["cor_mensagem"]], CAIXA_MENSAGEM, border_radius=8)

    largura = CAIXA_MENSAGEM.width - 20
    fonte = fontes["normal"]
    if fonte.size(estado["mensagem"])[0] > largura:
        fonte = fontes["pequena"]
    texto = cortar_texto(estado["mensagem"], fonte, largura)
    y = CAIXA_MENSAGEM.centery - fonte.get_height() // 2
    desenhar_texto(tela, texto, fonte, PRETO, (CAIXA_MENSAGEM.x + 10, y))


def desenhar_tela_jogo(tela, fontes, estado, maquinas, recorde, piscar):
    """Desenha a tela da partida."""
    tela.fill(COR_FUNDO)
    desenhar_barra_superior(tela, fontes, estado)

    indice_destacado = -1
    if estado["recomendacao"] is not None:
        indice_destacado = estado["recomendacao"]["indice"]

    for indice in range(len(maquinas)):
        desenhar_maquina(tela, fontes, maquinas[indice], indice, piscar, indice == indice_destacado)

    desenhar_caixa_ia(tela, fontes, estado)
    desenhar_caixa_supervisao(tela, fontes, estado, recorde)
    desenhar_mensagem(tela, fontes, estado)


def desenhar_tela_inicio(tela, fontes, recorde):
    """Desenha a tela inicial com as regras."""
    tela.fill(COR_FUNDO)
    centro = LARGURA_TELA // 2
    desenhar_texto(tela, "FACTORY CONTROL", fontes["titulo"], COR_TEXTO, (centro, 80), True)
    desenhar_texto(tela, "Você supervisiona uma fábrica. A IA ajuda, mas quem decide é você.",
                   fontes["normal"], COR_ROXO, (centro, 135), True)

    painel = pygame.Rect(140, 175, 720, 320)
    desenhar_painel(tela, painel)
    regras = [
        f"Meta: fabricar {META_PRODUTOS} produtos em {TEMPO_PARTIDA} segundos.",
        f"Você começa com {RECURSOS_INICIAIS} recursos. Cada produto custa {CUSTO_PRODUTO}.",
        f"Máquinas ligadas produzem 1 item a cada {TEMPO_PRODUCAO}s, mas se desgastam.",
        "Acima de 40% de desgaste a máquina pode quebrar (e perde o produto).",
        f"Revisão preventiva: {CUSTO_MANUTENCAO} recursos. Conserto após quebra: {CUSTO_CONSERTO}.",
        "O Assistente IA dá sugestões, mas cerca de 30% estão erradas!",
        "Aceite ou rejeite cada sugestão olhando o estado real das máquinas.",
        "Derrota: tempo acabar ou recursos insuficientes para continuar.",
    ]
    y = painel.y + 22
    for regra in regras:
        desenhar_texto(tela, "•  " + regra, fontes["normal"], COR_TEXTO, (painel.x + 30, y))
        y = y + 36

    desenhar_texto(tela, "Clique ou pressione ENTER para começar", fontes["media"], COR_VERDE, (centro, 540), True)
    desenhar_texto(tela, f"Recorde atual: {recorde} pts   |   ESC: sair", fontes["pequena"], COR_TEXTO_SUAVE,
                   (centro, 580), True)


def desenhar_tela_fim(tela, fontes, estado, resultado, pontuacao, recorde, novo_recorde):
    """Desenha a tela de resultado."""
    tela.fill(COR_FUNDO)
    centro = LARGURA_TELA // 2
    titulo, cor, descricao = TITULOS_FIM[resultado]
    desenhar_texto(tela, titulo, fontes["titulo"], cor, (centro, 80), True)
    desenhar_texto(tela, descricao, fontes["normal"], COR_TEXTO_SUAVE, (centro, 132), True)

    painel = pygame.Rect(220, 170, 560, 300)
    desenhar_painel(tela, painel)

    linhas = [
        ("Produtos fabricados", f"{estado['produtos']}/{META_PRODUTOS}"),
        ("Recursos restantes", str(estado["recursos"])),
        ("Tempo restante", f"{int(estado['tempo_restante'])}s"),
        ("Decisões corretas sobre a IA", str(estado["decisoes_corretas"])),
        ("Decisões erradas sobre a IA", str(estado["decisoes_erradas"])),
        ("Erros da IA que você detectou", f"{estado['ia_erros_detectados']}/{estado['ia_erros_recebidos']}"),
    ]
    y = painel.y + 22
    for rotulo, valor in linhas:
        desenhar_texto(tela, rotulo, fontes["normal"], COR_TEXTO_SUAVE, (painel.x + 30, y))
        desenhar_texto(tela, valor, fontes["media"], COR_TEXTO, (painel.right - 130, y))
        y = y + 34

    desenhar_texto(tela, f"Pontuação: {pontuacao}", fontes["grande"], COR_TEXTO, (centro, y + 30), True)

    if novo_recorde:
        desenhar_texto(tela, "NOVO RECORDE!", fontes["media"], COR_AMARELO, (centro, 500), True)
    else:
        desenhar_texto(tela, f"Recorde: {recorde} pts", fontes["media"], COR_TEXTO_SUAVE, (centro, 500), True)

    desenhar_texto(tela, "Sistemas de IA podem errar com muita confiança: a supervisão humana faz a diferença.",
                   fontes["normal"], COR_ROXO, (centro, 545), True)
    desenhar_texto(tela, "R ou clique: jogar novamente   |   ESC: sair", fontes["pequena"], COR_TEXTO_SUAVE,
                   (centro, 590), True)
