import luoxis
def task(ListeningValue,data) -> bool:
    # data = [{'Source':self.Source, \
    #         'MessageSender':self.MessageSender, \
    #         'MessageContent':self.MessageContent, \
    #         'MessageType':self.MessageType}]
    data = data[0]
    if(ListeningValue == data['MessageSender']):
        if(data['MessageContent'] == '创建任务'):
            luoxis.sendMessage(data['MessageType'],data['Source'],'请问您要创建什么任务')
        elif(data['MessageContent'] == '发送创建任务成功'):
            luoxis.sendMessage(data['MessageType'],data['Source'],'执行任务成功(发送这条信息就是任务本身)')
            return True #停止任务
class main(luoxis.luoxis):
    EnableChineseVariables = None
    def main(self):
        self.When_the_message_is_this_send_this(so='你好世界！',Send_this='hello world') #如果收到信息'傻逼',就发送傻逼
        if(self.MessageContent == '你好' or self.MessageContent == 'hello'):
            self.ReplyMessage('你好啊！')
        elif(luoxis.cq.at某人(2220514289) in self.MessageContent):
            self.ReplyMessage(luoxis.cq.at某人(self.消息发送人)+'干嘛艾特我家鸟儿')
        if(self.MessageContent == '创建任务'):
            self.event_listeners_go(ListeningFunction=task,ListeningValue=self.MessageSender) #创建任务
        #self可以调用类方法
if __name__ == '__main__':  
    main = main()
    main.go()

