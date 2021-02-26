import requests
import psycopg2
import configparser


def take_posts():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    token = config['VK']['token']
    domain = config['VK']['domain']
    version = 5.126
    offset = 0
    all_posts = []
    count_posts = int(config['VK']['count_posts'])
    while offset < count_posts:
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


def create_dict_count_word():
    dictionary = {}
    all_posts = take_posts()
    for post in all_posts:
        text = post['text']
        words = text.split()
        for word in words:
            if word in dictionary.keys():
                dictionary[word] += 1
            else:
                dictionary[word] = 1
    return dictionary


def add_to_db_count_word():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    con = psycopg2.connect(
        database=config['DB']['database'],
        user=config['DB']['user'],
        password=config['DB']['password'],
        host=config['DB']['host'],
        port=config['DB']['port']
    )
    cur = con.cursor()
    cur.execute("truncate table count_words")
    con.commit()
    print("Database opened successfully")
    count_words = create_dict_count_word()
    cnt = 0
    for name in count_words.keys():

        values = {'name': name, 'count': count_words[name]}
        cur.execute("insert into count_words (name, count) values (%(name)s,%(count)s)",
                    values
                    )
        cnt += 1
        if cnt > 5:
            break
    con.commit()


add_to_db_count_word()
