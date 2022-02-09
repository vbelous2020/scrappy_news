import newspaper
from pymongo import MongoClient
import logging
import db as func_db
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

client = MongoClient(config["mongo"]["db_server"], config["mongo"]["db_port"])
db = client[config["mongo"]["db_name"]]
posts = db[config["mongo"]["urls_collection"]]

logging.basicConfig(filename='../log/new_articles.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

list_of_sites = func_db.url_list()


def rss_exist(site):
    actual_site = newspaper.build('https://' + site, memoize_articles=False)
    if actual_site.size() <= 0:
        logging_info = f"We didn't detect rss on {site} "
        logging.info(logging_info)
        return False
    else:
        pass


def get_new_articles(list):
    for site in list:
        if rss_exist(site) is False:
            pass
        else:
            actual_site = newspaper.build('https://' + site, memoize_articles=False)     # True
            if actual_site.size() < 1:
                logging_info = f"No new articles - good news!"
                logging.info(logging_info)
            else:
                for article in actual_site.articles:
                    post = posts.insert_one({"url": article.url}).inserted_id
                logging_info = f"Add {actual_site.size()} at {actual_site.url}"
                logging.info(logging_info)


get_new_articles(list_of_sites)
