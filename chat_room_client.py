"""
chat room
客户端
功能:发送请求,获取结果
"""

from socket import *
from multiprocessing import Process
import sys

# 服务器地址
ADDR=("127.0.0.1",8888)



# 聊天--接收消息
def revc_msg(s):
    while True:
        data,addr=s.recvfrom(4096)
        if data == b'Q':
            sys.exit("您已被管理员移除群聊")
        print(data.decode()+"\n发言:",end="")


# 聊天--发送消息
def send_msg(s,name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = 'quit'
        if text=='quit':
            msg='Q '+name
            s.sendto(msg.encode(),ADDR)#告知服务端
            sys.exit("退出聊天室")#进程结束
        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)



# 网络结构
def main():
    s=socket(AF_INET,SOCK_DGRAM)
    #进入聊天室
    while True:
        name = input("请输入姓名:")#1.输入姓名
        msg = "L "+name #根据协议组织消息格式
        s.sendto(msg.encode(),ADDR)#2.将姓名发送给服务端
        data,addr=s.recvfrom(128)#3.接收服务端的反馈结果
        if data.decode() == "OK":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    #创建一个新进程
    p=Process(target=revc_msg,args=(s,))
    p.daemon=True
    p.start()
    #发送消息
    send_msg(s,name) #发送消息由父进程执行
    p.join()




if __name__ == '__main__':
    main()

