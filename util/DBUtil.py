from bsddb import db
import os
import logging

LOG_FILE_PATH = '/data0/log/DCP.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')


def fetch(curs):
    record = curs.first()
    while record:
        yield record
        record = curs.next()


def deleteByKey(db_name, content_key):
    database = db.DB()
    database.open('../db/' + db_name, dbtype=db.DB_HASH, flags=db.DB_CREATE)
    database.delete(content_key)

    logging.info("delete " + content_key + " success")
    database.close()


def bulk_delete(db_name, content_key_list):
    database = db.DB()
    database.open('../db/' + db_name, dbtype=db.DB_HASH, flags=db.DB_CREATE)
    for content_key in content_key_list:
        database.delete(content_key)

        logging.info("delete " + content_key + " success")
    database.close()


def bulk_insert(db_name, content_dict):
    database = db.DB()
    database.open('../db/' + db_name, dbtype=db.DB_HASH, flags=db.DB_CREATE)
    for content_key in content_dict.keys():
        if database.get(content_key):
            logging.warn(content_key + " already exists")
        else:
            database.put(content_key, content_dict[content_key])
            logging.info("insert " + content_key + " success")
    database.close()


def insert(db_name, content_key, content_value):
    database = db.DB()
    database.open('../db/' + db_name, dbtype=db.DB_HASH, flags=db.DB_CREATE)
    database.put(content_key, content_value)
    logging.info("insert " + content_key + " success")
    database.close()


def selectAll(db_name):
    result_set = {}
    database = db.DB()
    database.open('../db/' + db_name, dbtype=db.DB_HASH, flags=db.DB_CREATE)
    for content_key, content_value in fetch(database.cursor()):
        result_set[content_key] = content_value

    return result_set


def selectByKey(db_name, content_key):
    database = db.DB()
    database.open('../db/' + db_name, dbtype=db.DB_HASH, flags=db.DB_CREATE)
    content_value = database.get(content_key)
    database.close()

    return content_value


if __name__ == '__main__':
    adb = db.DB()

    adb.open('../db/db_filename', dbtype=db.DB_HASH, flags=db.DB_CREATE)
    for i, w in enumerate('some word for example'.split(" ")):
        adb.put(w, str(i))

    for key, data in fetch(adb.cursor()):
        print key, data

    print adb.get("some")
    adb.put("some", str(2))
    print adb.get("some")
    print adb.get("sada")

    adb.close()
