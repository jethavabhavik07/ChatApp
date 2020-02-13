import _thread
import ast
import datetime
import socket
import sys
import threading
import time

import redis

r_obj = redis.Redis(charset='utf-8', decode_responses=True)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
port = 8888
s.bind(('0.0.0.0', port))
global key


# name = ''

def menu():
    print("Please type 1-4 to execute : ")
    print("1. Add User")
    print("2. Get All Users")
    print("3. Start Chat")
    print("4. Chat history")
    print("5. Exit")


def add_user():
    name = input('Enter Name of the user you want to add : ')
    ip = input('Enter Ip address of the name mentioned : ')
    res = r_obj.hset('user_list', name, ip)
    return res


def get_user():
    usr = r_obj.hgetall('user_list')
    return usr


def chathistory(name):
    data = r_obj.lrange(name, 0, -1)
    data = reversed(data)
    for items in data:
        value = ast.literal_eval(items)
        # print(value)
        print(value['sender'] + '  =>  ' + value['timestamp'] + '  =>  ' + value['msg'])


def rec():
    while True:
        user = get_user()
        data, addr = s.recvfrom(1024)
        for k, v in user.items():
            if addr[0] == v:
                username = k
        print(username + " -> " + data.decode())
        t = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        data = {'sender': key, 'msg': data.decode(), 'timestamp': t}
        r_obj.lpush(key, str(data))


# def sender():
#     global key
#     user = get_user()
#     for k, v in user.items():
#         print(k + " : " + v)
#     key = input("User name to connect with..? \n")
#     connTo = user[key]
#     print("Connected to " + key)
#     # message = input("")
#     _thread.start_new_thread(rec(), ())
#     while True:
#         print('hello')
#         message = input("")
#         if message == 'bye':
#             break
#         else:
#             s.sendto(message.encode(), (connTo, port))
#             t = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
#             data = {'sender': 'bhavik', 'msg': message, 'timestamp': t}
#             r_obj.lpush(key, str(data))
#             # set_interval(rec, 1)
#             # a = input()


# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec)
#         func()
#
#     t = threading.Timer(sec, func_wrapper)
#     t.start()

def main():
    choice = 'y'
    try:
        while choice == 'y':
            menu()
            val = int(input("Enter Choice : "))
            if val == 1:
                print(add_user())
            elif val == 2:
                user = get_user()
                # print(user)
                for k, v in user.items():
                    print(k + " : " + v)
            elif val == 3:
                # threading.Thread(target=sender()).start()
                # sender()
                global key
                user = get_user()
                for k, v in user.items():
                    print(k + " : " + v)
                key = input("User name to connect with..? \n")
                connTo = user[key]
                print("Connected to " + key)
                # message = input("")
                _thread.start_new_thread(rec, ())
                while True:
                    try:
                        # print('hello')
                        message = input("")
                        s.sendto(message.encode(), (connTo, port))
                        t = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                        data = {'sender': 'bhavik', 'msg': message, 'timestamp': t}
                        r_obj.lpush(key, str(data))
                        # set_interval(rec, 1)
                        # a = input()
                    except KeyboardInterrupt:
                        print("Connection terminated")
                        break
            elif val == 4:
                ch = input("Enter name of sender: \n")
                chathistory(ch)
            elif val == 5:
                print('Thank You')
                sys.exit(0)
            else:
                pass
            choice = input("Do You want to continue....")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
