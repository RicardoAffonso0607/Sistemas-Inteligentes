import random
import time
import matplotlib.pyplot as plt

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

    # Listas de histórico para os gráficos
    hist_geracoes = []
    hist_valores = []
    hist_tempo_execucao = []
    
    tempo_inicio = time.time() # Marca o início do processamento
    
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

        # Encontra o melhor da geração para salvar no histórico
        melhor_da_geracao = max(populacao, key=lambda ind: calcular_fitness(ind, itens, capacidade))
        valor_melhor = calcular_fitness(melhor_da_geracao, itens, capacidade)
        
        # Salvando os dados de iteração, valor e tempo
        hist_geracoes.append(geracao)
        hist_valores.append(valor_melhor)
        hist_tempo_execucao.append(time.time() - tempo_inicio)
        
        # Imprime o progresso a cada 20 gerações
        if geracao % 20 == 0:
            melhor_da_geracao = max(populacao, key=lambda ind: calcular_fitness(ind, itens, capacidade))
            valor_melhor = calcular_fitness(melhor_da_geracao, itens, capacidade)
            print(f"Geração {geracao:03d} | Melhor Valor: {valor_melhor}")

    # Retorna o melhor indivíduo absoluto da última geração
    melhor_individuo_final = max(populacao, key=lambda ind: calcular_fitness(ind, itens, capacidade))
    return melhor_individuo_final, hist_geracoes, hist_valores, hist_tempo_execucao

def plotar_graficos_ag(geracoes, valores, tempos_execucao):
    """
    Plota dois gráficos detalhando o desempenho do Algoritmo Genético.
    """
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    fig.suptitle('Análise de Desempenho - Algoritmo Genético', fontsize=16)

    # 1. Gráfico de Evolução do Valor da Mochila
    axs[0].plot(geracoes, valores, color='blue', linewidth=2)
    axs[0].set_title('Evolução do Melhor Valor Encontrado')
    axs[0].set_xlabel('Gerações (Iterações)')
    axs[0].set_ylabel('Valor Total na Mochila')
    axs[0].grid(True, linestyle='--', alpha=0.7)

    # 2. Gráfico de Iterações vs Tempo de Processamento
    axs[1].plot(tempos_execucao, geracoes, color='green', linewidth=2)
    axs[1].set_title('Gerações vs Tempo de Processamento')
    axs[1].set_xlabel('Tempo de Execução (segundos)')
    axs[1].set_ylabel('Gerações (Iterações)')
    axs[1].grid(True, linestyle='--', alpha=0.7)

    # Ajusta o espaçamento entre os gráficos
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()


