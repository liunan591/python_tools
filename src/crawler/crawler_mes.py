import requests
import os

class Crawler_MES():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
               "Connection": "keep-alive"}
    cngh_file_list = {
            "备件库":"42954","工具库":"44232","材料库":"42344","检具库":"44243",
            "卧式车削":"42236","3/4轴铣削":"42238",#铣二
            "3+2与5轴铣削":"42240",#铣一
            "5坐标磨床":"42242",#安卡
            "零件班组":"42241",
            "普通磨组":"42305",
            "刀片组":"43684",
            "刀具钳工组":"42248","零件钳工":"44635",

            "包装班组":"44857","物流部":"44872",

            "外协":"42249","零件外协":"43691","创建外协采购单":"44056",

            "辅助区域":"44795",#暂未使用

            "质检":"42250","排产":"42378",

            "刀具设计":"42351","刀具工艺":"42350","刀具程序":"42349",
            "辅助工艺":"42713",
            "零件设计":"42347","零件工艺":"42352","零件程序":"42348",}
    def __init__(self):
        self.ses = requests.session()

    def get_info_for_slj(self):
        """获取转包装班组所需要的信息，产能规划（包装班组，质检班组）"""
        file_o1 = os.path.join(B,"包装班组.xlsx")
        file_o2 = os.path.join(B,"质检班组.xlsx")
        self.__get_file_form_cngh(Crawler_MES.cngh_file_list["包装班组"],file_o1)
        self.__get_file_form_cngh(Crawler_MES.cngh_file_list["质检"],file_o2)

    def __login(self):
        url = "http://172.16.100.101:8080/winway/login.do?lang=zh-CN&logout=true"
        data = {"userName":"winway@liunan","password":"ww2018"}
        login_info = self.ses.post(url, headers=Crawler_MES.headers, data=data)
        if not login_info.ok:
            raise Exception("log in failed 'MES'")

    def __get_file_form_cngh(self,file_id,file_o):
        """从产能规划中获取文件"""
        url = "http://172.16.100.101:8080/winway/showKapplanungfa.do"
        data = {"ppIdFb":file_id,"outputType":"XLSX"}
        file_get = self.ses.post(url, headers=Crawler_MES.headers, data=data)
        with open(file_o, 'wb') as file:
            file.write(file_get.content)


