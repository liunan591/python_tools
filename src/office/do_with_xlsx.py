# -*- coding: utf-8 -*-
import xlsxwriter #pip install XlsxWriter
import pandas as pd

#%%xlswriter
"""
https://xlsxwriter.readthedocs.io/worksheet.html
"""

#定义文件对象
workbook = xlsxwriter.Workbook(file)
#定义表格对象 
worksheet = workbook.add_worksheet()
#定义单元格格式对象
formatter = workbook.add_format({"font_size": 8, 'border': 1, })#字号8，边框1像素
formatter2 = workbook.add_format({'bold': True,'fg_color': '#D7E4BC', })#加粗,浅绿背景色
formatter3 = workbook.add_format({'align': 'right','valign': 'vcenter'})#左对齐，垂直居中
# 合并单元格
worksheet.merge_range(first_row, first_col, last_row, last_col, data[, cell_format])
worksheet.merge_range('A1:K1', "title", formatter)
# 设置单元格宽度、高度
worksheet.set_column(first_col, last_col, width, cell_format, options)
worksheet.set_column(1, 3, 30)   # Columns B-D width set to 30.
worksheet.set_column('A:A', 3)  # Columns A width set to 3.
worksheet.set_row(row, height, cell_format, options)
worksheet.set_row(0, 20)  # Set the height of Row 1 to 20.
worksheet.set_row(0, 20, cell_format)   # Set the height of Row 1 to 20 and cell format.
#写入内容
worksheet.write(row, col, *args)
worksheet.write(1, 10, "Hello", title_formatter)
worksheet.write_row(row, col, data[, cell_format])
worksheet.write_row('A1', ('Foo', 'Bar', 'Baz')) #write A1 B1 C1
worksheet.write_column(row, col, data[, cell_format])
worksheet.write_column('A1', ('Foo', 'Bar', 'Baz')) #write A1 A2 A3
#写入图片到单元格
worksheet.insert_image(row, col, image[, options])
worksheet.insert_image('B2', 'python.png')
#打印相关设置
worksheet.center_horizontally() #设置打印时水平居中
worksheet.set_margins(left=0.393,right=0.393)#以英寸为单位设定页边距
worksheet.set_paper(9)  #设置使用A4纸张
worksheet.set_landscape()   #设置纸张为横向
#关闭文件写入
workbook.close()
    
#%%pandas with xlsxwriter
# Create a Pandas dataframe from some data.
df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('a.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer,startrow=1, sheet_name='Sheet1')
# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']
#do something wiht xlsx
#close
writer.save()