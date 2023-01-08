try:
    import pymysql
except:
    import os
    os.system('pip3 install pymysql')
    import pymysql

# host = 'localhost'  #数据库地址
# port = 3306   #数据库端口
# db = 'mysql_test'  #数据库名
# user = 'root'  #数据库用户名
# password = ''  #数据库密码

# ---- 用pymysql 操作数据库
# def get_connection():
#     conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
#     return conn

# def sql(sql):
#     db = get_connection()
#     cursor = db.cursor()
#     cursor.execute(sql)
#     db.commit()
#     db.close()
#     return cursor.fetchone()
#     #print(check_it(sql))

# def sqls(sql):
#     data = list()
#     db = get_connection()
#     cursor = db.cursor()
#     cursor.execute(sql)
#     db.commit()
#     db.close()   
#     rest=cursor.fetchall()
#     for i in rest:
#         data.append(i)
#     return data

class MysqlManager(object):
    """
    mysql管理器
    """
 
    def __init__(self, db, user, passwd, host='localhost', port=3306, charset='utf8'):
        """
        数据库配置
        :param db:              数据库名字
        :param user:            链接的用户名
        :param passwd:          链接的密码
        :param host:            IP地址默认是：127.0.0.1  localhost
        :param port:            端口默认：3306 可修改
        :param charset:         默认转码：utf8
        """
        self.__db = db
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__port = port
        self.__charset = charset
        self.__connect = None
        self.__cursor = None
 
    def connect_db(self):
        """
        dbManager._connect_db()
        连接数据库
        :return:
        """
 
        params = pymysql.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__passwd,
            database=self.__db,
            use_unicode=True,
            charset=self.__charset
        )
 
        self.__connect = params
        self.__cursor = self.__connect.cursor()
 
    def Close_DB(self):
        """
        dbManager._close_db()
        :return:
        """
        self.__cursor.close()
        self.__connect.close()
 
    def Establish_DB(self, DB_name):
        """
        创建数据库
        :param DB_name: 创建的数据库名字
        :return:
        """
        self.connect_db()
        try:
            self.__cursor.execute("CREATE DATABASE %S" % DB_name)
        except Exception as e:
            print('创建数据库失败，失败原因：', e)
        else:
            print('数据库创建成功')
 
    def Establish_table(self, surface_name, condition):
        """
        创建表
        :param surface_name: 要创建的表名字
        :param condition: 要创建表的条件
        :return:
        """
        self.connect_db()
        try:
            create_table = "CREATE TABLE {table_name} ({value})".format(table_name=surface_name,value=condition)
            self.__cursor.execute(create_table)
        except Exception as e:
            print("创建表失败：",e)
        else:
            print("创建表成功")
 
 
    def Insert_DB(self, table_name, insert_data):
        """
        DBManager.insert(table, insert_data)
        :param table_name: str --> table 为字符串
        :param insert_data: [a:b] --> 为列表中嵌套字典类型
        :return:
        """
        # 用户传入数据自读那列表数据，根据key, value 添加进数据库
        # 连接数据库
        self.connect_db()
        try:
            data = self.Handle_value(insert_data)
            key = data[0]
            value = data[1]
            sql = "INSERT INTO {table_name}({key}) values ({values})".format(table_name=table_name, key=key,
                                                                             values=value)
            self.__cursor.execute(sql)
            self.__connect.commit()
 
        except Exception as e:
            print('数据插入失败，失败原因：', e)
        else:
            self.Close_DB()
            print('数据插入成功')
 
    def Delete(self, table_name, condition):
        """
        dbManager.delete(table, condition)
        传入相应的条件 -- > 删除数据库中的数据
        :param table_name: 表名
        :param condition: 传入条件
        :return:
        """
        self.connect_db()
        condition_Text = ' and '.join(self.Handle_value(condition))
        try:
            # 构建sql语句
            sql = "DELETE FROM {table_name} WHERE {condition}".format(table_name=table_name, condition=condition_Text)
            self.__cursor.execute(sql)
            self.__connect.commit()
        except Exception as e:
            print('删除失败：', e)
        else:
            self.Close_DB()
            print('删除成功')
 
    def Update(self, table_name, data, condition=None):
        """
        dbManager.update(table, date,condition)
        :param table_name: 表名
        :param data: dict -> data 字典类型
        :param condition: dict -> condition 字典类型
        :return:
        """
        self.connect_db()
        update_data = ','.join(self.Handle_value(data))
        try:
            if condition is not None:
                # 处理传入的条件
                condition_data = ' and '.join(self.Handle_value(condition))
                sql = "UPDATE {table} SET {values} WHERE {conditions}".format(table=table_name, values=update_data,
                                                                              conditions=condition_data)
            else:
                sql = "UPDATE {table} SET {values}".format(table=table_name, values=update_data)
            self.__cursor.execute(sql)
            self.__connect.commit()
        except Exception as e:
            print('更新失败：', e)
        else:
            self.Close_DB()
            print('更新成功')
 
    def Select_DB(self, table_name, show_ist, condition=None, get_one=False):
        """
        查数据
        :param table_name: --> str 字符串类型
        :param show_ist: --> 列表类型
        :param condition: --> 字典类型
        :param get_one: --> 布尔类型
        :return:
        """
        self.connect_db()
        # 处理显示的数据
        shou_list = ','.join(show_ist)
        try:
            if condition is not None:
                condition_list = self.Handle_value(condition)
                condition_data = ' and '.join(condition_list)
                sql = "SELECT {key} FROM {table} WHERE {values}".format(key=shou_list, table=table_name,
                                                                        values=condition_data)
            else:
                sql = "SELECT {key} FROM {table}".format(key=shou_list, table=table_name)
 
            self.__cursor.execute(sql)
            result = list()
            for i in self.__cursor.fetchall():
                result.append(i)
                
        except Exception as e:
            print("查询失败：", e)
        else:
            self.Close_DB()
            print("查询成功")
        return result
    # todo 处理传进来的Value
    def Handle_value(self, value):
        """
        处理传进来的value
        self.deal_values(value) --> str or list
        :param value: 传进来的value
        :return:
        """
        result = []
        for k, v in value[0].items():
            if isinstance(k, int):
                if k == 0:
                    content_KEY = []
                    content_VALUE = []
                    for vs in v:
                        for kx, vx in vs.items():
                            value = self.handel_text(value=vx, ks=k)
                            content_KEY.append(str(kx))
                            content_VALUE.append(value)
                    condition_key = ','.join(content_KEY)
                    condition_value = ','.join(content_VALUE)
                    return condition_key, condition_value
                else:
                    for vs in v:
                        for kx, vx in vs.items():
                            res = self.handel_text(key=kx, value=vx, ks=k)
                            result.append(res)
 
        return result
 
    def handel_text(self, value, ks, key=None):
        """
        处理进来的条件
        :param key: 传进来的Key
        :param value: 传进来的Value
        :param ks 传进来的K值
        :return:
        """
        condition = self.Judeg_parameter(ks)
        if isinstance(value, str):
            v = ("'{value}'".format(value=value))
        else:
            v = str(value)
        if ks == 0:
            return v
        else:
            return "{key}{condition}{value}".format(key=key, condition=condition, value=v)
 
    def Judeg_parameter(self, judeg_structure):
        if judeg_structure == 1:
            return "="
        elif judeg_structure == 2:
            return ">"
        elif judeg_structure == 3:
            return "<"
        elif judeg_structure == 4:
            return ">="
        elif judeg_structure == 5:
            return "<="
 
 
