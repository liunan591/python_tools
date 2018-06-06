# -*- coding: utf-8 -*-

import datetime
from concurrent import futures
import requests
from bs4 import BeautifulSoup
from src.utility.pangolin_logger import PangolinLogger
from hashlib import md5
import MySQLdb

#%%info
class ProjectInfo():

    def __init__(self,name):
        self.name = name
        self.finished = u"" #finished or not
        self.url = None
        self.common_info_dict = {u"批准号":u"",u"项目类别":u"",u"依托单位":u"",
            u"项目负责人":u"",u"资助经费":u"",u"批准年度":u"",u"关键词":u""}
        self.finished_info_dict = {u"申请代码":u"",u"负责人职称":u"",u"研究期限":u"",
            u"中文主题词":u"",u"英文主题词":u"",u"中文摘要":u"",u"英文摘要":u"",u"结题摘要":u""}
        self.achievement = u""

    def set_common_info(self, key, value):
        if key in self.common_info_dict:
            self.common_info_dict[key] = value
            
    def set_finished_info(self, key, value):
        if key in self.finished_info_dict:
            self.finished_info_dict[key] = value
        
    def get_project_info(self):
        return [self.finished, self.name,    #base info
        #common info(authorization_n p_type support_organization principal funds approval_year key_words)
        self.common_info_dict[u"批准号"],self.common_info_dict[u"项目类别"],
        self.common_info_dict[u"依托单位"],self.common_info_dict[u"项目负责人"],
        self.common_info_dict[u"资助经费"],self.common_info_dict[u"批准年度"],
        self.common_info_dict[u"关键词"],      
        #finished info:
            #request_code principal_technical study_period theme_words_c
            #theme_word_e abstract_c abstract_e abstract_finished
        self.finished_info_dict[u"申请代码"],self.finished_info_dict[u"负责人职称"],
        self.finished_info_dict[u"研究期限"],self.finished_info_dict[u"中文主题词"],
        self.finished_info_dict[u"英文主题词"],self.finished_info_dict[u"中文摘要"],
        self.finished_info_dict[u"英文摘要"],self.finished_info_dict[u"结题摘要"],
        #achievement info
        self.achievement]
        
        
