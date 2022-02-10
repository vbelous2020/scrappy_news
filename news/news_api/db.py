import psycopg
from psycopg import Error
import newspaper
from pymongo import MongoClient
import logging
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

con = f"""
      dbname={config['postgres']['postgres_name']}
      user={config['postgres']['postgres_user']}
      password={config['postgres']['postgres_password']}
      """

client = MongoClient(config["mongo"]["db_server"], 27017)
db = client[config["mongo"]["db_name"]]
urls_collection = db[config["mongo"]["urls_collection"]]

logging.basicConfig(filename='../log/new_articles.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def rss_exist(site):
    actual_site = newspaper.build(site, memoize_articles=False)
    if actual_site.size() <= 0:
        logging_info = f"We didn't detect rss on {site} "
        logging.info(logging_info)
        return False
    else:
        pass


def get_new_articles():
    list = url_list()
    for site in list:
        if rss_exist(site) is False:
            pass
        else:
            actual_site = newspaper.build(site, memoize_articles=False)  # True
            if actual_site.size() < 1:
                logging_info = f"No new articles - good news!"
                logging.info(logging_info)
            else:
                for article in actual_site.articles:
                    url = article.url
                    if url.find("photo.unian.ua/photo/") != -1 or \
                            url.find("unian.ua/static/press/live") != -1 or \
                            url.find("unian.ua/news/archive") != -1 or \
                            url.find("unian.ua/multimedia/video") != -1 or \
                            url.find("lenta.ua/novosti/") != -1:
                        continue
                    else:
                        urls_collection.insert_one({"url": url})
                logging_info = f"Add {actual_site.size()} at {actual_site.url}"
                logging.info(logging_info)


def get_list_of_urls():
    urls = list()
    objects = urls_collection.find()
    for obj in objects:
        urls.append(obj['url'])
    return urls


def delete_parsed_url(url):
    try:
        urls_collection.delete_one({"url": url})
        logging_info = f"Url parsed and removed from ulr list: {url}."
        logging.info(logging_info)
    except (Exception, Error) as error:
        logging_info = f"Error: {error}."
        logging.info(logging_info)


def create_pattern_table():
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            CREATE TABLE pattern (
                                id serial PRIMARY KEY,
                                name TEXT,
                                url TEXT, 
                                title_path TEXT,
                                title_hash TEXT,
                                date_path TEXT,
                                date_hash TEXT,
                                author_path TEXT,
                                author_hash TEXT,
                                short_path TEXT,
                                short_hash TEXT,
                                main_text_path TEXT,
                                main_text_hash TEXT,
                                username TEXT
                                )
                            """)
                conn.commit()
    except (Exception, Error) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()


def add_pattern(name, user, url, title_path, title_hash, date_path, date_hash, author_path,
                author_hash, short_path, short_hash, main_text_path, main_text_hash):
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                new_pattern = """
                INSERT INTO pattern (
                name, username, url, title_path, title_hash, date_path, date_hash, author_path, 
                author_hash, short_path, short_hash, main_text_path, main_text_hash
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cur.execute(new_pattern, (name, user, url, title_path, title_hash, date_path, date_hash, author_path,
                                          author_hash, short_path, short_hash, main_text_path, main_text_hash))
                conn.commit()
    except (Exception, Error) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()


def unique_url_check(url):
    flag = False
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                search_pattern = f"""SELECT * FROM pattern WHERE url = '{url}'"""
                cur.execute(search_pattern)
                conn.commit()
                result = cur.fetchone()
                if result:
                    flag = True
                    name = result[1]
                else:
                    name = None
    except (Exception, Error) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return flag, name


def url_list():
    urls = list()
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                search_pattern = f"""SELECT url FROM pattern"""
                cur.execute(search_pattern)
                conn.commit()
                result = cur.fetchall()
                for r in result:
                    urls.append(r[0])
    except (Exception, Error) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return urls


def get_pattern(url):
    d = dict()
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                search_pattern = f"""
                SELECT (title_path, date_path, author_path, short_path, main_text_path) 
                FROM pattern WHERE url = '{url}'"""
                cur.execute(search_pattern)
                conn.commit()
                result = cur.fetchone()
                if result:
                    d['title_path'] = result[0][0]
                    d['date_path'] = result[0][1]
                    d['author_path'] = result[0][2]
                    d['short_path'] = result[0][3]
                    d['main_text_path'] = result[0][4]
    except (Exception, Error) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return d


def check_pattern(current_url):
    pattern = dict()
    urls = url_list()
    for url in urls:
        index = current_url.find(url)
        if index != -1:
            pattern = get_pattern(url)
        else:
            continue
    return pattern


def delete_pattern(url):
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                search_pattern = f"""DELETE FROM pattern WHERE url = '{url}'"""
                cur.execute(search_pattern)
                conn.commit()
    except (Exception, Error) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
