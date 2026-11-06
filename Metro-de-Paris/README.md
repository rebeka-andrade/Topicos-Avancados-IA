# Metrô de Paris — Busca A*

Implementação do problema do Metrô de Paris utilizando o algoritmo de Busca A* (A-Estrela).

O objetivo é encontrar o caminho de menor tempo entre duas estações, considerando as distâncias entre elas, a velocidade do trem de 30 km/h e o tempo adicional de 5 minutos para cada mudança de linha.

O problema utiliza uma rede com 14 estações e uma heurística baseada nas distâncias em linha reta.

**Disciplina:** Tópicos Avançados em Inteligência Artificial I  
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas — IFPE  
**Período:** 2026.2

## Algoritmo utilizado
Busca A* com função de avaliação f(n) = g(n) + h(n).
