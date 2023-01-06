try:
    import pymysql
except:
    import os
    os.system('pip3 install pymysql')
    import pymysql
host = 'localhost'  #数据库地址
port = 3306   #数据库端口
db = 'mysql_test'  #数据库名
user = 'root'  #数据库用户名
password = ''  #数据库密码

# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn

def sql(sql):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return cursor.fetchone()
    #print(check_it(sql))

def sqls(sql):
    data = list()
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()   
    rest=cursor.fetchall()
    for i in rest:
        data.append(i)
    return data
