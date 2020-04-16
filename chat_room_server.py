"""
    群聊聊天室 服务端

chat room
env:python3+
socket udp and process
"""

from socket import *
from multiprocessing import Process

# 服务器地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)
text_list=["xx","aa","bb","oo"]
# 用户信息存储 {name:address}
dict_user={}
list_baned=[]
count=1
#处理进入聊天室
def do_login(s,name,address):
    """
    进入聊天室
    :param s: 服务端套接字
    :param name: 从客户端获得的用户名
    :param address: 客户端地址
    :return:
    """
    if address not in list_baned:
        if name in dict_user or "管理" in name:
            s.sendto("该用户名已经存在".encode(),address)
            return
        else:
            s.sendto(b'OK',address)
            #告知其他用户
            msg = "\n欢迎 %s 进入聊天室" % name
            for i in dict_user:
                s.sendto(msg.encode(),dict_user[i])
            dict_user[name] = address #用户字典中增加一项
    else:
        s.sendto("您被拒绝访问".encode(),address)



#处理聊天
def do_chat(s,name,text):
    """
    聊天处理
    通过全局变量dict_user字典的key键name获得该用户地址给其他客户端返回消息
    :param s: 服务端套接字
    :param name: 从客户端获得的用户名
    :param text: 从客户端获得的发送消息
    :return:
    """
    global count
    if text in text_list:
        for i in dict_user:
            msg="\n警告%s 聊天内容中包含敏感词汇,第%d次!"%(name,count)
            if count ==3:
                msg ="\n %s已经被强制退出群聊"%name
                list_baned.append(dict_user)
                s.sendto(b'Q',dict_user[name])
                count =1
            s.sendto(msg.encode(), dict_user[i])
            count+=1
    msg = "\n%s:%s"%(name,text)
    for i in dict_user:
        if i!=name:
            s.sendto(msg.encode(),dict_user[i])

# 处理退出
def do_quit(s, name):
    """
    处理退出
    通过全局变量dict_user字典的key键name获得该用户地址给其他客户端返回消息
    :param s:
    :param name:
    :return:
    """
    del dict_user[name]
    msg = "\n%s 退出聊天室" % name
    for i in dict_user:
        s.sendto(msg.encode(), dict_user[i])


# 接收各个客户端请求
def request(s):
    """
    总分模式
    1.接收不同的客户端请求类型
    2.分情况讨论
    3.不同的情况调用不同的封装方法
    4.每个封装功能设计参考 学的函数或者类的设计过程
    5.根据不同的需求创建 相应协议(如 进入聊天室L 聊天C 退出Q)
    :param s:
    :return:
    """
    while True:
        data,addr=s.recvfrom(1024) #接收请求
        tmp = data.decode().split(" ",2) #对请求的处理 通过拆分获得所需信息
        if tmp[0] == "L":
            #处理进入聊天室 tmp --> ['L','name']
            do_login(s,tmp[1],addr)
        elif tmp[0] == "C":
            # 处理进入聊天室 tmp --> ['L','name','XXX']
            do_chat(s,tmp[1],tmp[2])
        elif tmp[0] == "Q":
            #处理退出
            do_quit(s,tmp[1])


# 管理员消息
def manager(s):
    """
    管理员消息处理
    通过和子进程进行进行消息传输 发送给所有客户端消息
    :param s:
    :return:
    """
    while True:
        msg=input("管理员消息:")
        msg="C 管理员 "+msg
        s.sendto(msg.encode(),ADDR)#从父进程发送给子进程

# 搭建基本结构
def main():
    """
    主函数
    在主函数内创建套接字和进程对象
    :return:
    """
    # 创建UDP套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)


    # 创建新进程用于给管理员发送消息
    p=Process(target=request,args=(s,))
    p.start()
    manager(s)  # 处理发过来的请求
    p.join()


if __name__ == '__main__':
    main()