#%%method
class NSFC_crawl():    
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
        self.proxy = {}
        self.ses = requests.session()
        self.not_finished_list = [] 
        self.finished_list = [] 
        self.page_num = 0
        self.items_num = 0

    def __parse_captcha(self):
        #!----------------the web set in next line may be disabled in morning
        checkcode = self.ses.get('http://npd.nsfc.gov.cn/randomAction.action',
                            headers = self.header, proxies = self.proxy)  
        rc = RClient('Winterto1990', '1209wentao.', '99115', 'a33367e93a0a48c6a23103d80a8f70f6')
        im = checkcode.content
        code_result = dict(rc.rk_create(im,3040)).get('Result')
        self.code = code_result
        try:
            page = self.__parse_page(1, 'http://npd.nsfc.gov.cn/fundingProjectSearchAction!search.action')
            self.page_num = self.__cal_page_num(page)
            PangolinLogger().info("this time get %d pages from web" % self.page_num)
        except Exception_parse_page:
            self.__parse_captcha()
    
    def nsfc_crawl(self, progress = None):
        start = 1
        self.page_num = 99999999
        if progress:
            start = int(progress)
        while start < self.page_num:
            end = start + 1000
            self.__nsfc_crawl(start,end)
            start = end
        
    def __nsfc_crawl(self, start, end):
        self.__parse_captcha()
        page_n = start #the page which is going to crawl
        while True:
            try:
                page = self.__parse_page(page_n, 'http://npd.nsfc.gov.cn/fundingProjectSearchAction!search.action')
                PangolinLogger().info("crawling item list page : %d(%d)"%(page_n,self.page_num))
                items = page.select('.time_dl')
                for item in items:
                    try:
                        self.__parse_project_info_in_item_list(item)
                    except Exception_parse_list:
                        continue
            except Exception_parse_page:
                page_n += 1
                continue
            if page_n%10 == 0:
                with futures.ThreadPoolExecutor(20) as thread:
                    thread.map(self.__parse_info_of_finished_project, range(len(self.finished_list)),self.finished_list)
                self.put_items_to_db()
                self.not_finished_list = [] 
                self.finished_list = [] 
            if page_n >= end or page_n >= self.page_num:
                self.put_items_to_db()
                break
            else:
                page_n += 1
        
            
    def __cal_page_num(self,page):
        self.items_num = int(page.find("strong").getText().strip())
        items_per_page = int(page.find("option",{"selected":"selected"}).getText().strip())
        items_num = self.items_num
        if self.items_num % 10 != 0:
            items_num = self.items_num+10
        return int(items_num/items_per_page)
                
    def __parse_page(self, page_n, url):
        try:
            data = {'currentPage'                 : page_n,
                    'fundingProject.applyCode'    : 'H',
                    'checkCode'                   : self.code}
            get = self.ses.post(url, headers=self.header, proxies=self.proxy, data=data)
            soup = BeautifulSoup(get.content, 'lxml')
            return soup
        except Exception:
            raise Exception_parse_page(page_n)
    
    def __parse_project_info_in_item_list(self,item):
        try:
            finished = True
            #get project name and create project info object
            if item.select('dt > font'):
                project_name = item.select('dt > font')[0].get_text(strip=True)
                finished = False
            else:
                project_name = item.select('dt > a')[0].get_text(strip=True)
                project_url = item.select('dt > a')[0]['href']
            project = ProjectInfo(project_name)
            if finished:
                project.finished = u"已结题"
                project.url = project_url
                self.finished_list.append(project)
            else:
                project.finished = u"未结题"
                self.not_finished_list.append(project)
            #get common info for project    
            for pj_info in item.select('dd'):
                kv = pj_info.get_text(strip=True).split(u'：')
                if len(kv) == 2:
                    key,value = kv
                    project.set_common_info(key.strip(),value.strip())
        except Exception:
            raise Exception_parse_list(item)
            
    def __parse_info_of_finished_project(self, index, project):
        PangolinLogger().info("crawling finished item: %d(%d)"%(index+1,len(self.finished_list)))
        try:
            url = 'http://npd.nsfc.gov.cn/' + project.url
            get = requests.get(url, headers= self.header, proxies= self.proxy)
            content = BeautifulSoup(get.content, 'lxml')
            abstract = []
            for desc in content.select('.jben'):
                if desc.select('b'):
                    key = desc.select('b')[0].get_text(strip=True)
                    value = desc.get_text(strip=True).replace(key, '')
                    project.set_finished_info(key,value)
                else:
                    if desc.get_text()[0] == u"：":
                        abstract.append(desc.get_text(strip=True)[1:])
                    else:
                        abstract.append(desc.get_text(strip=True))
            project.set_finished_info(u"中文摘要",abstract[0])
            if len(abstract) == 2:project.set_finished_info(u"结题摘要",abstract[1])        
            if len(abstract) == 3:
                project.set_finished_info(u"英文摘要",abstract[1])        
                project.set_finished_info(u"结题摘要",abstract[2])        
            #theme words
            for desc in content.select('.xmu'):
                key = desc.select('b')[0].get_text(strip=True)
                value = desc.get_text(strip=True).replace(key, '')
                project.set_finished_info(key,value)
            #achievement
            temp_result = []
            for desc in content.select('.detail > a'):
                temp_result.append('http://npd.nsfc.gov.cn/' + desc['href'])
            project.achievement = str(temp_result)
        except Exception:
            raise Exception_parse_item(project.url,index+1)
            
    def put_items_to_db(self):
        items = []
        items.extend(self.finished_list)
        items.extend(self.not_finished_list)
        db = MySQLdb.connect('59.110.207.215',"medo_master","MEDOmaster123","medo_master", charset='utf8' )
        cursor = db.cursor()
        i = 1
        for item in items:
            if i % 20 == 0 or i==len(items):
                PangolinLogger().info("writing %d(%d)"%(i,len(items))) 
            try:    
                info = map(lambda x: x.replace('"','\\"'),item.get_project_info())
                sql = u"insert into NSFC_copy values (%s)" % \
                    ("\"" +u"\",\"".join(info) + "\"")
                cursor.execute(sql)
                db.commit()
                i = i+1
            except Exception as e :
                PangolinLogger().error(e)
                i=i+1
        cursor.close()
        db.close()
        
    
#%%        
class Exception_parse_page(Exception):
    '''
    爬取搜索页面异常
    '''
    def __init__(self, page):
        err = u'Exception_occured_in_parse_page:{0}'.format(page)
        Exception.__init__(self, err)
        PangolinLogger().error(err)

class Exception_parse_list(Exception):
    '''
    爬取搜索结果页面的条目异常
    '''
    def __init__(self, item):
        err = u'Exception_occured_in_parse_item:{0}'.format(item.get_text())
        Exception.__init__(self, err)
        PangolinLogger().error(err)
        
class Exception_parse_item(Exception):
    '''
    爬取结题页面异常
    '''
    def __init__(self, url, index):
        err = u'Exception_parse_item in url:{0} ({1})'.format(url,index)
        Exception.__init__(self, err)
        PangolinLogger().error(err)
        
#%%
class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {'Connection': 'Keep-Alive',
                        'Expect': '100-continue',
                        'User-Agent': 'ben'}
    def rk_create(self, im, im_type, timeout=60):
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.gif', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        print r.json()
        return r.json()
    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()