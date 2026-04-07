import random
import math
import time
import matplotlib.pyplot as plt

def avalia_mochila(estado, pesos, valores, capacidade):
    """
    Calcula o valor da mochila
    Retorna 0 se exceder a capacidade (penalidade)
    """
    peso_total = sum(estado[i] * pesos[i] for i in range(len(estado)))
    valor_total = sum(estado[i] * valores[i] for i in range(len(estado)))
    
    if peso_total > capacidade:
        return 0
    
    return valor_total

def gera_vizinho(estado):
    """
    Gera um vizinho invertendo o estado de um item aleatório
    """
    vizinho = estado.copy()
    idx = random.randint(0, len(estado) - 1)
    vizinho[idx] = 1 - vizinho[idx]
    return vizinho

def criar_funcao_temperatura(t_inicial, t_final, taxa_resfriamento, iteracoes_por_temp):
    """
    Gera uma função de temperatura pelo tempo
    Retorna uma função (callable) T(tempo)
    """
    def T(tempo):
        # Descobre em qual ciclo está
        ciclo = tempo // iteracoes_por_temp
        
        # Calcula a temperatura daquele ciclo específico
        temperatura_atual = t_inicial * (taxa_resfriamento ** ciclo)
        
        # Se atingiu a temperatura final de parada, retorna None para sinalizar o fim
        if temperatura_atual <= t_final:
            return None
            
        return temperatura_atual
        
    return T

def tempera_simulada(pesos, valores, capacidade, funcao_temperatura):
    """
    Têmpera Simulada refatorada para receber a função de resfriamento T(t)
    """
    n = len(pesos)
    estado_atual = [0] * n 
    melhor_estado = estado_atual.copy()
    
    valor_atual = avalia_mochila(estado_atual, pesos, valores, capacidade)
    melhor_valor = valor_atual
    
    tempo = 0 # O tempo (iteração absoluta) começa em 0

    # Lista de histórico para montar os gráficos
    hist_iteracoes = []
    hist_temperaturas = []
    hist_valores = []
    hist_tempo_execucao = []

    tempo_inicio = time.time() # Marca o início do processamento
    
    while True:
        # Pede para a função gerada qual é a temperatura no tempo 't'
        T = funcao_temperatura(tempo)
        
        # Critério de parada: a função T(t) retorna None quando passa do t_final
        if T is None:
            break
            
        vizinho = gera_vizinho(estado_atual)
        valor_vizinho = avalia_mochila(vizinho, pesos, valores, capacidade)
        
        delta = valor_vizinho - valor_atual
        
        # Maximização: aceita se for melhor
        if delta > 0:
            estado_atual = vizinho
            valor_atual = valor_vizinho
            
            if valor_atual > melhor_valor:
                melhor_estado = estado_atual.copy()
                melhor_valor = valor_atual
        else:
            # Aceitação probabilística de soluções piores dependente de T
            probabilidade = math.exp(delta / T)
            if random.random() < probabilidade:
                estado_atual = vizinho
                valor_atual = valor_vizinho

        # Salva o estado atual no histórico para os gráficos
        hist_iteracoes.append(tempo)
        hist_temperaturas.append(T)
        hist_valores.append(melhor_valor) # Rastreando a melhor solução encontrada até o momento
        hist_tempo_execucao.append(time.time() - tempo_inicio)
                
        # Avança o tempo
        tempo += 1
        
    return melhor_estado, melhor_valor, hist_iteracoes, hist_temperaturas, hist_valores, hist_tempo_execucao

