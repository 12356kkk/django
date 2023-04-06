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

sql = "select salary from table1"

cur.execute(query=sql)
number = cur.fetchall()

fp = open("./mapData/salary.txt", "w" ,encoding='utf-8')
loan_count = 0
for loanNumber in number:
    loanNumber1 = loanNumber[0].encode('utf-8'). decode('utf-8')
    loanNumber1 = str(loanNumber1[:])
    if (len(loanNumber1)==0):
        continue
    elif (id(loanNumber1[1])!=id('.')):
        b = loanNumber1[1:]
        loanNumber1 = loanNumber1[0] + '.0' + b
        if (id(loanNumber1[5]) != id('.')):
            d = loanNumber1[5:]
            loanNumber1 = loanNumber1[0:5] + '.0' + d
    elif (id(loanNumber1[5])!=id('.')):
        d = loanNumber1[5:]
        loanNumber1 = loanNumber1[0:5] + '.0' + d
    if (loan_count == 99):
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