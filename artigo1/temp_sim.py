import random
import math

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
                
        # Avança o tempo
        tempo += 1
        
    return melhor_estado, melhor_valor


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
    pesos_itens = [item["peso"] for item in itens]
    valores_itens = [item["valor"] for item in itens]
    capacidade_mochila = 10
    num_itens = len(pesos_itens)
    
    # Função de temperatura injetando os parâmetros
    funcao_T_do_tempo = criar_funcao_temperatura(
        t_inicial=1000, 
        t_final=0.01, 
        taxa_resfriamento=0.98, 
        iteracoes_por_temp=100
    )
    
    # Função de Têmpera Simulada
    print("Iniciando Têmpera Simulada com decaimento desacoplado...")
    melhor_solucao, valor_maximo = tempera_simulada(
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
