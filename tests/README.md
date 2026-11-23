# Testes

Esta pasta contem testes automatizados do projeto.

## Arquivos

- `test_logica.py`: valida as regras do jogo em `src/funcoes.py` e o recorde em `src/dados.py`.

## Como executar

```bash
python -m pytest
```

## Boas praticas

- Crie testes para toda regra de pontuacao, vidas e condicoes de fim de jogo.
- Prefira funcoes pequenas e testaveis no modulo `src/funcoes.py`.
