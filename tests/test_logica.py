"""Testes das regras do Factory Control."""


import os

from src.config import (
    RECURSOS_INICIAIS,
    TEMPO_PARTIDA,
    META_PRODUTOS,
    TEMPO_PRODUCAO,
    CUSTO_PRODUTO,
    CUSTO_MANUTENCAO,
    CUSTO_CONSERTO,
    DURACAO_MANUTENCAO,
    DESGASTE_SEGURO,
    LIMITE_DESGASTE_ALTO,
    TEMPO_RESPOSTA_IA,
    PONTOS_POR_PRODUTO,
)
from src.funcoes import (
    limitar_valor,
    criar_maquinas,
    criar_estado,
    status_maquina,
    alternar_maquina,
    iniciar_manutencao,
    chance_de_falha,
    atualizar_maquina,
    registrar_produto,
    opcoes_de_recomendacao,
    gerar_recomendacao,
    responder_recomendacao,
    atualizar_recomendacao,
    atualizar_partida,
    verificar_fim,
    calcular_pontuacao,
)
from src.dados import salvar_recorde, carregar_recorde

SEM_FALHA = 0.99
COM_FALHA = 0.0


def buscar_recomendacao(lista, acao, indice):
    """Procura na lista uma sugestão com a ação e a máquina informadas."""
    for recomendacao in lista:
        if recomendacao["acao"] == acao and recomendacao["indice"] == indice:
            return recomendacao
    return None


def test_limitar_valor():
    """Deve manter o valor dentro do intervalo."""
    assert limitar_valor(-5, 0, 100) == 0
    assert limitar_valor(150, 0, 100) == 100
    assert limitar_valor(50, 0, 100) == 50


def test_fabrica_comeca_com_tres_maquinas_desligadas():
    """A fábrica começa com 3 máquinas desligadas e sem desgaste."""
    maquinas = criar_maquinas()
    assert len(maquinas) == 3
    for maquina in maquinas:
        assert status_maquina(maquina) == "desligada"
        assert maquina["desgaste"] == 0


def test_estado_inicial():
    """A partida começa com os recursos e o tempo da configuração."""
    estado = criar_estado()
    assert estado["recursos"] == RECURSOS_INICIAIS
    assert estado["produtos"] == 0
    assert estado["tempo_restante"] == TEMPO_PARTIDA


def test_alternar_maquina_liga_e_desliga():
    """Clicar alterna entre ligada e desligada."""
    maquina = criar_maquinas(1)[0]
    assert alternar_maquina(maquina) is True
    assert maquina["ligada"] is True
    alternar_maquina(maquina)
    assert maquina["ligada"] is False


def test_maquina_quebrada_nao_liga():
    """Uma máquina quebrada não pode ser ligada."""
    maquina = criar_maquinas(1)[0]
    maquina["quebrada"] = True
    assert alternar_maquina(maquina) is False
    assert maquina["ligada"] is False


def test_maquina_ligada_produz_apos_tempo_de_producao():
    """Depois de TEMPO_PRODUCAO segundos ligada, sai um produto."""
    maquina = criar_maquinas(1)[0]
    alternar_maquina(maquina)
    pronto = False
    for segundo in range(TEMPO_PRODUCAO):
        pronto = atualizar_maquina(maquina, 1.0, SEM_FALHA)
    assert pronto is True


def test_maquina_desligada_nao_produz_nem_desgasta():
    """Máquina desligada fica parada."""
    maquina = criar_maquinas(1)[0]
    assert atualizar_maquina(maquina, 5.0, SEM_FALHA) is False
    assert maquina["progresso"] == 0
    assert maquina["desgaste"] == 0


def test_maquina_ligada_aumenta_desgaste():
    """O desgaste sobe enquanto a máquina trabalha."""
    maquina = criar_maquinas(1)[0]
    alternar_maquina(maquina)
    atualizar_maquina(maquina, 1.0, SEM_FALHA)
    assert maquina["desgaste"] > 0


def test_sem_risco_de_falha_com_desgaste_baixo():
    """Abaixo do desgaste seguro a chance de falha é zero."""
    assert chance_de_falha(DESGASTE_SEGURO, 1.0) == 0
    assert chance_de_falha(100, 1.0) > chance_de_falha(70, 1.0)
    assert chance_de_falha(70, 1.0) > 0


def test_maquina_pode_quebrar():
    """Com desgaste alto e sorteio baixo, a máquina quebra e para."""
    maquina = criar_maquinas(1)[0]
    alternar_maquina(maquina)
    maquina["desgaste"] = 90
    atualizar_maquina(maquina, 1.0, COM_FALHA)
    assert status_maquina(maquina) == "quebrada"


