import alg_gen
import temp_sim
import time
import matplotlib.pyplot as plt

def plotar_comparacao(valores_sa, valores_ga, tempos_sa, tempos_ga, num_execucoes):
    """
    Plota Boxplots comparando os Valores Finais e os Tempos de Execução de ambos os algoritmos.
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f'Comparação Geral - Têmpera Simulada vs Algoritmo Genético\n({num_execucoes} Execuções independentes)', fontsize=14)

    # 1. Gráfico de Boxplot para os Valores Encontrados
    axs[0].boxplot([valores_sa, valores_ga], labels=['Têmpera Simulada', 'Algoritmo Genético'], patch_artist=True, boxprops=dict(facecolor="lightblue"))
    axs[0].set_title('Melhor Valor Encontrado (Fitness)')
    axs[0].set_ylabel('Valor Total na Mochila')
    axs[0].grid(axis='y', linestyle='--', alpha=0.7)

    # 2. Gráfico de Boxplot para o Tempo de Execução
    axs[1].boxplot([tempos_sa, tempos_ga], labels=['Têmpera Simulada', 'Algoritmo Genético'], patch_artist=True, boxprops=dict(facecolor="lightgreen"))
    axs[1].set_title('Tempo de Processamento')
    axs[1].set_ylabel('Tempo (segundos)')
    axs[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def executar_comparacao(itens, capacidade, num_execucoes=20):
    """
    Executa ambos os algoritmos N vezes e armazena os resultados para comparação.
    """
    print(f"Iniciando a bateria de {num_execucoes} testes para cada algoritmo...")
    print("Isso pode levar alguns segundos. Por favor, aguarde...\n")

    # Preparação dos dados para a Têmpera Simulada
    pesos_itens = [item["peso"] for item in itens]
    valores_itens = [item["valor"] for item in itens]
    
    # Listas para armazenar os resultados globais
    resultados_valor_sa = []
    resultados_tempo_sa = []
    
    resultados_valor_ga = []
    resultados_tempo_ga = []

    for i in range(num_execucoes):
        print(f"Executando Teste {i+1}/{num_execucoes}...")
        
        # ==========================================
        # 1. Execução da Têmpera Simulada
        # ==========================================
        funcao_T = temp_sim.criar_funcao_temperatura(1000, 0.01, 0.98, 100)
        
        inicio_sa = time.time()
        # Ignoramos os históricos individuais usando '_'
        _, melhor_valor_sa, _, _, _, _ = temp_sim.tempera_simulada(
            pesos_itens, valores_itens, capacidade, funcao_T
        )
        fim_sa = time.time()
        
        resultados_valor_sa.append(melhor_valor_sa)
        resultados_tempo_sa.append(fim_sa - inicio_sa)

        # ==========================================
        # 2. Execução do Algoritmo Genético
        # ==========================================
        populacao_inicial = alg_gen.criar_populacao(tamanho=100, num_itens=len(itens))
        
        inicio_ga = time.time()
        melhor_ind_ga, _, _, _ = alg_gen.algoritmo_genetico(
            populacao_inicial, geracoes=570, itens=itens, capacidade=capacidade, 
            taxa_crossover=0.8, taxa_mutacao=0.05
        )
        fim_ga = time.time()
        
        valor_ga = alg_gen.calcular_fitness(melhor_ind_ga, itens, capacidade)
        
        resultados_valor_ga.append(valor_ga)
        resultados_tempo_ga.append(fim_ga - inicio_ga)

    # Cálculos das médias para exibir no console
    media_valor_sa = sum(resultados_valor_sa) / num_execucoes
    media_tempo_sa = sum(resultados_tempo_sa) / num_execucoes
    
    media_valor_ga = sum(resultados_valor_ga) / num_execucoes
    media_tempo_ga = sum(resultados_tempo_ga) / num_execucoes

    print("\n==============================================")
    print("              RESUMO DOS RESULTADOS             ")
    print("==============================================")
    print("TÊMPERA SIMULADA:")
    print(f" -> Média de Valor Encontrado: {media_valor_sa:.2f}")
    print(f" -> Tempo Médio de Execução:   {media_tempo_sa:.4f} seg")
    print("\nALGORITMO GENÉTICO:")
    print(f" -> Média de Valor Encontrado: {media_valor_ga:.2f}")
    print(f" -> Tempo Médio de Execução:   {media_tempo_ga:.4f} seg")
    print("==============================================\n")

    # Plota os gráficos comparativos
    plotar_comparacao(resultados_valor_sa, resultados_valor_ga, resultados_tempo_sa, resultados_tempo_ga, num_execucoes)

# ==========================================
# Bloco de Execução Principal
# ==========================================
if __name__ == "__main__":
    # Mochila com 100 itens (A base de teste ideal para mostrar as diferenças entre os algoritmos)
    itens_teste = [
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
    capacidade_teste = 532

    # Chama a função de comparação com 20 execuções
    executar_comparacao(itens_teste, capacidade_teste, num_execucoes=20)