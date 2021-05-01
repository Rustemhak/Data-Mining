from math import log, e
from zlib import adler32, crc32


def generate_cbf(f, p):
    words, m = get_amount_words(f)
    numerator = m * log(p)
    denominator = log(2) * (1 - e ** (-log(2)))
    n = -int(numerator / denominator)
    k = int((n / m) * log(2))
    cbf = [0] * n
    for w in words:
        ind = get_hash_values(w, k, n)
        for i in ind:
            cbf[i] += 1
    return cbf, k, m, n


def get_hash_values(word, k, n):
    pos = []
    hash_w = adler32(word.encode('utf-8'))
    for i in range(k // 2):
        pos.append(int(hash_w / (i + 1)) % n)
    hash_w = crc32(word.encode('utf-8'))
    for i in range(k // 2, k):
        pos.append(int(hash_w / (i + 1)) % n)
    return pos


def get_amount_words(f):
    words = f.read().split()
    set_words = set(words)
    return set_words, len(set_words)


def check_word_in_cbf(cbf, word, k):
    pos = []
    n = len(cbf)
    hash_w = adler32(word.encode('utf-8'))
    for i in range(k // 2):
        pos.append(int(hash_w / (i + 1)) % n)
    hash_w = crc32(word.encode('utf-8'))
    for i in range(k // 2, k):
        pos.append(int(hash_w / (i + 1)) % n)
    b = [0] * k
    for i in range(k):
        b[i] = cbf[pos[i]] > 0
    for x in b:
        if not x:
            return False
    return True


def get_probability(k, m, n):
    return (1 - e ** (-(k * m) / n)) ** k


if __name__ == '__main__':

    precision = 0.0001
    file = open('Billie-eilish-your-power-lyrics.txt')
    new_cbf, k, m, n = generate_cbf(file, precision)
    f = open('words.txt')
    samples = f.readline().split()
    for s in samples:
        if check_word_in_cbf(new_cbf, s, k):
            print(s, 'belongs to text')
        else:
            print(s, 'does not belong to text with probability: ', float(get_probability(k, m, n)))
