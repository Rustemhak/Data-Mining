import requests
import psycopg2


def take_posts(domain, count_post):
    token = '378645243786452437864524f337f0dea0337863786452457b19ce45a551858c0473f14'
    version = 5.126
    offset = 0
    all_posts = []

    while offset < count_post:
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


def create_dict_count_word(domain, count_post):
    dictionary = {}
    all_posts = take_posts(domain, count_post)
    for post in all_posts:
        text = post['text']
        words = text.split()
        for word in words:
            if word in dictionary.keys():
                dictionary[word] += 1
            else:
                dictionary[word] = 1
    return dictionary


def add_to_db_count_word(group_name, count_post):
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="tak5353446512",
        host="databasefordatamining.cttpobcopzft.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    cur = con.cursor()
    cur.execute("truncate table count_words")
    con.commit()
    print("Database opened successfully")
    count_words = create_dict_count_word(group_name, count_post)
    for name in count_words.keys():
        values = {'name': name, 'count': count_words[name]}
        cur.execute("insert into count_words (name, count) values (%(name)s,%(count)s)",
                    values
                    )
    con.commit()


group_name = 'itis_kfu'
count_post = 200
add_to_db_count_word(group_name, count_post)
