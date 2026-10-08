import random
import time
from itertools import combinations 

def calcular_coliciones(solucion):
    """
    retorna el numero de coliciones de una solucion, solo calculando
    las coliciones provocadas de manera diagonal
    """
    coliciones = 0
    n = len(solucion)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(solucion[i] - solucion[j]):
                coliciones += 1
    return coliciones


def generar_vecindario(solucion):
    """
    retorna una lista de tuplas de dos elementos, por cada elemto de la lista hay una tupla que tiene el vecino generado 
    y el indice de los elementos que se cambiaron para crear dicho vecino. [ ([vecino], (elementos_que_hicieron_swap))]
    Se usa el elemnto combinations de la libreria itertools para hacer el intercambio, este metodo genera todas las combinaciones
    posibles en una lista, en este caso las genera como pares
    """
    vecinos = []
    n = len(solucion)
    for i , j in combinations(range(n), 2):
        vecino = list(solucion)

        vecino[i], vecino[j] = vecino[j], vecino[i]

        vecinos.append((vecino, (i,j)))
    return vecinos



n = 8
max_iter = 500
tam_tabu = 15

solucion_actual = list(range(n))
random.shuffle(solucion_actual)

solucion_inicial = solucion_actual
mejor_solucion = solucion_inicial
menores_coliciones = calcular_coliciones(solucion_actual)

lista_tabu = []
num_movimientos = 0

inicio_tiempo = time.perf_counter()

while num_movimientos < max_iter and menores_coliciones > 0:
    vecinos = generar_vecindario(solucion_actual)
    mejor_vecino, mejor_movimiento , menor_colicion_vecino= None, None, float('inf')

    for vecino, movimiento in vecinos:
        coliciones = calcular_coliciones(vecino)

        if movimiento not in lista_tabu or coliciones < menores_coliciones:
            if coliciones < menor_colicion_vecino:
                menor_colicion_vecino = coliciones
                mejor_vecino = vecino
                mejor_movimiento = movimiento

    if mejor_vecino is None:
                break
    
    solucion_actual = mejor_vecino
    num_movimientos += 1

    if menor_colicion_vecino < menores_coliciones:
        mejor_solucion = mejor_vecino
        menores_coliciones = menor_colicion_vecino

    lista_tabu.append(mejor_movimiento)
    if len(lista_tabu) > tam_tabu:
        lista_tabu.pop(0)

tiempo_final = time.perf_counter()
tiempo_total = tiempo_final - inicio_tiempo

print(f"solucion inicial propuesta para el problema:    {solucion_inicial}")
print(f"Mejor solucion encontrada:  {mejor_solucion}")
print(f"Coliciones restantes:   {menores_coliciones} ")
if menores_coliciones == 0:
    print("se encontro una solucion optima")
else:
    print("No se encontro una solucion optima")


print("\n\t METRICAS DE RENDIMIENTO")
print(f"Movimientos totales:    {num_movimientos}")
print(f"Tiempo de ejecucion:    {tiempo_total:.5f} segundos")
