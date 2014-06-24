# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json
import sqlite3


class MmonlyPipeline(object):
    cn = sqlite3.connect('mmonly_sqlite3.db')
    cursor = cn.cursor()
    cursor.execute('create table if not exists mmonly(no INTEGER primary key, state TEXT, title TEXT,update_time TEXT, path TEXT, link TEXT)')
        
    
    def process_item(self, item, spider):
        
        #print '================================================'
        line = json.dumps(dict(item))+'\n'
        file = open(item['path']+'\\'+item['number']+'.json','wb')
        file.write(line)
        file.close()
        #print '================================================'

        select_sql = 'select state from mmonly where no = %s' % item['number']
        #print 'select: '+select_sql
        
        sr = MmonlyPipeline.cursor.execute(select_sql).fetchone()
        
        
        if sr:  # select has record, and the state must be fail
            if(item['state'] == 'ok'): # state changes
                #print '============= MmonlyPipeline: update ======'
                update_sql = 'update mmonly set state = "ok" where no = %d' % item['number']
                MmonlyPipeline.cursor.execute(update_sql)
        else:  # select has NOT records
            
            #print '============= MmonlyPipeline: insert into ======'
            insert_sql = 'insert into mmonly("no", "state", "title", "update_time", "path", "link") values("%s","%s","%s","%s","%s","%s")'%(item['number'],item['state'],item['title'],item['update_time'],item['path'],item['link'])
            MmonlyPipeline.cursor.execute(insert_sql)
            
        MmonlyPipeline.cn.commit()
        return item
