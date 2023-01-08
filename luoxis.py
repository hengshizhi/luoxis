import go_cqhttpsdk as sdk
sdk = sdk.sdk()
import os
import json
import time
import requests
import cq as cq
import mysql
dbManager = mysql.MysqlManager(db='mysql_test', user='root', passwd='')
cq = cq.cqc()
try:
    from flask import Flask, redirect, url_for, request, render_template
except:
    os.system('pip3 install flask')
    from flask import Flask, redirect, url_for, request, render_template
try:
    from multiprocessing import Process, Pipe     # 导入模块
except:
    os.system('pip3 install multiprocessing')
    from multiprocessing import Process, Pipe     # 导入模块

def sendMessage(消息类型,qid,消息内容): #等价于 发送消息()
    if(消息类型 == 'private'):
        sdk.发送私聊消息(qid,'',消息内容)
    elif(消息类型 == 'group'):
        sdk.发送群消息(qid,消息内容)

def POCQCode(消息:str,CQ码类型:str): #等价于 挑出CQ码()
    消息 = 消息.split('[')
    cqdata = ''
    for i in 消息:
        if(CQ码类型 in i):
            cqdata = i
            break
    cqdata = '['+cqdata.split(']')[0]+']'
    return cqdata

def 发送消息(消息类型,qid,消息内容):
    if(消息类型 == 'private'):
        sdk.发送私聊消息(qid,'',消息内容)
    elif(消息类型 == 'group'):
        sdk.发送群消息(qid,消息内容)

def 挑出CQ码(消息:str,CQ码类型:str):
    消息 = 消息.split('[')
    cqdata = ''
    for i in 消息:
        if(CQ码类型 in i):
            cqdata = i
            break
    cqdata = '['+cqdata.split(']')[0]+']'
    return cqdata

def v(): #获取版本号
    v = '1.0a3' #版本号
    print('版本:v'+v)
    try:
        gv = requests.get('http://luoxistar.df100.ltd/blog/wp-content/uploads/2023/01/zuixin.txt').text
        print(gv)
        if(v == gv):
            print('您已是最新版本')
        else:
            print('您不是最新版本,请前往[http://luoxistar.df100.ltd/blog/index.php/luoxis%e6%a1%86%e6%9e%b6%e4%b8%8b%e8%bd%bd/]下载最新版本')
    except:
        print('最新版本号获取失败')
        #ListeningFunction,action,conn,ListeningValue,ActionValue
def event_listeners(ListeningFunction:object,conn:object,ListeningValue=None):  
    while True:
        data = conn.recv()
        if(ListeningFunction(ListeningValue,data)):
            break
    conn.close()
class event:
    process_list = list()
    conn1,conn2 = Pipe()

event = event()
class luoxis:
    luoxisN = 'luoxis' #机器人调用命令头
    communication_f = 'luoxis.communication()'
    c_port = 8980  #端口
    c_listen = False  #最大连接数
    data = '' #收到的消息
    c_state = 0  #socket开启状态
    EnableChineseVariables = False #启动新版中文变量,当UseLegacy==True时不可使用英文变量,EnableChineseVariables==None时中英混用
    SourceGroup = None #初始化
    MessageContent = None #初始化
    MessageSender = None #初始化
    MessageType = None #初始化
    Source = None #初始化
    def go(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', '', self.post_data,methods=["POST"])
        self.app.run(debug = True,port=5000)
        pass
    def post_data(self):
        self.data = request.get_json()
        if(self.EnableChineseVariables == True or self.EnableChineseVariables == None):
            try:
                try:
                    self.SourceGroup = int(self.data['group_id'])  #群消息来源
                except:
                    self.SourceGroup = None
                self.MessageContent = self.data['message'] #消息内容
                self.MessageSender = int(self.data['user_id']) #消息发送者
                self.MessageType = self.data['message_type'] #消息类型（私聊/群组）
                if(self.MessageType == 'private'): #消息来源，如果是群则写群号，如果是私聊则写对方QQ号
                    self.Source = self.MessageSender
                else:
                    self.Source = self.SourceGroup
                try:
                    self.消息源群 = self.SourceGroup  #群消息来源
                except:
                    self.消息源群 = None
                self.消息内容 = self.MessageContent #消息内容
                self.消息发送人 = self.MessageSender #消息发送者QQ号
                self.消息类型 = self.MessageType #消息类型（私聊/群组）
                if(self.消息类型 == 'private'): #消息来源，如果是群则写群号，如果是私聊则写对方QQ号
                    self.消息来源 = self.MessageSender
                else:
                    self.消息来源 = self.SourceGroup
                print('消息来源:',self.消息来源)
                print('消息发送者:',self.消息发送人)
                print('收到的信息:',self.消息内容)
                print('消息类型:',self.消息类型)
            except:
                pass
        else:
            try:
                try:
                    self.SourceGroup = int(self.data['group_id'])  #群消息来源
                except:
                    self.SourceGroup = None
                self.MessageContent = self.data['message'] #消息内容
                self.MessageSender = int(self.data['user_id']) #消息发送者
                self.MessageType = self.data['message_type'] #消息类型（私聊/群组）
                if(self.MessageType == 'private'): #消息来源，如果是群则写群号，如果是私聊则写对方QQ号
                    self.Source = self.MessageSender
                else:
                    self.Source = self.SourceGroup
                print('消息来源:',self.Source)
                print('消息发送者:',self.MessageSender)
                print('收到的信息:',self.MessageContent)
                print('消息类型:',self.MessageType)
            except:
                pass
        if(self.MessageContent != None):
            self.main()
            MessageList = [{'Source':self.Source, \
            'MessageSender':self.MessageSender, \
            'MessageContent':self.MessageContent, \
            'MessageType':self.MessageType}]
            event.conn1.send(MessageList) #发送消息内容给子进程
        self.SourceGroup = None
        self.MessageContent = None
        self.MessageSender = None
        self.MessageType = None
        self.Source = None
        return 'OK'
    def sendMessage(self,QQID:int,消息内容:str): #发送消息，自动判读消息类型
        if(self.MessageType == 'private'):
            sdk.发送私聊消息(QQID,'',消息内容)
        elif(self.MessageType == 'group'):
            sdk.发送群消息(QQID,消息内容)
    def ReplyMessage(self,回复消息内容:str) -> bool: #应答消息
        self.sendMessage(self.Source,回复消息内容)
        return True
    def POCQCodeOne(self:str,CQ码类型:str): #挑出一条消息的第一个CQ码
        self.MessageContent = self.MessageContent.split('[')
        cqdata = str()
        for i in self.MessageContent:
            if(CQ码类型 in i):
                cqdata = i
                break
        cqdata = '['+cqdata.split(']')[0]+']'
        return cqdata
    def When_the_message_is_this_send_this(self,so,Send_this) -> bool:
        if(self.MessageContent == so):
            self.ReplyMessage(Send_this)
        return True
    def When_the_message_has_this_send_this(self,so:list,Send_this) -> bool:
        if(self.MessageContent in so):
            self.ReplyMessage(Send_this)
        return True
    def event_listeners_go(self,ListeningFunction:object,ListeningValue) -> bool:
        '''
        ListeningFunction:事件监听的事件,当传入的对象返回True的时候就执行(object)
        ListeningValue:ListeniyngFunction函数的传值(只能有一个值,通常为列表)
        '''
        conn = event.conn2
        p = Process(target=event_listeners,args=(ListeningFunction,conn,ListeningValue))
        p.start()
        event.process_list.append(p)
        return True
    def main(self):
        pass