def plotar_graficos_tempera(iteracoes, temperaturas, valores, tempos_execucao):
    """
    Plota três gráficos detalhando o desempenho da Têmpera Simulada.
    """
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle('Análise de Desempenho - Têmpera Simulada', fontsize=16)

    # 1. Gráfico de Temperatura por Iterações
    axs[0].plot(iteracoes, temperaturas, color='red', linewidth=2)
    axs[0].set_title('Decaimento da Temperatura')
    axs[0].set_xlabel('Iterações (t)')
    axs[0].set_ylabel('Temperatura (T)')
    axs[0].grid(True, linestyle='--', alpha=0.7)

    # 2. Gráfico de Evolução do Valor da Mochila
    axs[1].plot(iteracoes, valores, color='blue', linewidth=2)
    axs[1].set_title('Evolução do Melhor Valor Encontrado')
    axs[1].set_xlabel('Iterações (t)')
    axs[1].set_ylabel('Valor Total na Mochila')
    axs[1].grid(True, linestyle='--', alpha=0.7)

    # 3. Gráfico de Iterações vs Tempo de Processamento
    axs[2].plot(tempos_execucao, iteracoes, color='green', linewidth=2)
    axs[2].set_title('Iterações vs Tempo de Processamento')
    axs[2].set_xlabel('Tempo de Execução (segundos)')
    axs[2].set_ylabel('Iterações (t)')
    axs[2].grid(True, linestyle='--', alpha=0.7)

    # Ajusta o espaçamento entre os gráficos
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()


