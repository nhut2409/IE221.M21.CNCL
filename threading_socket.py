import threading
import socket


class Threading_socket():
    def __init__(self, gui):
        self.dataReceive = ""
        self.conn = None
        self.gui = gui
        self.name = ""

    def clientAction(self, inputIP):
        self.name = "client"
        print("client connect ...............")
        HOST = inputIP  # Cấu hình địa chỉ server
        PORT = 8000              # Cấu hình Port sử dụng
        self.conn = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # Cấu hình socket
        self.conn.connect((HOST, PORT))  # tiến hành kết nối đến server
        self.gui.notification("Đã kết nối tới", str(HOST))
        t1 = threading.Thread(target=self.client)  # tạo luồng chạy client
        t1.start()

    def client(self):
        while True:
            self.dataReceive = self.conn.recv(
                1024).decode()  # Đọc dữ liệu server trả về
            if(self.dataReceive != ""):
                friend = self.dataReceive.split("|")[0]
                action = self.dataReceive.split("|")[1]
                if(action == "hit" and friend == "server"):
                    x = int(self.dataReceive.split("|")[2])
                    y = int(self.dataReceive.split("|")[3])
                    self.gui.handleButton(x, y)
                if(action == "Undo" and friend == "server"):
                    self.gui.Undo(False)
                if (action == "newgame" and friend == "server"):
                    self.gui.newGame(False)
            self.dataReceive = ""

    def serverAction(self):
        self.name = "server"
        HOST = socket.gethostbyname(socket.gethostname())  # Láy  lập địa chỉ
        print("Make host.........." + HOST)
        self.gui.notification("Gui IP chp ban", str(HOST))
        PORT = 8000  # Thiết lập port lắng nghe
        # cấu hình kết nối
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))  # lắng nghe
        s.listen(1)  # thiết lập tối ta 1 kết nối đồng thời
        self.conn, addr = s.accept()  # chấp nhận kết nối và trả về thông số
        t2 = threading.Thread(target=self.server, args=(addr, s))
        t2.start()

    def server(self, addr, s):
        try:
            # in ra thông địa chỉ của client
            print('Connected by', addr)
            while True:
                # Đọc nội dung client gửi đến
                self.dataReceive = self.conn.recv(1024).decode()
                if(self.dataReceive != ""):
                    friend = self.dataReceive.split("|")[0]
                    action = self.dataReceive.split("|")[1]
                    print(action)
                    if(action == "hit" and friend == "client"):
                        x = int(self.dataReceive.split("|")[2])
                        y = int(self.dataReceive.split("|")[3])
                        self.gui.handleButton(x, y)
                    if(action == "Undo" and friend == "client"):
                        self.gui.Undo(False)
                    if(action == "newgame" and friend == "client"):
                        self.gui.newGame(False)
                self.dataReceive = ""
        finally:
            s.close()  # đóng socket

    def sendData(self, data):
        # Gửi dữ liệu lên server`
        self.conn.sendall(str("{}|".format(self.name) + data).encode())