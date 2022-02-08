import logging
import pymongo
import psycopg
from psycopg import Error
from config_clear import MONGODB_DB, MONGODB_COLLECTION, con

mng_cl = pymongo.MongoClient('127.0.0.1')
db = mng_cl[f'{MONGODB_DB}']
source_collection = db[f'{MONGODB_COLLECTION}']

logging.basicConfig(filename='log/clear_work_log.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def create_clear_data_table():
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            CREATE TABLE clear_data (
                                id serial PRIMARY KEY,
                                url TEXT, 
                                title TEXT,
                                date TIMESTAMPTZ,
                                date_publ TEXT,
                                author TEXT,
                                author_link TEXT,
                                short TEXT,
                                main_text TEXT
                                )
                            """)
                conn.commit()
                cur.execute(""" SET timezone = 'Europe/Kiev' """)
                conn.commit()
                print("DONE")
    except (Exception, Error) as e:
        logging_info = f"Error: {e}"
        logging.info(logging_info)
    finally:
        if conn:
            cur.close()
            conn.close()


def read_from_mongo():
    data = list()
    try:
        source = source_collection.find({'cleared': False})
        for item in source:
            d = dict()
            d['url'] = item['url']
            d['title'] = item['title']
            d['date'] = item['date']
            d['author'] = item['author']
            d['author_link'] = item['author_link']
            d['short'] = item['short']
            d['timestamp'] = item['timestamp']
            main_text = str()
            for i in item['main_text']:
                main_text += i + ' '
            d['main_text'] = item['main_text']
            data.append(d)
    except Exception as e:
        logging_info = f"Error: {e}"
        logging.info(logging_info)
    return data


def url_check(url):
    flag = False
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                search_pattern = f"""SELECT url FROM clear_data WHERE url = '{url}'"""
                cur.execute(search_pattern)
                conn.commit()
                result = cur.fetchone()
                if result:
                    flag = True
    except (Exception, Error) as e:
        logging_info = f"Error: {e}"
        logging.info(logging_info)
    finally:
        if conn:
            cur.close()
            conn.close()
    return flag


def flag_to_mongo(url):
    source_collection.update_one({'url': url},
                                 {'$set': {'cleared': True}}, upsert=False)
    logging_info = f'Url: {url} has been updated!'
    logging.info(logging_info)


def write_to_postgres(data):
    if data:
        for d in data:
            if url_check(d['url']):
                print()
                logging_info = f"Url({d['url']}) exists in db. Nothing to add."
                logging.info(logging_info)
                continue
            else:
                try:
                    logging_info = f"Saving data from url: {d['url']}"
                    logging.info(logging_info)
                    with psycopg.connect(con) as conn:
                        with conn.cursor() as cur:
                            new_pattern = """
                            INSERT INTO clear_data (url, title, date_publ, date, author, author_link, short, main_text) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                            cur.execute(new_pattern, (d['url'], d['title'], d['date'], d['timestamp'], d['author'],
                                                      d['author_link'], d['short'], d['main_text']))
                            conn.commit()
                    flag_to_mongo(d['url'])
                except (Exception, Error) as e:
                    logging_info = f"Error: {e}"
                    logging.info(logging_info)
                finally:
                    if conn:
                        cur.close()
                        conn.close()
    else:
        logging_info = f"No news - good news!"
        logging.info(logging_info)


def read_clear():
    d = dict()
    try:
        with psycopg.connect(con) as conn:
            with conn.cursor() as cur:
                search_pattern = f"""
                    SELECT (title_path, date_path, author_path, short_path, main_text_path) 
                    FROM pattern """
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