def test_falha_perde_produto_em_andamento():
    """Quando a máquina quebra, o produto em andamento é perdido."""
    maquina = criar_maquinas(1)[0]
    alternar_maquina(maquina)
    maquina["desgaste"] = 95
    maquina["progresso"] = 0.8
    atualizar_maquina(maquina, 1.0, COM_FALHA)
    assert maquina["progresso"] == 0


def test_conserto_consome_recursos_e_conserta():
    """Consertar custa CUSTO_CONSERTO, leva um tempo e zera o desgaste."""
    maquina = criar_maquinas(1)[0]
    maquina["quebrada"] = True
    maquina["desgaste"] = 80

    recursos, iniciou = iniciar_manutencao(maquina, 50)
    assert iniciou is True
    assert recursos == 50 - CUSTO_CONSERTO
    assert status_maquina(maquina) == "manutencao"

    atualizar_maquina(maquina, DURACAO_MANUTENCAO, SEM_FALHA)
    assert maquina["quebrada"] is False
    assert maquina["desgaste"] == 0
    assert maquina["ligada"] is True


def test_revisao_e_mais_barata_que_conserto():
    """Revisar antes de quebrar custa menos que consertar depois."""
    maquina = criar_maquinas(1)[0]
    maquina["desgaste"] = 70
    recursos, iniciou = iniciar_manutencao(maquina, 50)
    assert iniciou is True
    assert recursos == 50 - CUSTO_MANUTENCAO
    assert CUSTO_MANUTENCAO < CUSTO_CONSERTO


def test_manutencao_sem_recursos_nao_acontece():
    """Sem recursos suficientes a manutenção não começa."""
    maquina = criar_maquinas(1)[0]
    recursos, iniciou = iniciar_manutencao(maquina, CUSTO_MANUTENCAO - 1)
    assert iniciou is False
    assert recursos == CUSTO_MANUTENCAO - 1


def test_registrar_produto_consome_recursos():
    """Cada produto pronto custa CUSTO_PRODUTO recursos."""
    estado = criar_estado()
    assert registrar_produto(estado) is True
    assert estado["produtos"] == 1
    assert estado["recursos"] == RECURSOS_INICIAIS - CUSTO_PRODUTO


def test_registrar_produto_sem_recursos():
    """Sem recursos o produto não é contado."""
    estado = criar_estado()
    estado["recursos"] = CUSTO_PRODUTO - 1
    assert registrar_produto(estado) is False
    assert estado["produtos"] == 0


def test_atualizar_partida_reduz_tempo():
    """O cronômetro diminui conforme o tempo passa."""
    estado = criar_estado()
    maquinas = criar_maquinas()
    atualizar_partida(estado, maquinas, 1.0)
    assert estado["tempo_restante"] == TEMPO_PARTIDA - 1


def test_ia_recomenda_conserto_em_maquina_quebrada():
    """Manutenção em máquina quebrada é uma sugestão boa."""
    maquinas = criar_maquinas()
    maquinas[1]["quebrada"] = True
    boas, ruins = opcoes_de_recomendacao(maquinas)
    assert buscar_recomendacao(boas, "manutencao", 1) is not None


def test_ia_recomenda_revisao_com_desgaste_alto():
    """Desgaste acima do limite gera sugestão de manutenção boa."""
    maquinas = criar_maquinas()
    maquinas[2]["desgaste"] = LIMITE_DESGASTE_ALTO + 5
    boas, ruins = opcoes_de_recomendacao(maquinas)
    assert buscar_recomendacao(boas, "manutencao", 2) is not None


def test_ia_manutencao_em_maquina_nova_e_ruim():
    """Manutenção em máquina com pouco desgaste é uma sugestão ruim."""
    maquinas = criar_maquinas()
    boas, ruins = opcoes_de_recomendacao(maquinas)
    assert buscar_recomendacao(ruins, "manutencao", 0) is not None


def test_ia_desligar_maquina_saudavel_e_ruim():
    """Desligar uma máquina saudável que está produzindo é ruim."""
    maquinas = criar_maquinas()
    alternar_maquina(maquinas[0])
    boas, ruins = opcoes_de_recomendacao(maquinas)
    assert buscar_recomendacao(ruins, "desligar", 0) is not None


def test_ia_quando_erra_da_sugestao_ruim():
    """Com sorteio abaixo da chance de erro, a sugestão é ruim."""
    recomendacao = gerar_recomendacao(criar_maquinas(), 0.0)
    assert recomendacao["adequada"] is False


def test_ia_quando_acerta_da_sugestao_boa():
    """Com sorteio alto, a sugestão é boa."""
    recomendacao = gerar_recomendacao(criar_maquinas(), 0.99)
    assert recomendacao["adequada"] is True


