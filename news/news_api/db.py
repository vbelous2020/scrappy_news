import psycopg
from psycopg import Error

db_name = "scrapy_fast"
db_user = "postgres"
db_password = "firmamento10"

con = f"dbname={db_name} user={db_user} password={db_password}"


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


def delete_index(url):
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