if __name__ == "__main__":

    # Definição do Problema

    # Mochila com 20 itens
    itens = [
        {"peso": 14, "valor": 67},
        {"peso": 2, "valor": 95},
        {"peso": 18, "valor": 23},
        {"peso": 7, "valor": 80},
        {"peso": 11, "valor": 45},
        {"peso": 4, "valor": 88},
        {"peso": 20, "valor": 12},
        {"peso": 9, "valor": 55},
        {"peso": 15, "valor": 34},
        {"peso": 3, "valor": 90},
        {"peso": 13, "valor": 41},
        {"peso": 6, "valor": 72},
        {"peso": 17, "valor": 28},
        {"peso": 8, "valor": 60},
        {"peso": 1, "valor": 100},
        {"peso": 19, "valor": 18},
        {"peso": 5, "valor": 77},
        {"peso": 16, "valor": 31},
        {"peso": 10, "valor": 50},
        {"peso": 12, "valor": 48}
    ]
    capacidade_mochila = 104

    # Mochila com 100 itens
    #itens = [
    #    {"peso": 14, "valor": 28}, {"peso": 3, "valor": 92}, {"peso": 18, "valor": 15}, {"peso": 8, "valor": 64}, {"peso": 11, "valor": 45},
    #    {"peso": 19, "valor": 11}, {"peso": 5, "valor": 77}, {"peso": 13, "valor": 39}, {"peso": 2, "valor": 98}, {"peso": 16, "valor": 22},
    #    {"peso": 7, "valor": 81}, {"peso": 20, "valor": 10}, {"peso": 9, "valor": 56}, {"peso": 4, "valor": 88}, {"peso": 15, "valor": 31},
    #    {"peso": 1, "valor": 100}, {"peso": 12, "valor": 42}, {"peso": 17, "valor": 18}, {"peso": 6, "valor": 70}, {"peso": 10, "valor": 49},
    #    {"peso": 8, "valor": 60}, {"peso": 14, "valor": 35}, {"peso": 3, "valor": 95}, {"peso": 19, "valor": 14}, {"peso": 5, "valor": 75},
    #    {"peso": 11, "valor": 48}, {"peso": 2, "valor": 94}, {"peso": 16, "valor": 27}, {"peso": 7, "valor": 83}, {"peso": 18, "valor": 19},
    #    {"peso": 13, "valor": 38}, {"peso": 4, "valor": 85}, {"peso": 9, "valor": 52}, {"peso": 1, "valor": 99}, {"peso": 20, "valor": 12},
    #    {"peso": 15, "valor": 29}, {"peso": 6, "valor": 73}, {"peso": 10, "valor": 51}, {"peso": 12, "valor": 40}, {"peso": 17, "valor": 20},
    #    {"peso": 3, "valor": 89}, {"peso": 19, "valor": 16}, {"peso": 8, "valor": 62}, {"peso": 14, "valor": 32}, {"peso": 5, "valor": 78},
    #    {"peso": 2, "valor": 91}, {"peso": 11, "valor": 44}, {"peso": 16, "valor": 25}, {"peso": 7, "valor": 80}, {"peso": 18, "valor": 17},
    #    {"peso": 4, "valor": 87}, {"peso": 13, "valor": 41}, {"peso": 9, "valor": 55}, {"peso": 1, "valor": 96}, {"peso": 20, "valor": 13},
    #    {"peso": 15, "valor": 34}, {"peso": 6, "valor": 71}, {"peso": 10, "valor": 53}, {"peso": 12, "valor": 46}, {"peso": 17, "valor": 21},
    #    {"peso": 8, "valor": 65}, {"peso": 3, "valor": 90}, {"peso": 19, "valor": 15}, {"peso": 14, "valor": 37}, {"peso": 5, "valor": 74},
    #    {"peso": 2, "valor": 97}, {"peso": 11, "valor": 47}, {"peso": 16, "valor": 24}, {"peso": 7, "valor": 84}, {"peso": 18, "valor": 16},
    #    {"peso": 13, "valor": 36}, {"peso": 4, "valor": 86}, {"peso": 9, "valor": 58}, {"peso": 1, "valor": 98}, {"peso": 20, "valor": 11},
    #    {"peso": 15, "valor": 30}, {"peso": 6, "valor": 76}, {"peso": 10, "valor": 50}, {"peso": 12, "valor": 43}, {"peso": 17, "valor": 23},
    #    {"peso": 3, "valor": 93}, {"peso": 19, "valor": 12}, {"peso": 8, "valor": 61}, {"peso": 14, "valor": 33}, {"peso": 5, "valor": 79},
    #    {"peso": 2, "valor": 90}, {"peso": 11, "valor": 49}, {"peso": 16, "valor": 26}, {"peso": 7, "valor": 82}, {"peso": 18, "valor": 18},
    #    {"peso": 4, "valor": 89}, {"peso": 13, "valor": 40}, {"peso": 9, "valor": 54}, {"peso": 1, "valor": 95}, {"peso": 20, "valor": 14},
    #    {"peso": 15, "valor": 33}, {"peso": 6, "valor": 72}, {"peso": 10, "valor": 48}, {"peso": 12, "valor": 45}, {"peso": 17, "valor": 19}
    #]
    #capacidade_mochila = 532

    num_itens = len(itens)
    
    # Parâmetros de Controle
    tamanho_populacao = 100
    geracoes = 570
    taxa_crossover = 0.9
    taxa_mutacao = 0.05

    # Função que gera a população inicial
    print("Gerando população inicial...")
    populacao_inicial = criar_populacao(tamanho_populacao, num_itens)
    
    # Algoritmo genético
    print("Iniciando o Algoritmo Genético...\n")
    melhor_individuo, hist_geracoes, hist_valores, hist_tempo = algoritmo_genetico(
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

    print("\nGerando gráficos...")
    # Chama a função de plotagem com os dados rastreados
    plotar_graficos_ag(hist_geracoes, hist_valores, hist_tempo)