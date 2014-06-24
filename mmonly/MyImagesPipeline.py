from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.contrib.pipeline.images import FSImagesStore
from scrapy.exceptions import DropItem
from scrapy.http import Request
import os
import shutil
import time



class MyImagesPipeline(ImagesPipeline):
    images_store = ''
    persist_path = ''


    def get_media_requests(self, item, info):
        if not  item['image_urls']:
            print '****** no pics  ********'
        for image_url in item['image_urls']:

            #yield Request(image_url,headers={'referer':'http://www.mmonly.com'+item['link']})
            yield Request(image_url)



    def item_completed(self, results, item, info):
        if not (MyImagesPipeline.images_store and MyImagesPipeline.persist_path):
            with open(r'mmonly\settings.py') as settings:
                for line in settings:
                    if line:
                        if line.startswith('IMAGES_STORE'):
                            MyImagesPipeline.images_store = line.split('\'')[1]
                        if line.startswith('persist'):
                            MyImagesPipeline.persist_path = line.split('\'')[1]
                        
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        des_path = '%s\\%s.%s.%s(%sP).%s'%(MyImagesPipeline.persist_path,item['number'],item['update_time'],item['title'],item['pages'],item['category'])
        #print '===================== %s ================='%des_path
        item['path'] = des_path
        if not os.path.exists(des_path):
            os.makedirs(des_path)
            
        fp = open(os.path.join(des_path,'log.txt'),'a')
        fp.write('='*10 + ' The following came at %s '%time.strftime( '%Y-%m-%d %X', time.localtime()) + '='*10 + '\n')
        for (i,image_path) in enumerate(image_paths):
            try:
                shutil.move(os.path.join(MyImagesPipeline.images_store,image_path),'%s\\%d.%s'%(des_path,i,os.path.basename(image_path)))
            except shutil.Error, ex:
                fp.write(time.strftime( '%Y-%m-%d %X: ', time.localtime())+str(ex)+'\n')
                continue
        fp.close()
        downFail_counter = 0
        item['images'] = []
        for t in results:
            if t[0]:
                item['images'].append(t)
            else :
                downFail_counter += 1
                item['images'].append((False,'down fail'))
        if downFail_counter:
            item['state'] = 'fail'
        else:
            item['state'] = 'ok'
        #print '********** images ********'+item['images']
        return item
