import luoxis
class main(luoxis.luoxis):
    EnableChineseVariables = None
    def main(self):
        self.When_the_message_is_this_send_this(so='你好世界！',Send_this='hello world') #如果收到信息'傻逼',就发送傻逼
        if(self.MessageContent == '你好' or self.MessageContent == 'hello'):
            self.ReplyMessage('你好啊！')
        elif(luoxis.cq.at某人(2220514289) in self.MessageContent):
            self.ReplyMessage(luoxis.cq.at某人(self.消息发送人)+'干嘛艾特我家鸟儿')
        #self可以调用类方法
if __name__ == '__main__':  

    main = main()
    main.go()