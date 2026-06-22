from app.utils import ler_pontos

def recomendar(objetivos, companhias, periodos, orcamentos): #recebe quatro listas dos checkboxes, se o usuario nao marcou nada, elas chegam vazias
    todos_pontos = ler_pontos()
    resultado = []

    criterios = [
        (objetivos, 'categoria'),
        (companhias, 'publico'),
        (periodos, 'periodo'),
        (orcamentos, 'custo'),
    ]

    for ponto in todos_pontos:
        score = 0
        grupos_ativos = 0

        for escolhas, coluna in criterios:
            if not escolhas:
                continue

            grupos_ativos += 1

            for escolha in escolhas:
                if escolha in ponto[coluna]:
                    score += 1
                    break

        if grupos_ativos == 0 or score == 0:
            continue

        score_normalizado = score / grupos_ativos
        resultado.append((score_normalizado, ponto))

    resultado.sort(key=lambda x: x[0], reverse=True)

    return [ponto for score, ponto in resultado[:8]]