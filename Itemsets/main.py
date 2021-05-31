import pandas
from itertools import combinations

support_s = 800


def get_buckets():
    df = pandas.read_csv('Groceries_dataset.csv')
    customers_id = sorted(set(df['Member_number']))
    products = sorted(set(df['itemDescription']))
    transactions = dict.fromkeys(customers_id)
    for customer in customers_id:
        transactions[customer] = list(df[df.Member_number == customer]['itemDescription'])
    return transactions, products


def find_frequent_itemsets():
    transactions, products = get_buckets()
    singletons, unsupported_items = get_frequent_singleton(transactions, products, support_s)
    doubletons = list(set(get_frequent_doubleton(transactions, products, support_s, unsupported_items)))
    return singletons, doubletons


def get_frequent_singleton(transactions, products, support_s):
    table = dict.fromkeys(products, 0)
    unsupported_items = []
    for prod in transactions.values():
        for p in prod:
            table[p] += 1
    for k, v in table.items():
        if v >= support_s:
            pass
        else:
            unsupported_items.append(k)
    # print('Продукты, которые не прошли уровень поддержки: ', *unsupported_items)
    singletons = []
    for p in products:
        if p not in unsupported_items:
            singletons.append(p)
    return singletons, unsupported_items


def get_frequent_doubleton(transactions, products, support_s, unsupported_items):
    doubletons = []
    for t in transactions.values():
        for comb in combinations(t, 2):
            doubletons.append((products.index(comb[0]) + 1, products.index(comb[1]) + 1))
    k = len(products)

    group_first = [[] for i in range(k)]
    for pair in doubletons:
        group_first[(pair[0] + pair[1]) % k].append(pair)
    unsupported_pair_first = []
    for group in group_first:
        if len(group) < support_s:
            for p in group:
                unsupported_pair_first.append(p)
    group_second = [[] for i in range(k)]
    for pair in doubletons:
        group_second[(pair[0] + 2 * pair[1]) % k].append(pair)
    for i in range(len(group_second)):
        for p in unsupported_pair_first:
            if p in group_second[i]:
                group_second[i].remove(p)
    for group in group_second:
        if len(group) < support_s:
            group_second.remove(group)
    frequent_doubletons = []
    for g in group_second:
        for p in g:
            item1 = products[p[0] - 1]
            item2 = products[p[1] - 1]
            if item1 not in unsupported_items and item2 not in unsupported_items and item1 != item2:
                frequent_doubletons.append((item1, item2))
    return frequent_doubletons


frequent_itemsets = find_frequent_itemsets()
singletons = frequent_itemsets[0]
doubletons = frequent_itemsets[1]
print('Level of support = ', support_s)
print('Frequent singletons: ', singletons)
print('Frequent doubletons: ', doubletons)
