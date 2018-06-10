import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
user='root', passwd=None, db='mysql')
cur = conn.cursor()
"""一个连接可以有很多个光标。一个光标跟踪一种状态（state）信息，比如跟踪数据库的
使用状态。如果你有多个数据库，且需要向所有数据库写内容，就需要多个光标来处理。
光标还会包含最后一次查询执行的结果"""
cur.execute("USE scraping")
cur.execute("SELECT * FROM pages WHERE id=1")
print(cur.fetchone())
cur.close()
conn.close()



