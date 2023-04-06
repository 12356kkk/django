# coding:utf-8
import MySQLdb
#connect() 方法用于创建数据库的连接，里面可以指定参数：用户名，密码，主机等信息。
#这只是连接到了数据库，要想操作数据库需要创建游标。
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345678',
        db ='data',
        charset='utf8'
        )

#通过获取到的数据库连接conn下的cursor()方法来创建游标。
cur = conn.cursor()

sql = "select city from table1"

cur.execute(query=sql)

number = cur.fetchall()

fp = open("./mapData/city.txt", "w" ,encoding='utf-8')
loan_count = 0
for loanNumber in number:
    loanNumber1 = loanNumber[0].encode('utf-8'). decode('utf-8')
    loanNumber1= str(loanNumber1)[0:2]
    if (loan_count == 149):
        fp.write(loanNumber1)
        break
    loan_count += 1
    print("***第"+str(loan_count)+"行写入成功***")
    fp.write(loanNumber1 + ",")
fp.close()

#cur.close() 关闭游标
cur.close()

#conn.close()关闭数据库连接
conn.close()