if __name__ == "__main__":

    # Definição do Problema

    # Mochila com 20 itens
    #itens = [
    #    {"peso": 14, "valor": 67},
    #    {"peso": 2, "valor": 95},
    #    {"peso": 18, "valor": 23},
    #    {"peso": 7, "valor": 80},
    #    {"peso": 11, "valor": 45},
    #    {"peso": 4, "valor": 88},
    #    {"peso": 20, "valor": 12},
    #    {"peso": 9, "valor": 55},
    #    {"peso": 15, "valor": 34},
    #    {"peso": 3, "valor": 90},
    #    {"peso": 13, "valor": 41},
    #    {"peso": 6, "valor": 72},
    #    {"peso": 17, "valor": 28},
    #    {"peso": 8, "valor": 60},
    #    {"peso": 1, "valor": 100},
    #    {"peso": 19, "valor": 18},
    #    {"peso": 5, "valor": 77},
    #    {"peso": 16, "valor": 31},
    #    {"peso": 10, "valor": 50},
    #    {"peso": 12, "valor": 48}
    #]
    #capacidade_mochila = 104

    # Mochila com 100 itens
    itens = [
        {"peso": 14, "valor": 28}, {"peso": 3, "valor": 92}, {"peso": 18, "valor": 15}, {"peso": 8, "valor": 64}, {"peso": 11, "valor": 45},
        {"peso": 19, "valor": 11}, {"peso": 5, "valor": 77}, {"peso": 13, "valor": 39}, {"peso": 2, "valor": 98}, {"peso": 16, "valor": 22},
        {"peso": 7, "valor": 81}, {"peso": 20, "valor": 10}, {"peso": 9, "valor": 56}, {"peso": 4, "valor": 88}, {"peso": 15, "valor": 31},
        {"peso": 1, "valor": 100}, {"peso": 12, "valor": 42}, {"peso": 17, "valor": 18}, {"peso": 6, "valor": 70}, {"peso": 10, "valor": 49},
        {"peso": 8, "valor": 60}, {"peso": 14, "valor": 35}, {"peso": 3, "valor": 95}, {"peso": 19, "valor": 14}, {"peso": 5, "valor": 75},
        {"peso": 11, "valor": 48}, {"peso": 2, "valor": 94}, {"peso": 16, "valor": 27}, {"peso": 7, "valor": 83}, {"peso": 18, "valor": 19},
        {"peso": 13, "valor": 38}, {"peso": 4, "valor": 85}, {"peso": 9, "valor": 52}, {"peso": 1, "valor": 99}, {"peso": 20, "valor": 12},
        {"peso": 15, "valor": 29}, {"peso": 6, "valor": 73}, {"peso": 10, "valor": 51}, {"peso": 12, "valor": 40}, {"peso": 17, "valor": 20},
        {"peso": 3, "valor": 89}, {"peso": 19, "valor": 16}, {"peso": 8, "valor": 62}, {"peso": 14, "valor": 32}, {"peso": 5, "valor": 78},
        {"peso": 2, "valor": 91}, {"peso": 11, "valor": 44}, {"peso": 16, "valor": 25}, {"peso": 7, "valor": 80}, {"peso": 18, "valor": 17},
        {"peso": 4, "valor": 87}, {"peso": 13, "valor": 41}, {"peso": 9, "valor": 55}, {"peso": 1, "valor": 96}, {"peso": 20, "valor": 13},
        {"peso": 15, "valor": 34}, {"peso": 6, "valor": 71}, {"peso": 10, "valor": 53}, {"peso": 12, "valor": 46}, {"peso": 17, "valor": 21},
        {"peso": 8, "valor": 65}, {"peso": 3, "valor": 90}, {"peso": 19, "valor": 15}, {"peso": 14, "valor": 37}, {"peso": 5, "valor": 74},
        {"peso": 2, "valor": 97}, {"peso": 11, "valor": 47}, {"peso": 16, "valor": 24}, {"peso": 7, "valor": 84}, {"peso": 18, "valor": 16},
        {"peso": 13, "valor": 36}, {"peso": 4, "valor": 86}, {"peso": 9, "valor": 58}, {"peso": 1, "valor": 98}, {"peso": 20, "valor": 11},
        {"peso": 15, "valor": 30}, {"peso": 6, "valor": 76}, {"peso": 10, "valor": 50}, {"peso": 12, "valor": 43}, {"peso": 17, "valor": 23},
        {"peso": 3, "valor": 93}, {"peso": 19, "valor": 12}, {"peso": 8, "valor": 61}, {"peso": 14, "valor": 33}, {"peso": 5, "valor": 79},
        {"peso": 2, "valor": 90}, {"peso": 11, "valor": 49}, {"peso": 16, "valor": 26}, {"peso": 7, "valor": 82}, {"peso": 18, "valor": 18},
        {"peso": 4, "valor": 89}, {"peso": 13, "valor": 40}, {"peso": 9, "valor": 54}, {"peso": 1, "valor": 95}, {"peso": 20, "valor": 14},
        {"peso": 15, "valor": 33}, {"peso": 6, "valor": 72}, {"peso": 10, "valor": 48}, {"peso": 12, "valor": 45}, {"peso": 17, "valor": 19}
    ]
    capacidade_mochila = 532

    pesos_itens = [item["peso"] for item in itens]
    valores_itens = [item["valor"] for item in itens]
    num_itens = len(pesos_itens)
    
    # Função de temperatura injetando os parâmetros
    funcao_T_do_tempo = criar_funcao_temperatura(
        t_inicial=1000, 
        t_final=0.01, 
        taxa_resfriamento=0.98, 
        iteracoes_por_temp=100
    )
    
    # Função de Têmpera Simulada
    print("Iniciando Têmpera Simulada...")
    (melhor_solucao, valor_maximo,
     iteracoes, temperaturas, valores, tempos_execucao) = tempera_simulada(
        pesos=pesos_itens, 
        valores=valores_itens, 
        capacidade=capacidade_mochila,
        funcao_temperatura=funcao_T_do_tempo # Passagem da função como argumento
    )
    
    peso_final = sum(melhor_solucao[i] * pesos_itens[i] for i in range(len(melhor_solucao)))
    
    print("\n===============================")
    print("       RESULTADO FINAL         ")
    print("===============================")
    print(f"Melhor combinação: {melhor_solucao}")
    print(f"Valor Total Gerado: {valor_maximo}")
    print(f"Capacidade Ocupada: {peso_final} / {capacidade_mochila}")

    print("\nDetalhes dos itens selecionados:")
    for i in range(num_itens):
        if melhor_solucao[i] == 1:
            print(f" -> Item {i+1} (Peso: {itens[i]['peso']}, Valor: {itens[i]['valor']})")

    print("\nGerando gráficos...")
    # Chama a função de plotagem
    plotar_graficos_tempera(iteracoes, temperaturas, valores, tempos_execucao)
