import random

def criar_individuo(num_itens):
    """
    Gera um indivíduo aleatório (lista de 0s e 1s)
    """
    return [random.randint(0, 1) for _ in range(num_itens)]

def criar_populacao(tamanho, num_itens):
    """
    Cria a população inicial
    """
    return [criar_individuo(num_itens) for _ in range(tamanho)]

def calcular_fitness(individuo, itens, capacidade):
    """
    Calcula a aptidão do indivíduo. Zera o valor se exceder o peso
    """
    peso_total = 0
    valor_total = 0
    
    for i in range(len(individuo)):
        if individuo[i] == 1:
            peso_total += itens[i]["peso"]
            valor_total += itens[i]["valor"]
            
    if peso_total > capacidade:
        return 0  # Indivíduo inválido (excedeu o peso)
        
    return valor_total

def selecao_torneio(populacao, itens, capacidade):
    """
    Seleciona pais através de torneio (escolhe o melhor entre 3 aleatórios)
    """
    competidores = random.sample(populacao, 3)
    # Usa uma função lambda para passar os parâmetros adicionais para calcular_fitness
    competidores.sort(key=lambda ind: calcular_fitness(ind, itens, capacidade), reverse=True)
    return competidores[0]

def crossover(pai1, pai2, taxa_crossover):
    """
    Realiza o cruzamento de um ponto entre dois pais
    """
    if random.random() < taxa_crossover:
        ponto_corte = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        return filho1, filho2
    return pai1.copy(), pai2.copy()

def mutacao(individuo, taxa_mutacao):
    """
    Aplica mutação invertendo genes com base na taxa de mutação
    """
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i] # Troca 0 por 1 e 1 por 0
    return individuo


def algoritmo_genetico(populacao, geracoes, itens, capacidade, taxa_crossover, taxa_mutacao):
    """
    Executa o algoritmo genético e retorna o melhor indivíduo encontrado
    """
    tamanho_populacao = len(populacao)
    
    for geracao in range(geracoes):
        nova_populacao = []
        
        # Elitismo: preserva o melhor da geração atual
        melhor_atual = max(populacao, key=lambda ind: calcular_fitness(ind, itens, capacidade))
        nova_populacao.append(melhor_atual)
        
        # Gera o restante da nova população
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, itens, capacidade)
            pai2 = selecao_torneio(populacao, itens, capacidade)
            
            filho1, filho2 = crossover(pai1, pai2, taxa_crossover)
            
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            
            nova_populacao.extend([filho1, filho2])
            
        # Garante o tamanho exato da população
        populacao = nova_populacao[:tamanho_populacao]
        
        # Imprime o progresso a cada 20 gerações
        if geracao % 20 == 0:
            melhor_da_geracao = max(populacao, key=lambda ind: calcular_fitness(ind, itens, capacidade))
            valor_melhor = calcular_fitness(melhor_da_geracao, itens, capacidade)
            print(f"Geração {geracao:03d} | Melhor Valor: {valor_melhor}")

    # Retorna o melhor indivíduo absoluto da última geração
    return max(populacao, key=lambda ind: calcular_fitness(ind, itens, capacidade))

if __name__ == "__main__":
    # Definição do Problema
    itens = [
        {"peso": 2, "valor": 10},
        {"peso": 3, "valor": 15},
        {"peso": 5, "valor": 40},
        {"peso": 7, "valor": 35},
        {"peso": 1, "valor": 5},
        {"peso": 4, "valor": 25},
        {"peso": 1, "valor": 15}
    ]
    capacidade_mochila = 10
    num_itens = len(itens)
    
    # Parâmetros de Controle
    tamanho_populacao = 50
    geracoes = 100
    taxa_crossover = 0.8
    taxa_mutacao = 0.1

    # Função que gera a população inicial
    print("Gerando população inicial...")
    populacao_inicial = criar_populacao(tamanho_populacao, num_itens)
    
    # Algoritmo genético
    print("Iniciando o Algoritmo Genético...\n")
    melhor_individuo = algoritmo_genetico(
        populacao=populacao_inicial,
        geracoes=geracoes,
        itens=itens,
        capacidade=capacidade_mochila,
        taxa_crossover=taxa_crossover,
        taxa_mutacao=taxa_mutacao
    )
    
    valor_final = calcular_fitness(melhor_individuo, itens, capacidade_mochila)
    peso_final = sum(itens[i]["peso"] for i in range(num_itens) if melhor_individuo[i] == 1)
    
    print("\n===============================")
    print("       RESULTADO FINAL         ")
    print("===============================")
    print(f"Melhor Cromossomo:   {melhor_individuo}")
    print(f"Valor Total Gerado:  {valor_final}")
    print(f"Capacidade Ocupada:  {peso_final} / {capacidade_mochila}")
    
    print("\nDetalhes dos itens selecionados:")
    for i in range(num_itens):
        if melhor_individuo[i] == 1:
            print(f" -> Item {i+1} (Peso: {itens[i]['peso']}, Valor: {itens[i]['valor']})")

