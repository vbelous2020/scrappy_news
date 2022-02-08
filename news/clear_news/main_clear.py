import logging
import clear

logging.basicConfig(filename='log/clear_work_log.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def transfer_to_clear():
    data = clear.read_from_mongo()
    clear.write_to_postgres(data)


if __name__ == "__main__":
    while True:
        transfer_to_clear()
