import newspaper
from pymongo import MongoClient
# from config import MONGODB_DB, MONGODB_SERVER, MONGODB_COLLECTION
import logging
import db as func_db

db_server = '127.0.0.1'
db = "observer"
db_urls = "news_data"


logging.basicConfig(filename='new_articles.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

client = MongoClient(db_server, 27017)
db = client[db]
posts = db[db_urls]


list_of_sites = func_db.url_list()


# "pravda.com.ua", "interfax.com.ua", "regnum.ru", "unn.com.ua", "ukrinform.ru",
# "rbc.ru", "russian.rt.com", "korrespondent.net", "nv.ua", "gordonua.com", "bbc.com", "president.gov.ua"
# "epravda.com.ua", "dw.com", "delo.ua", "censor.net", "ukranews.com", "lb.ua", "kp.ua", "zn.ua", "gazeta.ua", "focus.ua",
# "sud.ua", "kommersant.ru", "currenttime.tv", "glavnoe.ua", "dumskaya.net", "autonews.autoua.net",
# "radiosvoboda.org", "tengrinews.kz", "ua.news", "news.un.org", "24tv.ua", "apk-inform.com", "news.bigmir.net",
# "msp.gov.ua", "avianews.com", "apostrophe.ua", "eurointegration.com.ua", "jurliga.ligazakon.net", "slovoidilo.ua",
# "ua-news.in.ua", "kharkivoda.gov.ua", "moz.gov.ua", "protocol.ua", "kurs.com.ua", "newsukraine.org", "folga.com.ua",
# "daily.rbc.ua", "headlinesua.com", "i-ua.tv", "maritimebusinessnews.com.ua", "ukrinform.ua",
# "zaxid.net",  "5.ua", "suspilne.media", "fakty.com.ua", "defence-ua.com", "rada.gov.ua",
# "novynarnia.com", "glavcom.ua", "ukravtodor.gov.ua", "dnew.info", "cerkva.kharkov.ua", "mukachevo.net",
# "ukraineisyou.com.ua", "adverman.com", "replyua.net", "hronika.info",
# "facenews.ua", "espreso.tv", "sport.ua", "newsyou.info", "from-ua.com", "politeka.net", "ictv.ua",
# "terrikon.com", "merezha.co", "vgorode.ua", "osvita.ua", "dialog.ua", "business.ua",
# "ua.112ua.tv", "zikua.news", "hvylya.net", "vgolos.ua", "bagnet.org", "football24.ua",
# "fakty.ua", "tochka.net", "stb.ua", "kriminal.tv", "novosti-n.org", "press-centr.com", "korupciya.com",
# "woman.ru", "gorod.dp.ua", "aif.ru", "narodna-pravda.ua", "hyser.ua", "krymr.com", "dp.informator.ua", "tyzhden.ua",
# "playground.ru", "schoollife.org.ua", "itc.ua", "isport.ua", "enovosty.com", "bykvu.com", "podrobnosti.ua",
# "expres.online", "golos.ua", "mfa.gov.ua", "uaspectr.com", "zmist.direct",  "omr.gov.ua", "bank.gov.ua",
# "mvs.gov.ua", "minregion.gov.ua", "mtu.gov.ua",
# "nais.gov.ua", "minjust.gov.ua", "decentralization.gov.ua", "ua.meest.com",  "gazeta-fp.com.ua",
# "dmsu.gov.ua", "volynnews.com", "kyivcity.gov.ua",  "ba.org.ua", "nssmc.gov.ua", "tax.gov.ua",
# "thedigital.gov.ua", "news.dtkt.ua", "gp.gov.ua", "day.kyiv.ua", "kmu.gov.ua", "hcj.gov.ua", "prostir.ua",
# "armyinform.com.ua",  "rp.gov.ua", "mil.in.ua", "amcu.gov.ua",
# "vmr.gov.ua", "arma.gov.ua", "portal.lviv.ua", "phc.org.ua",  "liga.net", "iz.ru", "rg.ru",
# "tsn.ua","golosameriki.com",  "babel.ua", "mind.ua", "hromadske.ua", "meta.ua", "rian.com.ua",
# "34.ua",  "dnipro.tv", "ms.detector.media", "znaj.ua", "expres.online",
# "unian.ua", "depo.ua", "racurs.ua", "comments.ua", "vesti.ua", "crimea.kp.ru", "pfu.gov.ua",
# "dpsu.gov.ua", "yur-gazeta.com", "stv.detector.media", "customs.gov.ua")


# list_not_working = ("segodnya.ua", "delo.ua", "ukraina.ru", "ukraine.segodnya.ua", "newcominfo.info", "bbcccnn.org",
# "telegraf.com.ua",  "strana.news", "antikor.com.ua", "newsoneua.tv", "finance.ua", "prm.ua", "hitculture.online", "sfs.gov.ua",
# "dazv.gov.ua", "mepr.gov.ua",  "visnuk.com.ua", "golovbukh.ua", "obozrevatel.com", "pidgorodne.dp.ua",


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
            actual_site = newspaper.build('https://' + site, memoize_articles=True)
            if actual_site.size() < 1:
                logging_info = f"No new articles - good news!"
                logging.info(logging_info)
            else:
                for article in actual_site.articles:
                    post = posts.insert_one({"url": article.url}).inserted_id
                logging_info = f"Add {actual_site.size()} at {actual_site.url}"
                logging.info(logging_info)


# get_new_articles(list_of_sites)
