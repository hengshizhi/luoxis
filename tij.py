import requests
class sdk:
    url = "http://127.0.0.1:5700"
    def get(self,终结点,myParams):
        url = self.url+终结点  #拼接终结点
        res = requests.get(url=url, params=myParams)  #发送给API请求
        print('GET:',url)
        return(res.text)  #返回请求的内容

    ## 发送私聊消息
    def send_private_msg(self,user_id=True,group_id=True,message=True,auto_escape=True):
        myParams = {}
        myParams['user_id'] = user_id
        myParams['group_id'] = group_id
        myParams['message'] = message
        myParams['auto_escape'] = auto_escape
        ret = self.get('/send_private_msg',myParams)
        return ret
    
    def 发送私聊消息(self,user_id="对方 QQ 号",group_id="主动发起临时会话时的来源群号(可选, 机器人本身必须是管理员/群主)",message="要发送的内容",auto_escape="消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效"):
        self.send_private_msg(user_id,group_id,message,auto_escape)
sdk = sdk()
def 搜歌(消息类型,消息来源):
    cq = f'[CQ:record,file=http://m10.music.126.net/20230103132402/ab6e1acd0eb07f02b29f214f429a03c3/ymusic/obj/w5zDlMODwrDDiGjCn8Ky/14053669782/4d5a/224b/7dfe/186896bc4d999692cbe91affc8e154a6.mp3]'
    发送消息(消息类型,消息来源,cq)

def 发送消息(消息类型,qid,消息内容):
    if(消息类型 == 'private'):
        sdk.发送私聊消息(qid,None,消息内容,None)
    elif(消息类型 == 'group'):
        sdk.发送群消息(qid,消息内容)

搜歌('private',3192145045)
#cq = '[CQ:record,file=http://m10.music.126.net/20230103124556/73f1985bb417bd58c17a8c2e6b218945/ymusic/obj/w5zDlMODwrDDiGjCn8Ky/14053669782/4d5a/224b/7dfe/186896bc4d999692cbe91affc8e154a6.mp3]'
#sdk.发送私聊消息(3192145045,None,cq,None)