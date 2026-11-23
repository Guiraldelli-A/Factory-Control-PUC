"""Regras do Factory Control (sem Pygame, para poderem ser testadas)."""


import random

from src.config import (
    QUANTIDADE_MAQUINAS,
    RECURSOS_INICIAIS,
    TEMPO_PARTIDA,
    META_PRODUTOS,
    TEMPO_PRODUCAO,
    CUSTO_PRODUTO,
    CUSTO_MANUTENCAO,
    CUSTO_CONSERTO,
    DURACAO_MANUTENCAO,
    DESGASTE_POR_SEGUNDO,
    DESGASTE_SEGURO,
    CHANCE_FALHA_MAXIMA,
    LIMITE_DESGASTE_ALTO,
    LIMITE_DESGASTE_BAIXO,
    CHANCE_IA_ERRAR,
    PRIMEIRA_RECOMENDACAO,
    INTERVALO_RECOMENDACAO,
    TEMPO_RESPOSTA_IA,
    DURACAO_MENSAGEM,
    PONTOS_POR_PRODUTO,
    PONTOS_DECISAO_CORRETA,
    PONTOS_DECISAO_ERRADA,
    PONTOS_POR_SEGUNDO_RESTANTE,
)


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def criar_maquina(nome):
    """Cria uma máquina nova e desligada."""
    maquina = {
        "nome": nome,
        "ligada": False,
        "quebrada": False,
        "desgaste": 0.0,
        "progresso": 0.0,
        "em_manutencao": 0.0,
        "religar": False,
    }
    return maquina


def criar_maquinas(quantidade=QUANTIDADE_MAQUINAS):
    """Cria a lista de máquinas da fábrica."""
    maquinas = []
    for numero in range(1, quantidade + 1):
        maquinas.append(criar_maquina(f"Máquina {numero}"))
    return maquinas


def criar_estado():
    """Cria o dicionário com o estado da partida."""
    estado = {
        "recursos": RECURSOS_INICIAIS,
        "produtos": 0,
        "tempo_restante": float(TEMPO_PARTIDA),
        "decisoes_corretas": 0,
        "decisoes_erradas": 0,
        "ia_erros_recebidos": 0,
        "ia_erros_detectados": 0,
        "recomendacao": None,
        "tempo_para_recomendacao": float(PRIMEIRA_RECOMENDACAO),
        "mensagem": "",
        "cor_mensagem": "neutra",
        "tempo_mensagem": 0.0,
    }
    return estado


def definir_mensagem(estado, texto, tipo="neutra"):
    """Mostra uma mensagem de aviso por alguns segundos."""
    estado["mensagem"] = texto
    estado["cor_mensagem"] = tipo
    estado["tempo_mensagem"] = float(DURACAO_MENSAGEM)


def status_maquina(maquina):
    """Retorna 'manutencao', 'quebrada', 'ligada' ou 'desligada'."""
    if maquina["em_manutencao"] > 0:
        return "manutencao"
    if maquina["quebrada"]:
        return "quebrada"
    if maquina["ligada"]:
        return "ligada"
    return "desligada"


def alternar_maquina(maquina):
    """Liga ou desliga a máquina. Retorna False se não for possível."""
    if maquina["quebrada"] or maquina["em_manutencao"] > 0:
        return False
    maquina["ligada"] = not maquina["ligada"]
    return True


def custo_manutencao(maquina):
    """Retorna o custo da manutenção (conserto é mais caro)."""
    if maquina["quebrada"]:
        return CUSTO_CONSERTO
    return CUSTO_MANUTENCAO


def iniciar_manutencao(maquina, recursos):
    """Inicia a manutenção. Retorna (recursos_restantes, iniciou)."""
    custo = custo_manutencao(maquina)
    if maquina["em_manutencao"] > 0 or recursos < custo:
        return recursos, False

    maquina["religar"] = maquina["ligada"] or maquina["quebrada"]
    maquina["ligada"] = False
    maquina["em_manutencao"] = float(DURACAO_MANUTENCAO)
    return recursos - custo, True


def chance_de_falha(desgaste, dt):
    """Probabilidade de a máquina quebrar em dt segundos."""
    if desgaste <= DESGASTE_SEGURO:
        return 0.0
    risco = (desgaste - DESGASTE_SEGURO) / (100 - DESGASTE_SEGURO)
    return risco * CHANCE_FALHA_MAXIMA * dt


