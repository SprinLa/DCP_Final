from bsddb import db


def irecords(curs):
    record = curs.first()
    while record:
        yield record
        record = curs.next()


if __name__ == '__main__':

    adb = db.DB()
    adb.open('../db/db_filename', dbtype=db.DB_HASH, flags=db.DB_CREATE)
    for i, w in enumerate('some word for example'.split(" ")):
        adb.put(w, str(i))

    for key, data in irecords(adb.cursor()):
        print key, data

    adb.delete("some")
    print adb.get("some")


    adb.close()
