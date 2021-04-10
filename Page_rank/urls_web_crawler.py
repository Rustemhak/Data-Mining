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

            if not (pair in relation):
                relation.append(pair)
                if not (inner_link in links):
                    links.append(inner_link)
                depth += 1
                if depth < 5:
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
url = 'https://refactoring.guru/design-patterns/iterator'
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
transition_matrix = []
for i in range(size_matrix):
    transition_matrix.append([0.0] * size_matrix)
for i in range(size_matrix):
    count_1 = adjacency_matrix[i].count(1)
    print(count_1)
    for j in range(size_matrix):
        if count_1 > 0 and adjacency_matrix[i][j] > 0:
            transition_matrix[i][j] = float(adjacency_matrix[i][j] / count_1)
for i in range(size_matrix):
    print('сумма', i, '-й', sum(transition_matrix[i]))
# print(transition_matrix)

vector = [float(1 / size_matrix)] * size_matrix

beta = 0.8
e_matrix = [float(0.2 / float(size_matrix))] * size_matrix
print('начальный вектор', sum(vector))
for i in range(100):
    s1 = multiply_vector_matrix(vector, transition_matrix, beta)
    vector = sum_vector(s1, e_matrix)

    print(i, '-я итерация', 5 * sum(vector))

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
f = open('transition_matrix.csv','w')
for i in range(size_matrix):
    for j in range(size_matrix):
        f.write(str(transition_matrix[i][j]) + ',')
    f.write('\n')
f.close()