def test_rejeitar_sugestao_ruim_e_decisao_correta():
    """Rejeitar uma sugestão ruim conta como acerto e não gasta recursos."""
    estado = criar_estado()
    maquinas = criar_maquinas()
    boas, ruins = opcoes_de_recomendacao(maquinas)
    estado["recomendacao"] = buscar_recomendacao(ruins, "manutencao", 0)

    assert responder_recomendacao(estado, maquinas, False) is True
    assert estado["decisoes_corretas"] == 1
    assert estado["ia_erros_detectados"] == 1
    assert estado["recursos"] == RECURSOS_INICIAIS
    assert estado["recomendacao"] is None


def test_aceitar_sugestao_ruim_e_decisao_errada():
    """Aceitar manutenção desnecessária conta erro e gasta recursos."""
    estado = criar_estado()
    maquinas = criar_maquinas()
    boas, ruins = opcoes_de_recomendacao(maquinas)
    estado["recomendacao"] = buscar_recomendacao(ruins, "manutencao", 0)

    assert responder_recomendacao(estado, maquinas, True) is False
    assert estado["decisoes_erradas"] == 1
    assert estado["recursos"] == RECURSOS_INICIAIS - CUSTO_MANUTENCAO


def test_aceitar_sugestao_boa_e_decisao_correta():
    """Aceitar ligar uma máquina parada é acerto e liga a máquina."""
    estado = criar_estado()
    maquinas = criar_maquinas()
    boas, ruins = opcoes_de_recomendacao(maquinas)
    estado["recomendacao"] = buscar_recomendacao(boas, "ligar", 2)

    assert responder_recomendacao(estado, maquinas, True) is True
    assert maquinas[2]["ligada"] is True


def test_sugestao_expira_sem_resposta():
    """Se o jogador não responder a tempo, a sugestão some."""
    estado = criar_estado()
    maquinas = criar_maquinas()
    estado["recomendacao"] = gerar_recomendacao(maquinas, 0.99)
    atualizar_recomendacao(estado, maquinas, TEMPO_RESPOSTA_IA + 1)
    assert estado["recomendacao"] is None


def test_vitoria_ao_atingir_meta():
    """Atingir a meta de produtos é vitória."""
    estado = criar_estado()
    estado["produtos"] = META_PRODUTOS
    assert verificar_fim(estado, criar_maquinas()) == "vitoria"


def test_derrota_quando_tempo_acaba():
    """Tempo zerado sem a meta é derrota."""
    estado = criar_estado()
    estado["tempo_restante"] = 0
    assert verificar_fim(estado, criar_maquinas()) == "derrota_tempo"


def test_derrota_sem_recursos():
    """Sem recursos para produzir é derrota."""
    estado = criar_estado()
    estado["recursos"] = CUSTO_PRODUTO - 1
    assert verificar_fim(estado, criar_maquinas()) == "derrota_recursos"


def test_derrota_todas_quebradas_sem_recursos_para_consertar():
    """Com todas quebradas, precisa ter recurso para consertar e produzir."""
    estado = criar_estado()
    maquinas = criar_maquinas()
    for maquina in maquinas:
        maquina["quebrada"] = True
    estado["recursos"] = CUSTO_CONSERTO
    assert verificar_fim(estado, maquinas) == "derrota_recursos"


def test_partida_em_andamento():
    """No início não há vitória nem derrota."""
    assert verificar_fim(criar_estado(), criar_maquinas()) is None


def test_pontuacao_conta_produtos_e_decisoes():
    """Pontuação soma produtos e decisões, sem bônus na derrota."""
    estado = criar_estado()
    estado["produtos"] = 3
    estado["decisoes_corretas"] = 2
    estado["decisoes_erradas"] = 1
    esperado = 3 * PONTOS_POR_PRODUTO + 2 * 50 - 30
    assert calcular_pontuacao(estado, "derrota_tempo") == esperado


def test_pontuacao_vitoria_tem_bonus():
    """Na vitória, recursos e tempo restantes viram bônus."""
    estado = criar_estado()
    estado["produtos"] = META_PRODUTOS
    assert calcular_pontuacao(estado, "vitoria") > calcular_pontuacao(estado, "derrota_tempo")


def test_pontuacao_nunca_negativa():
    """Muitas decisões erradas não deixam a pontuação negativa."""
    estado = criar_estado()
    estado["decisoes_erradas"] = 10
    assert calcular_pontuacao(estado, "derrota_tempo") == 0


def test_salvar_e_carregar_recorde():
    """O recorde salvo deve ser lido de volta."""
    caminho = "tests/recorde_teste.txt"
    salvar_recorde(caminho, 1234)
    assert carregar_recorde(caminho) == 1234
    os.remove(caminho)


def test_carregar_recorde_inexistente():
    """Sem arquivo, o recorde é 0."""
    assert carregar_recorde("tests/arquivo_que_nao_existe.txt") == 0
