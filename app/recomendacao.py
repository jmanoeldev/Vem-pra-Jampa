from app.utils import ler_pontos


# Tabelaa de custos aceitos por orçamento
# Se o usuário marca 'alto', entao o algoritmo ele e todos os orçamentos abaixo dele
CUSTO_ACEITO = {
    'alto':  ['baixo', 'medio', 'alto'],
    'medio': ['baixo', 'medio'],
    'baixo': ['baixo'],
}

def recomendar_pontos(objetivo, companhia, periodo, orcamento):
    # Carrega todos os pontos turisticos do csv
    pontos = ler_pontos()
    resultado = []

    # monta o conjunto de custos aceitos de acordo com o orcamento
    custos_aceitos = set()
    # o set nao vai deixar repetir se o usuario marca dois orcamentos, por exemplo:
    # medio:[baixo, medio]
    # baixo:[baixo]
    for o in orcamento:                    #se o existe no dic, retorna no valor, se nao retorna []
        custos_aceitos.update(CUSTO_ACEITO.get(o, [])) #update: adiciona os valores de uma vez dentro do set

    for ponto in pontos:

        # percorre cada custo do ponto e ve se esta dentro do que o orcamento aceita
        # basta um ser verdade para o 'any' retornar True
        custo_ok = any(c in custos_aceitos for c in ponto['custo'])
        if not custo_ok:
            continue # o ponto nao passou pelo filtro: pula para o proximo

        pontuacao = 0

        # criterio principal. se bateu, a pontuacao vale mais
        if ponto['categoria'] in objetivo:
            pontuacao += 3

        # percorre as opcoes do usuario e pergunta se esta dentro do ponto
        # c=casal in ['casal','familia','amigos']
        if any(c in ponto['publico'] for c in companhia):
            pontuacao += 1

        #percorre cada periodo do usuario e pergunta se ta dentro do ponto
        if any(p in ponto['periodo'] for p in periodo):
            pontuacao += 1

        # so adiciona ao resultado se tiver pelo menos 1 ponto
        if pontuacao > 0:
            ponto['pontuacao'] = pontuacao
            resultado.append(ponto)

    # ordena da maior para menor pontuacao
    # key: diz que deve ser ordenada pela pontuacao
    # lambda: funcao pequena pra retornar p['pontuacao']
    resultado.sort(key=lambda p: p['pontuacao'], reverse=True)

    #retorna os 5 primeiros apenas
    return resultado[:5]