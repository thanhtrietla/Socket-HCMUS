import tkinter as Tk
import socket
import threading
import json
import time

from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import lxml

# Lấy địa chỉ IP của máy Server
HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)

PORT = 65432
FORMAT = "utf8"
# Thời gian update (60 phút)
TIME = 60

# Ứng dụng
class App(Tk.Tk):
    def __init__(self):
        Tk.Tk.__init__(self)

        # Giao diện 
        self.title("Server")
        self.geometry("500x500")
        self.configure(bg = "#ffffff")
        self.resizable(width = False, height = False)

        self.canvas = Tk.Canvas(self, bg = "#ffffff", height = 500, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = Tk.PhotoImage(file = f"ServerBackground.png")
        self.canvas.create_image(250.0, 251.5, image = self.background_img)

        self.canvas.create_text(250.0, 50.5, text = "Server IP Address: " + HOST, fill = "#E36D6D", font = ("OpenSans-Bold", int(10.0)))
        self.canvas.create_text(250.0, 80.5, text = "CLIENTS STATUS", fill = "#E36D6D", font = ("OpenSans-Bold", int(20.0)))

        # Bảng trạng thái
        self.conent = Tk.Frame(self)
        self.status = Tk.Listbox(self.conent, height = 20, width = 70)
        self.conent.pack_configure(padx = 50, pady = 100)
        self.scroll = Tk.Scrollbar(self.conent)
        self.scroll.pack(side = 'right', fill = 'both')
        self.status.config(yscrollcommand = self.scroll.set)
        self.scroll.config(command = self.status.yview)
        self.status.pack()

        # Nút đóng Server
        self.closeButtonImg = Tk.PhotoImage(file = f"CloseButton.png")
        closeButton = Tk.Button(image = self.closeButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: closeServer(), relief = "flat")
        closeButton.place(x = 212, y = 428, width = 76, height = 16)

        # Các hàm chức năng
        # Đăng ký
        def handleClientSignUp(connection, nClient, clientStatus):
            # Nhận Username
            username = connection.recv(1024).decode(FORMAT)
           
            # Kiểm tra Username có tồn tại chưa
            with open('Accounts.json') as accountData:
                accountList = json.load(accountData)
            accountData.close()

            usernameList = []
            for account in accountList['accounts']:
                usernameList.append(account['username'])

            # Nếu có thì gửi phản hồi đã tồn tại cho Client
            if username in usernameList:
                connection.sendall('Exist'.encode(FORMAT))
                return
                
            # Nếu không gửi phản hồi đúng cho Client
            connection.sendall('True'.encode(FORMAT))
            # Nhận Password
            password = connection.recv(1024).decode(FORMAT)

            # Thêm tài khoản mới vào dữ liệu
            newAccount = {"username": username, "password": password}
            accountList['accounts'].append(newAccount)

            with open('Accounts.json', 'w') as accountData:
                json.dump(accountList, accountData, indent = 2)
            accountData.close()

            tmp = "Client " + str(nClient) + " has signed up with username: " + username
            clientStatus.append(tmp)

        # Đăng nhập
        def handleClientLogin(connection, nClient, onlineClient, clientStatus):
            # Nhận Username và Password
            username = connection.recv(1024).decode(FORMAT)
            connection.sendall(username.encode(FORMAT))
            password = connection.recv(1024).decode(FORMAT)
            
            # Kiểm tra tài khoản đã được đăng nhập chưa
            if username in onlineClient:
                connection.sendall('Exist'.encode(FORMAT))
                return None

            # Kiểm tra tài khoản có trong dữ liệu hay không
            with open('Accounts.json') as accountData:
                accountList = json.load(accountData)
            accountData.close()

            clientAccount = {"username": username, "password": password}

            # Nếu không thì gửi phản hồi sai cho Client
            if clientAccount not in accountList['accounts']:
                connection.sendall('False'.encode(FORMAT))
                return None
            
            # Nếu có thì gửi phản hồi đúng cho Client
            connection.sendall('True'.encode(FORMAT))
            
            # Thêm tài khoản vừa đăng nhập vào danh sách đang đăng nhập
            onlineClient.append(username)

            tmp = "Client " + str(nClient) + " has logged in as: " + username
            clientStatus.append(tmp)

            # Trả về Username để hiển thị ở các trạng thái tiếp theo
            return username

        # Tra cứu
        def handleClientLookUp(connection, nClient, clientStatus, usingAccount):
            # Nhận tên tỉnh và ngày từ Client
            date = connection.recv(1024).decode(FORMAT)
            connection.sendall(date.encode(FORMAT))
            province = connection.recv(1024).decode(FORMAT)
            
            # Nếu Client bỏ trống ngày thì sử dụng file TongSoCa.json để lấy thông tin tổng số ca
            if date == "None": json1_file = open("TongSoCa.json")
            # Nếu không thì sử dụng file date.json để lấy thông tin số ca mắc mới trong ngày đó
            else: 
                try: json1_file = open(date + '.json')
                # Nếu ngày nhập vào không hợp lệ hoặc không có thì gửi phản hồi sai cho Client
                except:
                   connection.sendall('False'.encode(FORMAT))
                   return

            # Xử lý file để lấy thông tin số ca mắc
            json1_str = json1_file.read()
            json1_data = json.loads(json1_str)

            # Nếu tên tỉnh có tồn tại trong file vừa lấy thì gửi phản hồi đúng cho Client
            if province in json1_data:
                connection.sendall('True'.encode(FORMAT))
                connection.recv(1024).decode(FORMAT)
                # Gửi số ca mắc cho Client
                cases = json1_data[province]  # gán số ca vào biến
                connection.sendall(cases.encode(FORMAT))
            # Nếu không thì gửi phản hồi sai cho Client
            else:
                connection.sendall('False'.encode(FORMAT))  
                return
            
            if date == "None": tmp = usingAccount + " has searched for total cases in " + province
            else: tmp = usingAccount + " has searched for new cases in " + province + " in " + date
            clientStatus.append(tmp)
        
        # Hàm quản lý Client
        def handleClient(connection, address, nClient, onlineClient, clientStatus):
            tmp = "Connected by Client " + str(nClient) + ": " +  str(address)
            clientStatus.append(tmp)

            # Tài khoản đang sử dụng
            usingAccount = None
            while True:
                # Cập nhật trạng thái Client
                updateClientStatus(clientStatus)
                try:
                    # Nhận yêu cầu từ Client
                    message = connection.recv(1024).decode(FORMAT)

                    # Đăng ký
                    if message == "Sign up":
                        connection.sendall(message.encode(FORMAT))
                        handleClientSignUp(connection, nClient, clientStatus)                   

                    # Đăng nhập
                    elif message == "Login":
                        connection.sendall(message.encode(FORMAT))
                        # Tài khoản Client vừa đăng nhập
                        usingAccount = handleClientLogin(connection, nClient, onlineClient, clientStatus)

                    # Đăng xuất
                    elif message == "Logout":
                        # Xóa tài khoản đang sử dụng khỏi danh sách
                        onlineClient.remove(usingAccount)
                        tmp = usingAccount + " has logged out"
                        clientStatus.append(tmp)

                    # Tra cứu
                    elif message == "Look up":
                        connection.sendall(message.encode(FORMAT))
                        handleClientLookUp(connection, nClient, clientStatus, usingAccount)

                    # Thoát
                    elif message == "Exit":
                        # Nếu có tài khoản đăng nhập thì xóa khỏi danh sách
                        if usingAccount in onlineClient: onlineClient.remove(usingAccount)

                        tmp = "Client " + str(nClient) + " has disconnected."
                        clientStatus.append(tmp)
                        updateClientStatus(clientStatus)
                        connection.close()
                        break

                # Nếu Client mất kết nối đột ngột
                except:
                    tmp = "Client " + str(nClient) + " might be forcibly disconnected!"
                    if usingAccount in onlineClient: onlineClient.remove(usingAccount)
                    clientStatus.append(tmp)
                    updateClientStatus(clientStatus)
                    connection.close()
                    break

        # Hàm in cập nhật hoạt động của Client
        def updateClientStatus(clientStatus):
            self.status.delete(0, len(clientStatus))
            for i in clientStatus:
                self.status.insert(clientStatus.index(i), i)
        
        # Hàm chuyển dataframe thành json
        def writeToJson(frame, fileName):
            df1 = dict(frame.values)
            JS = json.dumps(df1, indent=0)
            with open(fileName, "w") as outfile:
                outfile.write(JS)
        
        # Hàm lấy dữ liệu
        def getData():
            # Lấy thông tin tổng số ca từ url web về
            url1 = 'https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19_t%E1%BA%A1i_Vi%E1%BB%87t_Nam'
            options = ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(url1)

            # tạo soup, tìm bảng
            time.sleep(5)
            soup1 = BeautifulSoup(driver.page_source, 'lxml')

            tables = soup1.find(
                'table', class_='wikitable plainrowheaders sortable tpl-blanktable jquery-tablesorter')

            # lập cột
            provinces = []
            cases = []
            deaths = []
            # tìm data
            for row in tables.findAll('tr'):
                cells = row.find_all('td')
                if len(cells) > 1:
                    province = cells[0]
                    provinces.append(province.text.strip())  # lấy cột tỉnh

                    case = cells[1]
                    cases.append(case.text.strip().replace(',', '.'))  # cột ca nhiễm

                    death = cells[2]
                    deaths.append(death.text.strip())  # cột người chết

            # lập list để tạo dataframe
            data = {'Tỉnh': provinces, 'Số ca nhiễm': cases}

            # lập data frame
            df_1 = pd.DataFrame(data)
            file_name = "TongSoCa.json"

            writeToJson(df_1, file_name)

            # Lấy hết tất cả các url chứa thông tin cần lấy
            urls = ['https://covid19.gov.vn/timelinebigstory/1d44b380-0adb-11ec-bf1c-e9c9e7c491f4/1.htm',
                    'https://covid19.gov.vn/timelinebigstory/1d44b380-0adb-11ec-bf1c-e9c9e7c491f4/2.htm',
                    'https://covid19.gov.vn/timelinebigstory/1d44b380-0adb-11ec-bf1c-e9c9e7c491f4/3.htm']

            # Bắt đầu scrape
            for url in urls:  # chạy vòng lặp duyệt từng url
                response = requests.get(url)
                html = response.text

                # Find all the tags in which the data is stored.
                soup = BeautifulSoup(html, 'lxml')
                lists = soup.find_all('li')

                for list in lists:
                    # lấy thông tin ngày tháng
                    dt = list.find('div', class_='timeago').text.strip()
                    # xoá 6 chữ cái đầu -> in được ngày tháng dạng dd-mm-yy
                    date = dt[6:].replace('/', '-')
                    filename = date + ".json"  # tạo tên file để lát nữa xuất file json dưới tên này

                    p_tags = list.find_all('p')
                    for p in p_tags[1:2]:  # find all p tag and exclude the first one and the third
                        s = p.text.replace('Các tỉnh, thành phố ghi nhận ca bệnh như sau: ', '')  # làm đẹp dữ liệu vừa lấy

                    # chỉnh lại dữ liệu để lát nữa dễ extract
                    s = s.replace('(', ',').replace(')', '').strip()
                    my_list = s.split(",")
                    # print(my_list)

                    TinhThanh = my_list[::2]  # List tỉnh thành
                    SoCa = my_list[1::2]  # lIST SỐ CA

                    # xoá hết khoảng trắng của các phần tử trong list
                    TinhThanh = [x.strip(' ') for x in TinhThanh]
                    SoCa = [x.strip(' ') for x in SoCa]

                    # Tạo dataframe từ dữ liệu TinhThanh, SoCa
                    pd.set_option('display.max_rows', 1000)
                    df = pd.DataFrame({'Tỉnh': TinhThanh, 'Số Ca': SoCa})
                    # In ra file json
                    writeToJson(df, filename)
        
        # Hàm cập nhật dữ liệu
        def updateData():
            while True:
                getData()
                time.sleep(60*TIME)

        # Đóng Server
        def closeServer(): self.destroy()

        # Hàm chạy Server
        def runServer():
            # Số thứ tự Client
            nClient = 1

            # Danh sách Client đang đăng nhập
            onlineClient = []

            # Danh sách trạng thái của Client, dùng để cập nhật lên màn hình ứng dụng
            clientStatus = []

            self.status.insert(0,"Waiting for Clients...")
            while True:
                # Nhận kết nối từ Client
                connection, address = server.accept()

                # Khi đã kết nối, đưa Client đó vào tiểu trình quản lý riêng
                thread = threading.Thread(target = handleClient, args = (connection, address, nClient, onlineClient, clientStatus))
                thread.daemon = True
                thread.start()

                # Số Client đang kết nối tăng lên
                nClient+=1
        
        # Đưa hàm cập nhật dữ liệu vào tiểu trình khác
        updateThread = threading.Thread(target = updateData)
        updateThread.daemon = True
        updateThread.start()
        
        # Chạy Server
        serverThread = threading.Thread(target = runServer)
        serverThread.daemon = True
        serverThread.start()

#----MAIN----
# Tạo Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Chạy ứng dụng
try:
    app = App()
    app.mainloop()
except:
    server.close()