def 增(dbManager,表名:str,insert_data):
    '''
     0 代表是插入数据，因为插入数据和 其他 查询 修改 更新数据条件不一样
    insert_data = [{
        0: [
            {"name": 'GFGF'},
            {"age": 3333},
            {"sex": 1}
        ]
    }]
    '''
    # 增
    return dbManager.Insert_DB(table_name=表名, insert_data=insert_data)
 
 
def 删(dbManager,表名:str,WHERE):
    # 删
    # 如果 条件很多 就在字典里加条件就可以，如果只有一条数据，就写一个字典就好
    # 0 没有任何条件
    # 1 是 = 号
    # 2 是 > 号
    # 剩下具体看 Judeg_parameter方法
    '''
    WHERE = [{
        1: [{
            "name": 'FFFF',
            "sex": 13
        }],
        2: [{
            "age": 300
        }]
    }]
    '''
    return dbManager.Delete(table_name=表名, condition=WHERE)
 
 
def 改(dbManager,表名,数据,WHERE=None):
    # 改
    # 一个是带处理条件的查询，一个是不带处理条件的查询
    # 0 没有任何条件
    # 1 是 = 号
    # 2 是 > 号
    # 剩下具体看 Judeg_parameter方法
    '''
    WHERE = [{
        1: [{
            "ID": 10,
            "name": "RRR"
        }]
    }]
    数据 = [{
        1: [{
            "name": 'TTT',
            "sex": 6
        }]
    }]
    '''
    return dbManager.Update(table_name=表名, condition=WHERE, data=数据)
    # dbManager.Update(table_name='user', data=data)                # 这个是直接修改某个表里面 字段的所有参数
 
 
def 查(dbManager,表名:str,字段:list,WHERE=None):
    """
    condition: 传入None 则没有查询条件， 传入查询条件，则查询传入条件的规则
    get_one: 查询是否查一条 还是查询所有 False 是符合条件的所有东西  True是查符合条件的一条数据
    字段 = ['用户名','密码']
    WHERE = [{
        1: [{
            "ID": 4,
            "name": "DDD"
        }]
    }]
    """
    return dbManager.Select_DB(table_name=表名, show_ist=字段, condition=WHERE, get_one=True)
 
 
if __name__ == '__main__':
    '''
    下面是增删改查的所有使用方法
    因为可以添加多种查询条件，所以 在传入值的时候会稍微复杂一点点，但也不难明白
    [{
        0: [
            {"name": 'GFGF'},
            {"age": 3333},
            {"sex": 1}
        ],
        1: [
            {"name": 'GFGF'},
            {"age": 3333},
            {"sex": 1}
        ]
    }]
    可能是这样是数据结构。 这个KEY = 0 或者 1 是什么意思呢？？
    它就是传入条件 比如 某个条件可能 xx > 1 and ff = '某某某' 
    1 2 3 4 5 这些是用来区分 = > < 符号的，具体看 Judeg_parameter 这个方法。什么对应什么
    
    插数据是因为只需要字符串就可以，所以做特殊处理。用 0 表示
    
    下面 每个方法 删 改 查 都有写 怎么使用
    '''
    # db = 'mysql_test' #数据库名
    # user = 'root' #用户
    # passwd = '' #密码
    # dbManager = MysqlManager(db='mysql_test', user='root', passwd='')
    # print(查(dbManager=dbManager,表名='消息记录',字段=['*'],WHERE=[{1:[{'信息发送者':'127'}]}]))
    # print(删(dbManager=dbManager,表名='消息记录',WHERE=[{1:[{'信息发送者':'127'}]}]))
    '''
    PRIMARY KEY AUTO_INCREMENT    这句话的意思是 把这个字段设置成主KEY  并且自增长
    VARCHAR(255)                  字符串类型 长度 255
    '''
    # condition = "ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,name VARCHAR(255),sex INT,age INT"
    # dbManager.Establish_table(surface_name='user', condition=condition)