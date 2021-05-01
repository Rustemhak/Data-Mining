from random import randint, randrange
from time import sleep


class X:
    value = 0
    element = 0
    position = 0

    def __init__(self, position, element, value):
        self.position = position
        self.element = element
        self.value = value


def generate(n, b, e):
    a = []
    for i in range(n):
        a.append(randint(b, e))
    return a


def get_dict(a):
    d = {}
    for x in a:
        if x in d.keys():
            d[x] += 1
        else:
            d[x] = 1
    return d


def generate_variables(cnt, b, e):
    var = []
    for i in range(cnt):
        var.append(randint(b, e))
    var.sort()
    return var


def calc_2_moment_with_AMS(var, a, n):
    for x in var:
        for i in range(x.position + 1, n):
            if a[i] == x.element:
                x.value += 1
    x_list = []
    for x in var:
        x_list.append(n * (2 * x.value - 1))
    return sum(x_list) / len(x_list)


if __name__ == '__main__':
    amount = 1000000
    begin = 0
    end = 1000
    count1_var = 100
    count2_var = 500
    cnt_try = 0
    while True:
        cnt_try += 1
        print('Attempt number:', cnt_try)
        generated_list = generate(amount, begin, end)
        # print(get_dict(generated_list))
        map_of_gen = get_dict(generated_list)
        print('0-th moment', len(map_of_gen))
        print('1-th moment', sum(map_of_gen.values()))
        moment2 = 0
        for v in map_of_gen.values():
            moment2 += v * v
        print('2-th moment  without AMS algorithm', moment2)
        x_list = []
        gen_var1 = generate_variables(count1_var, begin, amount)
        for pos in gen_var1:
            x_list.append(X(pos, generated_list[pos], 1))
        print('2-th with AMS algorithm 100 variables', calc_2_moment_with_AMS(x_list, generated_list, amount))
        x_list = []
        gen_var2 = generate_variables(count2_var, begin, amount)
        for pos in gen_var2:
            x_list.append(X(pos, generated_list[pos], 1))
        print('2-th with AMS algorithm 500 variables', calc_2_moment_with_AMS(x_list, generated_list, amount))
        sleep(0.2)
