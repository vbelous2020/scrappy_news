import logging
import pymongo
import psycopg
from psycopg import Error
import pytz
from config_clear import MONGODB_DB, MONGODB_COLLECTION, con

mng_cl = pymongo.MongoClient('127.0.0.1')
db = mng_cl[f'{MONGODB_DB}']
source_collection = db[f'{MONGODB_COLLECTION}']

logging.basicConfig(filename='log/clear_work_log.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def read_from_mongo():
    data = list()
    try:
        source = source_collection.find()
        for item in source:
            d = dict()
            d['url'] = item['url']
            d['title'] = item['title']
            d['date'] = item['date']
            d['author'] = item['author']
            d['author_link'] = item['author_link']
            d['short'] = item['short']
            main_text = str()
            for i in item['main_text']:
                main_text += i + ' '
            print(main_text)
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


def write_to_postgres(data):
    for d in data:
        if url_check(d['url']):
            continue
        else:
            try:
                logging_info = f"Saving data from url: {d['url']}"
                logging.info(logging_info)
                with psycopg.connect(con) as conn:
                    with conn.cursor() as cur:
                        new_pattern = """
                        INSERT INTO clear_data (url, title, date, author, author_link, short, main_text) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                        cur.execute(new_pattern, (d['url'], d['title'], d['date'], d['author'], d['author_link'],
                                                  d['short'], d['main_text']))
                        conn.commit()
                logging_info = "Data saved successfully!"
                logging.info(logging_info)
            except (Exception, Error) as e:
                logging_info = f"Error: {e}"
                logging.info(logging_info)
            finally:
                if conn:
                    cur.close()
                    conn.close()


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
                """ SET timezone = 'Europe/Kiev' """
                print("DONE")
    except (Exception, Error) as e:
        logging_info = f"Error: {e}"
        logging.info(logging_info)
    finally:
        if conn:
            cur.close()
            conn.close()