def atualizar_maquina(maquina, dt, sorteio):
    """Avança a máquina em dt segundos. Retorna True se um produto ficou pronto."""

    if maquina["em_manutencao"] > 0:
        maquina["em_manutencao"] = maquina["em_manutencao"] - dt
        if maquina["em_manutencao"] <= 0:
            maquina["em_manutencao"] = 0.0
            maquina["quebrada"] = False
            maquina["desgaste"] = 0.0
            maquina["ligada"] = maquina["religar"]
            maquina["religar"] = False
        return False

    if maquina["quebrada"] or not maquina["ligada"]:
        return False

    novo_desgaste = maquina["desgaste"] + DESGASTE_POR_SEGUNDO * dt
    maquina["desgaste"] = limitar_valor(novo_desgaste, 0, 100)

    if sorteio < chance_de_falha(maquina["desgaste"], dt):
        maquina["quebrada"] = True
        maquina["ligada"] = False
        maquina["progresso"] = 0.0
        return False

    maquina["progresso"] = maquina["progresso"] + dt / TEMPO_PRODUCAO
    if maquina["progresso"] >= 1:
        maquina["progresso"] = maquina["progresso"] - 1
        return True
    return False


def registrar_produto(estado):
    """Cobra o custo e soma um produto. Retorna False se faltar recurso."""
    if estado["recursos"] < CUSTO_PRODUTO:
        return False
    estado["recursos"] = estado["recursos"] - CUSTO_PRODUTO
    estado["produtos"] = estado["produtos"] + 1
    return True


def criar_recomendacao(acao, indice, adequada, texto, motivo):
    """Cria o dicionário de uma sugestão da IA."""
    recomendacao = {
        "acao": acao,
        "indice": indice,
        "adequada": adequada,
        "texto": texto,
        "motivo": motivo,
        "confianca": 90,
        "tempo_restante": float(TEMPO_RESPOSTA_IA),
    }
    return recomendacao


def opcoes_de_recomendacao(maquinas):
    """Separa as sugestões possíveis em duas listas: (boas, ruins)."""
    boas = []
    ruins = []

    for indice in range(len(maquinas)):
        maquina = maquinas[indice]
        nome = maquina["nome"]
        desgaste = int(maquina["desgaste"])

        if maquina["em_manutencao"] > 0:
            continue

        if maquina["quebrada"]:
            boas.append(criar_recomendacao(
                "manutencao", indice, True,
                f"Falha detectada na {nome}. Recomendo manutenção imediata.",
                f"a {nome} estava quebrada e só volta a produzir após o reparo.",
            ))
        elif maquina["desgaste"] >= LIMITE_DESGASTE_ALTO:
            boas.append(criar_recomendacao(
                "manutencao", indice, True,
                f"O desgaste da {nome} está em {desgaste}%. Recomendo manutenção preventiva.",
                f"com desgaste de {desgaste}%, a {nome} tinha alto risco de quebrar.",
            ))
        elif maquina["desgaste"] < LIMITE_DESGASTE_BAIXO:
            ruins.append(criar_recomendacao(
                "manutencao", indice, False,
                f"Recomendo manutenção preventiva na {nome} para evitar falhas.",
                f"a {nome} tinha só {desgaste}% de desgaste: a manutenção gastaria recursos à toa.",
            ))

        if not maquina["quebrada"]:
            if not maquina["ligada"]:
                boas.append(criar_recomendacao(
                    "ligar", indice, True,
                    f"A {nome} está parada. Ligue-a para acelerar a produção.",
                    "mais máquinas ligadas produzem mais rápido.",
                ))
            elif maquina["desgaste"] < LIMITE_DESGASTE_ALTO:
                ruins.append(criar_recomendacao(
                    "desligar", indice, False,
                    f"Desligue a {nome} para economizar energia.",
                    f"a {nome} estava saudável e produzindo; desligá-la só atrasaria a meta.",
                ))

    return boas, ruins


def gerar_recomendacao(maquinas, sorteio):
    """Gera a próxima sugestão da IA (às vezes errada). Retorna None se não houver."""
    boas, ruins = opcoes_de_recomendacao(maquinas)

    if sorteio < CHANCE_IA_ERRAR and len(ruins) > 0:
        lista = ruins
    elif len(boas) > 0:
        lista = boas
    else:
        lista = ruins

    if len(lista) == 0:
        return None

    recomendacao = random.choice(lista)
    recomendacao["confianca"] = random.randint(85, 98)
    return recomendacao


def aplicar_recomendacao(estado, maquinas, recomendacao):
    """Executa a ação sugerida pela IA. Retorna True se deu certo."""
    maquina = maquinas[recomendacao["indice"]]
    acao = recomendacao["acao"]

    if acao == "manutencao":
        estado["recursos"], iniciou = iniciar_manutencao(maquina, estado["recursos"])
        return iniciou
    if acao == "ligar":
        if maquina["ligada"]:
            return True
        return alternar_maquina(maquina)
    if acao == "desligar":
        if not maquina["ligada"]:
            return True
        return alternar_maquina(maquina)
    return False


