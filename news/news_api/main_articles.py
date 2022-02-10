from time import sleep

from db import get_new_articles

if __name__ == "__main__":
    while True:
        get_new_articles()
        sleep(300)
