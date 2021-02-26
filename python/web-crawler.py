import requests
import psycopg2


def take_200_posts(domain):
    token = '378645243786452437864524f337f0dea0337863786452457b19ce45a551858c0473f14'
    version = 5.126
    offset = 0
    all_posts = []

    while offset < 200:
        response = requests.get('https://api.vk.com/method/wall.get', params={
            'access_token': token,
            'v': version,
            'domain': domain,
            'count': 100,
            'offset': offset
        }
                                )
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
    return all_posts


def create_dict_count_word(domain):
    dictionary = {}
    all_posts = take_200_posts(domain)
    for post in all_posts:
        text = post['text']
        words = text.split()
        for word in words:
            if word in dictionary.keys():
                dictionary[word] += 1
            else:
                dictionary[word] = 1
    return dictionary


def get_top_100_word(domain):
    count = 0
    dictionary = create_dict_count_word(domain)
    top_words = []
    for top_word in sorted(dictionary, reverse=True, key=lambda w: dictionary[w]):
        if count <= 100:
            top_words.append([top_word, dictionary[top_word]])
            count += 1
        else:
            break
    return top_words


def add_to_db_top_100_word(group_name):
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="tak5353446512",
        host="databasefordatamining.cttpobcopzft.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    cur = con.cursor()
    cur.execute("truncate table top_100_words")
    con.commit()
    print("Database opened successfully")
    top_100_words = get_top_100_word(group_name)
    for item in top_100_words:
        values = {'name': item[0], 'count': item[1]}
        cur.execute("insert into top_100_words (name, count) values (%(name)s,%(count)s)",
                    values
                    )
    con.commit()


group_name = 'itis_kfu'
add_to_db_top_100_word(group_name)
