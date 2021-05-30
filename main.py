import socket
import asyncio
import threading
import time


class ServerWrapper:

    def __check_post(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', self.port)) == 0

    def __check_connection(self,host,port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, port)) == 0

    def __on_message(self,conn,addr):
        while True:
            data = conn.recv(1024)
            if not data :
                time.sleep(0.1)
            else:
                asyncio.run(self.onmessage(conn,data.decode('utf-8')))

            if self.__check_connection(addr[0],addr[1]):
                conn.close()
                break

    def __on_connect(self):
        while True:
            conn,addr = self.s.accept()
            asyncio.run(self.connect(conn,addr))
            c = threading.Thread(target=self.__on_message,args=(conn,addr,))
            c.start()




    def __init__(self,port=5033):
        self.port = port
        self.ip_address = socket.gethostbyname(socket.gethostname())
        if 'connect' not in dir(self):
            raise Exception('Method connect is missing')

        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((self.ip_address,self.port))
        self.s.listen()
        c = threading.Thread(target=self.__on_connect)
        c.start()



class TestServer(ServerWrapper):
    async def connect(self,conn,addr):
        conn.send(b'connected')

    async def onmessage(self,conn,msg):
        print(msg)
