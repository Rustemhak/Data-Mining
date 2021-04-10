import requests
from bs4 import BeautifulSoup
import re
from decimal import Decimal
import time
from graphviz import Digraph

header = 'https://refactoring.guru'
relation = []
links = []


def crawl(url, depth):
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, features="lxml")

    for link in soup.find_all('a'):
        inner_link = str(link.get('href'))
        if re.fullmatch('/\S*', inner_link):
            inner_link = header + inner_link
        if re.fullmatch(header + '\S*', inner_link):
            pair = [url, inner_link]
            if len(links) < 20:
                if not (pair in relation):
                    relation.append(pair)
                    if not (inner_link in links):
                        links.append(inner_link)
                    depth += 1
                    if depth < 6:
                        crawl(inner_link, depth)


def multiply_vector_matrix(v, G, beta):
    result = []

    for row in range(len(v)):
        total = 0
        for col in range(len(v)):
            total += beta * float(G[col][row] * v[col])
        result.append(total)
    return result


def multiply_num_vector(k, v):
    for index in range(len(v)):
        v[index] *= k
    return v


def sum_vector(v1, v2):
    v = [0.0] * len(v1)
    for k in range(len(v1)):
        v[k] = float(v1[k] + v2[k])
    return v


startTime = time.time()
url = 'https://refactoring.guru'
links.append(url)
depth = 1
crawl(url, depth)
print(relation)
print(links)
adjacency_matrix = []
size_matrix = len(links)
for i in range(size_matrix):
    adjacency_matrix.append([0] * size_matrix)
for rel in relation:
    id_input = links.index(rel[0])
    id_output = links.index(rel[1])
    adjacency_matrix[id_input][id_output] = 1

# print(adjacency_matrix)
#
# adjacency_matrix = [[0, 1, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0]]
# size_matrix = 4
not_dead_end = []
for i in range(size_matrix):
    count_1 = adjacency_matrix[i].count(1)
    print(count_1)
    if count_1 > 0:
        # transition_matrix[i][j] = float(adjacency_matrix[i][j] / count_1)
        not_dead_end.append(i)
size_not_dead_end = len(not_dead_end)
print(not_dead_end,
      'не дед энды')
transition_matrix = []
# indexes of not dead end keep in  not_dead_end
for i in range(size_not_dead_end):
    transition_matrix.append([0.0] * size_not_dead_end)
print(size_not_dead_end)
for row in not_dead_end:
    count_1 = 0
    for col in not_dead_end:
        if adjacency_matrix[row][col] == 1:
            count_1 += 1
    for col in not_dead_end:
        if adjacency_matrix[row][col] == 1:
            transition_matrix[not_dead_end.index(row)][not_dead_end.index(col)] = float(1 / count_1)

for i in range(size_not_dead_end):
    print('сумма', i, '-й', sum(transition_matrix[i]))
# print(transition_matrix)

vector = [float(1 / size_not_dead_end)] * size_not_dead_end

beta = 0.8
e_matrix = [float(0.2 / float(size_not_dead_end))] * size_not_dead_end
print('начальный вектор', sum(vector))
for i in range(30):
    s1 = multiply_vector_matrix(vector, transition_matrix, beta)
    vector = sum_vector(s1, e_matrix)
    print(i, '-я итерация', sum(vector))
    vector_with_dead_end = [0.0] * size_matrix
    for j in not_dead_end:
        vector_with_dead_end[j] = vector[not_dead_end.index(j)]
    for j in range(size_matrix):
        if not (j in not_dead_end):
            for k in not_dead_end:
                if adjacency_matrix[k][j] == 1:
                    vector_with_dead_end[j] += float(1 / sum(adjacency_matrix[k])) * vector_with_dead_end[k]
    print('сумма вектор с дед эндами', sum(vector_with_dead_end))
    print('сумма вектор без дед эндов', sum(vector))

endTime = time.time()
totalTime = endTime - startTime
print("Время, затраченное на выполнение данного кода = ", totalTime)
print(vector)
max_rank = max(vector)
print('Максимальный ранк ', max_rank)
max_i = 0
for i in range(len(vector)):
    if vector[i] == max_rank:
        max_i = i
        break
print('Имеет страница ', links[max_i])

print('Сумма элементов вектора', sum(vector))

dot = Digraph(comment='Graph of links')
for i in range(size_matrix):
    dot.node(str(i), str(i))
for i in range(size_matrix):
    for j in range(size_matrix):
        if adjacency_matrix[i][j] == 1:
            dot.edge(str(i), str(j))
# print(dot.source)
dot.render('output/graph.gv', view=True)
f = open('transition_matrix.csv', 'w')
for i in range(size_not_dead_end):
    for j in range(size_not_dead_end):
        f.write(str(transition_matrix[i][j]) + ',')
    f.write('\n')
f.close()
