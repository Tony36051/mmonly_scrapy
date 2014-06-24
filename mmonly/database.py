import sqlite3


class database(object):
    def __init__(self):
        print 'init'
        cn = sqlite3.connect('mmonly_sqlite3.db')
        cursor = cn.cursor()
        sql = 'create table if not exists mmonly(no INTEGER primary key, state TEXT, title TEXT,update_time TEXT, path TEXT, link TEXT)'
        insert_sql = 'insert into mmonly("no", "state", "title", "update_time", "path", "link") values("%s","%s","%s","%s","%s","%s")'%(item['number'],item['state'],item['title'],item['update_time'],item['path'],item['link'])


    def __del__(self):
        print 'del'
        cn.close()


    if __name__ == '__main__':
        database()
        print 'hello'
