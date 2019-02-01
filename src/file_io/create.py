# -*- coding: utf-8 -*-
#%%
import pandas as pd
import os
import xlsxwriter
import tkinter.messagebox
import datetime

#c_path = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(".")
for file in files:
    if file.startswith("产能规划"):
        file_d = file
    elif file.startswith("库存动态报告"):
        file_i = file
    elif file.startswith("单据概述"):
        file_order = file

def findTask(value):
    v = str(value)
    task = ""
    if "检验" in v:
        task = task + "检"
    if "清洗" in v:
        task = task + "洗"
    if "标刻" in v:
        task = task + "标"
    if "包装" in v:
        task = task + "包"
    if not task:
        task = value.iloc[0]
    return task

def write_df_to_xlsx(df,workbook,worksheet,start_row,start_column):
    # 定义数据formatter格式对象，设置边框加粗1像素
    """对于格式的设置，可以使用formatter = workbook.add_format({字典})的方式
    如果不知道字典中是什么内容，可以通过以下方式，获取提示（.set, 按tab键获取提示）
    formatter = workbook.add_format()
    formatter.set_border
    """
    formatter = workbook.add_format({"font_size":12,'border':1,})
    # 定义标题栏格式对象：边框加粗1像素，背景色为灰色，单元格内容居中、加粗
    title_formatter = workbook.add_format({'border':1,"font_size":12,'bold':True,})
    title_formatter2 = workbook.add_format({"font_size":12,'bold':True,'align':'right'})
    
    # 定义平均值栏数据格式对象：边框加粗1像素，数字按2位小数显示
    ave_formatter = workbook.add_format()
    ave_formatter.set_border(1)
    ave_formatter.set_num_format('0.00')
    
    #标题栏格式
    merge_format = workbook.add_format({
                        'bold':     True,
#                        'border':   1,
                        'align':    'center',#水平居中
                        'valign':   'vcenter',#垂直居中
                        "font_size":20,
#                        'fg_color': '#D7E4BC',#颜色填充
#                        "left":1
#                        "right":1
#                        "top":1
#                        "bottom":1
                    })
    #标题栏（合并）
    title = "物流部转包装班组原料清单"
    worksheet.merge_range('A1:J1', title, merge_format)
    
    #设置单元格宽度、高度
    """
    worksheet.set_column('C:C', 40)
    worksheet.set_row(0, 40)
    """
    worksheet.set_column('A:A', 4)
    worksheet.set_column('B:B', 8.5)
    worksheet.set_column('C:C', 24)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 5)
    worksheet.set_column('F:F', 7)
    worksheet.set_column('G:G', 20)
    worksheet.set_column('H:H', 24)
    worksheet.set_column('I:I', 10)
    worksheet.set_column('J:J', 10)
    worksheet.set_row(0, 40)
    
    worksheet.write(1, 0, "序号", title_formatter)
    for i in range(len(df)):
        for j in range(len(df.columns)):
            if i == 0:
                worksheet.write(i+1,j+start_column+1,df.columns[j],title_formatter)
            if j == 0:
                worksheet.write(i+start_row+1,j+start_column,str(i+1),formatter)
            worksheet.write(i+start_row+1,j+start_column+1,str(df.iloc[i][j]),formatter)
    worksheet.write(len(df)+4,7,"转交人：",title_formatter2)
    worksheet.write(len(df)+5,7,"转交时间：",title_formatter2)
    worksheet.write(len(df)+5,8,datetime.datetime.now().strftime('%y-%m-%d'),title_formatter2)
    workbook.close()
    
#%%
class SYQ_Deliver:
    def __init__(self,file_d,file_order):
        tasks = pd.read_excel(file_d,dtype = {'流转卡' : str}, encoding="gbk")
        orders = pd.read_excel(file_order, encoding="gbk")
        tasks = tasks[["流转卡","产品","说明","应有步骤","实际步骤"]]
        self.orders = orders[["单号","参考编号","客户"]]
        tasks["task"] = tasks["应有步骤"] + tasks["实际步骤"]
        donet = tasks.groupby(["流转卡"]).aggregate(findTask)
        temp = pd.DataFrame(donet)
        self.done = temp[["产品","说明","task"]]

    def file_input(self,file_i):
        tasks = pd.read_excel(file_i,dtype = {'目标流转卡' : str}, encoding="gbk")
        tasks = tasks[["目标订货合同号","目标流转卡","来源流转卡","产品","数量","注释","产品描述","用户"]]
        self.tasks = tasks
        self.missed = tasks[tasks["目标流转卡"].isna()]
        self.need = tasks[tasks["目标流转卡"].notna()]
#        self.need.set_index("目标流转卡",inplace=True)

    def lookup(self,file_i):
        self.file_input(file_i)
        info_b = self.tasks.join(self.done,on="目标流转卡", lsuffix="l",rsuffix="r")
        info_back = info_b.join(self.orders.set_index("单号"),on="目标订货合同号",lsuffix="l",rsuffix="r")
        return info_back

    def save_to(self,file_o,file_i):
        columns = {'目标流转卡':'目标流转', '产品l':'毛坯',"注释":"出库说明","产品描述":"毛坯名称",
                   "用户":"转交人","产品r":"成品","说明":"成品名称","task":"任务清单","参考编号":"加工号"}
        columns_need = ['目标流转','毛坯',"毛坯名称","数量","加工号","客户","成品","成品名称","任务清单"]
        content_t = self.lookup(file_i)
        content_t.rename(columns=columns,inplace=True)
        content = content_t[columns_need]
        if True in content.成品.isna():
            tkinter.messagebox.showwarning('警告','存在目标流转不存在的出库记录，请检查无成品对应的行信息进行修正')
        workbook = xlsxwriter.Workbook(file_o)
        worksheet = workbook.add_worksheet()
        write_df_to_xlsx(content,workbook,worksheet,1,0)


if __name__ == "__main__":
    test = SYQ_Deliver(file_d,file_order)
    test.save_to("done.xlsx",file_i)

#    result2.to_csv("done.csv")