def responder_recomendacao(estado, maquinas, aceitou):
    """Registra a decisão do jogador. Retorna True se a decisão foi correta."""
    recomendacao = estado["recomendacao"]
    if recomendacao is None:
        return None

    adequada = recomendacao["adequada"]
    correta = aceitou == adequada

    if correta:
        estado["decisoes_corretas"] = estado["decisoes_corretas"] + 1
    else:
        estado["decisoes_erradas"] = estado["decisoes_erradas"] + 1

    if not adequada:
        estado["ia_erros_recebidos"] = estado["ia_erros_recebidos"] + 1
        if not aceitou:
            estado["ia_erros_detectados"] = estado["ia_erros_detectados"] + 1

    if aceitou:
        aplicar_recomendacao(estado, maquinas, recomendacao)

    motivo = recomendacao["motivo"]
    if aceitou and adequada:
        definir_mensagem(estado, f"Boa decisão! A sugestão era adequada: {motivo}", "boa")
    elif aceitou and not adequada:
        definir_mensagem(estado, f"A IA errou e você aceitou: {motivo}", "ruim")
    elif not aceitou and not adequada:
        definir_mensagem(estado, f"Bem observado! A IA errou: {motivo}", "boa")
    else:
        definir_mensagem(estado, f"A sugestão era boa: {motivo}", "ruim")

    estado["recomendacao"] = None
    estado["tempo_para_recomendacao"] = float(INTERVALO_RECOMENDACAO)
    return correta


def atualizar_recomendacao(estado, maquinas, dt):
    """Cria novas sugestões e remove as que não foram respondidas a tempo."""
    recomendacao = estado["recomendacao"]

    if recomendacao is not None:
        recomendacao["tempo_restante"] = recomendacao["tempo_restante"] - dt
        if recomendacao["tempo_restante"] <= 0:
            estado["recomendacao"] = None
            estado["tempo_para_recomendacao"] = float(INTERVALO_RECOMENDACAO)
            definir_mensagem(estado, "A sugestão da IA expirou sem resposta.")
        return

    estado["tempo_para_recomendacao"] = estado["tempo_para_recomendacao"] - dt
    if estado["tempo_para_recomendacao"] <= 0:
        estado["recomendacao"] = gerar_recomendacao(maquinas, random.random())
        estado["tempo_para_recomendacao"] = float(INTERVALO_RECOMENDACAO)


def atualizar_partida(estado, maquinas, dt):
    """Avança a partida em dt segundos."""
    estado["tempo_restante"] = estado["tempo_restante"] - dt
    if estado["tempo_restante"] < 0:
        estado["tempo_restante"] = 0.0

    for maquina in maquinas:
        ficou_pronto = atualizar_maquina(maquina, dt, random.random())
        if ficou_pronto:
            if not registrar_produto(estado):
                definir_mensagem(estado, "Recursos insuficientes para concluir o produto!", "ruim")

    atualizar_recomendacao(estado, maquinas, dt)

    if estado["tempo_mensagem"] > 0:
        estado["tempo_mensagem"] = estado["tempo_mensagem"] - dt
        if estado["tempo_mensagem"] <= 0:
            estado["tempo_mensagem"] = 0.0
            estado["mensagem"] = ""


def recursos_minimos_necessarios(maquinas):
    """Recursos mínimos para ainda ser possível fabricar um produto."""
    for maquina in maquinas:
        if not maquina["quebrada"]:
            return CUSTO_PRODUTO
    return CUSTO_PRODUTO + CUSTO_CONSERTO


def verificar_fim(estado, maquinas):
    """Retorna 'vitoria', 'derrota_tempo', 'derrota_recursos' ou None."""
    if estado["produtos"] >= META_PRODUTOS:
        return "vitoria"
    if estado["tempo_restante"] <= 0:
        return "derrota_tempo"
    if estado["recursos"] < recursos_minimos_necessarios(maquinas):
        return "derrota_recursos"
    return None


def calcular_pontuacao(estado, resultado):
    """Calcula a pontuação final (nunca negativa)."""
    pontos = estado["produtos"] * PONTOS_POR_PRODUTO
    pontos = pontos + estado["decisoes_corretas"] * PONTOS_DECISAO_CORRETA
    pontos = pontos + estado["decisoes_erradas"] * PONTOS_DECISAO_ERRADA

    if resultado == "vitoria":
        pontos = pontos + estado["recursos"]
        pontos = pontos + int(estado["tempo_restante"]) * PONTOS_POR_SEGUNDO_RESTANTE

    if pontos < 0:
        pontos = 0
    return pontos
