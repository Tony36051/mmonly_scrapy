from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from mmonly.items import MmonlyItem
from scrapy.http import Request
import sqlite3

class MmonlySpider(BaseSpider):
    cn = sqlite3.connect('mmonly_sqlite3.db')
    cursor = cn.cursor()
    cursor.execute('create table if not exists mmonly(no INTEGER primary key, state TEXT, title TEXT,update_time TEXT, path TEXT, link TEXT)')
    done_list = [t[0]  for t in cursor.execute('select no from mmonly where state = "ok"').fetchall()]
  
    name = "mmonly"
    allowed_domains = ["mmonly.com"]
    start_urls = [
        #"http://www.mmonly.com/glamour/201107/1378.html"
        #"http://www.mmonly.com/glamour/201103/36.html"
        #"http://www.mmonly.com/glamour/201308/4947.html"
        #"http://www.mmonly.com/glamour/list_1.html",
        "http://www.mmonly.com/photo/list_1.html",
        "http://www.mmonly.com/korea/list_1.html",
        "http://www.mmonly.com/beautyleg/list_1.html",
        "http://www.mmonly.com/beauty/list_1.html",
        "http://www.mmonly.com/cosplay/list_6_1.html",
        "http://www.mmonly.com/jiepaimeinv/list_7_1.html"
        ]
    flag = {}.fromkeys(('glamour','photo','korea','beautyleg','beauty','cosplay','jiepaimeinv'),False)

    def parse(self, response):
        #print response.url
        hxs = HtmlXPathSelector(response)
        
        item_pages = hxs.select('/html/body/div[2]/div[7]/div[1]/ul//@href').extract()
        for i in range(0,len(item_pages),2):
            num = int(item_pages[i][item_pages[i].rfind('/')+1:-5])
            if num in self.done_list:
                print '========== ignore %d done item ============'%num
            else:
                #print 'parseItem: http://www.mmonly.com'+item_pages[i]
                yield Request('http://www.mmonly.com'+item_pages[i], callback = self.parseItem)
            
        
        if not self.flag.get(response.url.split('/')[3]):
            self.flag[response.url.split('/')[3]] = True
            s = hxs.select('/html/body/div[2]/div[9]/ul/li[last()]/a/@href').extract()[0]
            nList = int(s[s.rfind('_')+1:s.rfind('.')])
            for j in range(2,nList+1):
                #print response.url[:response.url.rfind('_')+1]+str(j)+'.html'
                yield Request(response.url[:response.url.rfind('_')+1]+'%d.html'%j, callback = self.parse)
                
        

        

    def parseItem(self, response):
        #print '==================== got ================'
        # Duplicate Item detecting:
        item = MmonlyItem()
        item['number'] = response.url[response.url.rfind('/')+1:-5]
        select_sql = 'select state from mmonly where no = %s' % item['number']
        sr = MmonlySpider.cursor.execute(select_sql).fetchone()
        if sr: #if sr==None, bool(sr)==false, selectResult is empty
            if(sr[0] == 'ok'): # select has record and state is ok
                #write log file
                return

        # parsing item from response.url
        item['link'] = response.url[response.url.find('com')+3:]
        item['category'] = item['link'].split('/')[1]
        
        # parsing item by xpathSelector
        hxs = HtmlXPathSelector(response)
        pages = hxs.select('/html/body/div[2]/div[5]/ul/li[1]/a/text()').extract()[0]
        if pages.find(':')==-1:
            pages = hxs.select('/html/body/div[2]/div[5]/ul/li[2]/a/text()').extract()[0]
        item['pages'] = pages[1:-3]
        
        item['title'] = hxs.select('/html/body/div[2]/div[2]/div[1]/h1/text()').extract()[0]
        item['update_time'] = hxs.select('/html/body/div[2]/div[2]/div[1]/em/text()').extract()[0][6:-1]
        description = hxs.select('/html/body/div[2]/div[2]/div[2]/text()').extract()
        if description:
            item['description'] = hxs.select('/html/body/div[2]/div[2]/div[2]/text()').extract()[0][5:]

        
        item['image_urls'] = hxs.select('/html/body/div[2]/div[1]/a/img/@src').extract()
        item['image_urls'].append(hxs.select('/html/body/div[2]/div[4]/div[2]/p/a/img/@src').extract()[0])
        
        if item['image_urls'][1].find('uploads') != -1:
            #print '=========== old item ==============='
            Request(response.url, callback = self.parseOldItem)
        else:
            for i in range(2,int(item['pages'])+1):
                #print "%s%d%s" % (image_url_base[0][0:image_url_base[0].rfind('/')+1] ,i,".jpg")
                item['image_urls'].append("%s%d%s" % (item['image_urls'][1][0:item['image_urls'][1].rfind('/')+1] ,i,".jpg"))
        return item


    def parseOldItem(self,response):
        print '################ Catch one old Item ################3'
        pass
        '''
        hxs = HtmlXPathSelector(response)
   
        item = MmonlyItem()
        item['link'] = link = hxs.select('//div[@class="arcPic l"]/a/@href').extract()[0]
        item['number'] = link[link.rfind('/')+1:link.rfind('.')]
        item['title'] = title = hxs.select('//div[@class="arcTitle"]/h1/text()').extract()[0]
        item['update_time'] = update_time = hxs.select('//div[@class="arcTitle"]/em/text()').extract()[0][6:]
        description = hxs.select('//div[@class="arcDES both"]/text()').extract()
        if not description:
            item['description'] = description[0]
        #item['category'] = category = hxs.select('//div[@class="arcPre both"]/a[2]/text()').extract()[0]
        item['category'] = link[1:link.find('/',3)]
        pages = hxs.select('/html/body/div[2]/div[5]/ul/li[1]/a/text()').extract()[0]
        item['pages'] = pages[1:pages.rfind(':')-1]
        #print '================================='+item['pages']
        item['image_urls'] = image_url_base = hxs.select('//div[@class="arcPic l"]/a/img/@src').extract()
        
        for i in range(1,int(item['pages'])+1):
            #print "%s%d%s" % (image_url_base[0][0:image_url_base[0].rfind('/')+1] ,i,".jpg")
            #item['image_urls'].append("%s%d%s" % (image_url_base[0][0:image_url_base[0].rfind('/')+1] ,i,".jpg"))
            #item['image_urls'].append(hxs.select('/html/body/div[2]/div[4]/div[2]/p/a/img/@src').extract()[0])
        return item
        '''
