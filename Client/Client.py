import tkinter as Tk
from tkinter import messagebox
import socket

HOST = ""
PORT = 65432
FORMAT = "utf8"
# Giao diện
class ConnectPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        self.canvas = Tk.Canvas(self, bg = "#ffffff", height = 300, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.backgroundImg = Tk.PhotoImage(file = f"ConnectPageBackground.png")
        self.canvas.create_image(250.0, 150.0, image = self.backgroundImg)

        self.canvas.create_text(370.5, 66.0, text = "CONNECT", fill = "#5780e7", font = ("None", int(30.0)))

        # Phần nhập địa chỉ IP của Server
        self.canvas.create_text(375.5, 113.5, text = "Server IP Address:", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))     
        self.serverIPEntryImg = Tk.PhotoImage(file = f"ServerIPEntry.jpg")
        self.canvas.create_image(372.5, 133.5, image = self.serverIPEntryImg)
        self.serverIPEntry = Tk.Entry(self, bd = 0, bg = "#ebfaff", highlightthickness = 0)
        self.serverIPEntry.place(x = 286, y = 126, width = 175, height = 15)
        self.serverIPEntry.focus()

        # Nút kết nối
        self.connectButtonImg = Tk.PhotoImage(file = f"ConnectButton.jpg")
        self.connectButton = Tk.Button(self, image = self.connectButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.Connect(self, client),  relief = "flat")
        self.connectButton.place(x = 338, y = 150, width = 75, height = 15)

        # Phần thông báo
        self.notify = self.canvas.create_text(375.5, 176, text = "", fill = "#DF0101", font = ("OpenSans-Bold", int(9.0)))

class SignInPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        self.canvas = Tk.Canvas(self, bg = "#ffffff", height = 300, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.backgroundImg = Tk.PhotoImage(file = f"Background.png")
        self.canvas.create_image(250.0, 150.0, image = self.backgroundImg)

        self.canvas.create_text(250.0, 38.5, text = "SIGN IN", fill = "#5780e7", font = ("OpenSans-Bold", int(20.0)))

        self.entryImg = Tk.PhotoImage(file = f"Entry.jpg")

        # Phần nhập Username
        self.canvas.create_text(250.0, 86.5, text = "Username:", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))
        self.canvas.create_image(250.0, 106.5, image = self.entryImg)
        self.usernameEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0)
        self.usernameEntry.place(x = 165, y = 100, width = 173, height = 15)
        self.usernameEntry.focus()

        # Phần nhập Password
        self.canvas.create_text(250.0, 133.5, text = "Password:", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))
        self.canvas.create_image(250.0, 153.5, image = self.entryImg)
        self.passwordEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, show = '*')
        self.passwordEntry.place(x = 165, y = 147, width = 173, height = 15)

        # Phần thông báo
        self.notify = self.canvas.create_text(250.0, 177.5, text = "", fill = "#DF0101", font = ("OpenSans-Bold", int(9.0)))

        # Nút đăng nhập
        self.loginButtonImg = Tk.PhotoImage(file = f"LoginButton.jpg")
        loginButton = Tk.Button(self, image = self.loginButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.Login(self, client), relief = "flat")
        loginButton.place(x = 162, y = 193, width = 76, height = 16)

        # Nút chuyển sáng trang đăng ký
        self.signUpButtonImg = Tk.PhotoImage(file = f"SignUpButton.jpg")
        signUpButton = Tk.Button(self, image = self.signUpButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.showPage(SignUpPage), relief = "flat")
        signUpButton.place(x = 261, y = 193, width = 76, height = 16)

        # Nút thoát
        self.exitButtonImg = Tk.PhotoImage(file = f"ExitButton.jpg")
        exitButton = Tk.Button(self, image = self.exitButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.Exit(), relief = "flat")
        exitButton.place(x = 212, y = 221, width = 76, height = 16)

class SignUpPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        self.canvas = Tk.Canvas(self, bg = "#ffffff", height = 300, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.backgroundImg = Tk.PhotoImage(file = f"Background.png")
        background = self.canvas.create_image(250.0, 150.0, image = self.backgroundImg)

        self.canvas.create_text(250.0, 38.5, text = "SIGN UP", fill = "#5780e7", font = ("OpenSans-Bold", int(20.0)))

        self.entryImg = Tk.PhotoImage(file = f"Entry.jpg")

        # Phần nhập Username
        self.canvas.create_text(250.0, 68.5, text = "Username:", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))
        self.canvas.create_image(250.0, 88.5, image = self.entryImg)
        self.usernameEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0)
        self.usernameEntry.place(x = 164, y = 81, width = 173, height = 15)
        self.usernameEntry.focus()
        
        # Phần nhập Password
        self.canvas.create_text(250.0, 115.5, text = "Password:", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))
        self.canvas.create_image(250.0, 135.5, image = self.entryImg)
        self.passwordEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, show = '*')
        self.passwordEntry.place(x = 164, y = 128, width = 173, height = 15)

        # Phần xác nhận lại Password
        self.canvas.create_text(250.0, 162.5, text = "Confirm Password:", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))
        self.canvas.create_image(250.0, 182.5, image = self.entryImg)
        self.confirmPasswordEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, show = '*')
        self.confirmPasswordEntry.place(x = 164, y = 175, width = 173, height = 15)

        # Phần thông báo
        self.notify = self.canvas.create_text(250.0, 205.5, text = "", fill = "#DF0101", font = ("OpenSans-Bold", int(9.0)))

        # Nút đăng ký
        self.signUpButtonImg = Tk.PhotoImage(file = f"SignUpButton.jpg")
        signUpButton = Tk.Button(self, image = self.signUpButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.signUp(self, client), relief = "flat")
        signUpButton.place(x = 162, y = 220, width = 76, height = 16)
        
        # Nút trở về trang đăng nhập
        self.backButtonImg = Tk.PhotoImage(file = f"BackButton.jpg")
        backButton = Tk.Button(self, image = self.backButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.showPage(SignInPage), relief = "flat")
        backButton.place(x = 261, y = 220, width = 76, height = 16)
              
class HomePage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        self.canvas = Tk.Canvas(self, bg = "#ffffff", height = 300, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.backgroundImg = Tk.PhotoImage(file = f"HomePageBackground.png")
        self.canvas.create_image(250.0, 150.0, image = self.backgroundImg)
        
        self.canvas.create_text(250.0, 35.5, text = "COVID-19", fill = "#5780e7", font = ("OpenSans-Bold", int(20.0)))

        self.entryImg = Tk.PhotoImage(file = f"Entry.jpg")
        
        # Phần nhập tên tỉnh thành
        self.canvas.create_text(250.0, 65.5, text = "Province", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))
        self.canvas.create_image(250.0, 85.5, image = self.entryImg)
        self.provinceEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0)
        self.provinceEntry.place(x = 163, y = 78, width = 175, height = 15)

        # Phần nhập ngày
        self.canvas.create_text(250.0, 112.5, text = "Date", fill = "#8c52ff", font = ("OpenSans-Bold", int(12.0)))
        self.canvas.create_image(250.0, 132.5, image = self.entryImg)
        self.dateEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0)
        self.dateEntry.place(x = 163, y = 125, width = 175, height = 15)

        # Phần thông báo
        self.notify = self.canvas.create_text(250.0, 152.5, text = "", fill = "#DF0101", font = ("OpenSans-Bold", int(9.0)))

        # Nút tra cứu
        self.lookUpButtonImg = Tk.PhotoImage(file = f"LookUpButton.png")
        lookUpButton = Tk.Button(self, image = self.lookUpButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.lookUp(self, client), relief = "flat")
        lookUpButton.place(x = 162, y = 165, width = 76, height = 16)
        
        # Nút đăng xuất
        self.logoutButtonImg = Tk.PhotoImage(file = f"LogoutButton.png")
        logoutButton = Tk.Button(self, image = self.logoutButtonImg, borderwidth = 0, highlightthickness = 0, command=lambda: appControl.Logout(), relief = "flat")
        logoutButton.place(x = 261, y = 165, width = 76, height = 16)

        # Phần hiển thị thông tin
        self.info = self.canvas.create_text(250.0, 220, text = "", fill = "#5780e7", font = ("OpenSans-Bold", int(15.0)))

# Ứng dụng
class App(Tk.Tk):
    def __init__(self):
        Tk.Tk.__init__(self)

        # Giao diện chung
        self.title("Client")
        self.geometry("500x300")
        self.configure(bg = "#ffffff")
        self.resizable(width = False, height = False)

        container = Tk.Frame()
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Tạo các Page cho ứng dụng
        self.frames = {}
        for f in (ConnectPage, SignInPage, HomePage, SignUpPage):
            frame = f(container, self)
            frame.grid(row = 0, column = 0, sticky = 'nsew')
            self.frames[f] = frame

        # Đưa trang Kết nối hiển thị đầu tiên
        self.frames[ConnectPage].tkraise()

    # Hàm chuyển ứng dụng sang một trang khác
    def showPage(self, page): self.frames[page].tkraise()

    # Các hàm chức năng
    # Kết nối
    def Connect(self, currentPage, client):
        # Nhận địa chỉ IP mà người dùng nhập
        HOST = currentPage.serverIPEntry.get()
        # Nếu người dùng bỏ trống thì yêu cầu người dùng nhập vào
        if HOST == '':
            currentPage.canvas.itemconfigure(currentPage.notify, text = "You must insert Server IP Address!")
            return

        print("You tried to connect to Server:", HOST, PORT)

        # Kết nối với Server có địa chỉ IP vừa nhập
        try: 
            client.connect((HOST, PORT))
            print("Successfully Connected")
            print("Your Address:", client.getsockname())
            # Chuyển sang trang đăng nhập
            self.showPage(SignInPage)
            
        # Nếu địa chỉ IP không hợp lệ thì hiện thông báo 
        except:
            currentPage.canvas.itemconfigure(currentPage.notify, text = "Invalid IP Address!")
            print("Failed to Connect!")

    # Đăng ký
    def signUp(self, currentPage, client):
        try:
            # Nhận Username và Password mà người dùng nhập
            username = currentPage.usernameEntry.get()
            password = currentPage.passwordEntry.get()
            confirmPassword = currentPage.confirmPasswordEntry.get()

            # Nếu người dùng bỏ trống bất kỳ ô nào thì yêu cầu người dùng nhập vào
            if username == "" or password == "" or confirmPassword == "":
                currentPage.canvas.itemconfigure(currentPage.notify, text = "You must fill all the empty fields!")
                return

            print("You tried to sign up with username:", username, "- password:", password, "- confirm password:", confirmPassword)

            # Nếu người xác nhận Password không khớp
            if confirmPassword != password:
                currentPage.canvas.itemconfigure(currentPage.notify, text = "Your password and confirm password don't match!")
                print("Failed to Sign up")
                return

            # Nếu thỏa các điều kiện nhập thì bắt đầu gửi thông tin tài khoản cho Server
            client.sendall('Sign up'.encode(FORMAT))
            client.recv(1024).decode(FORMAT)

            # Gửi Username
            client.sendall(username.encode(FORMAT))

            # Đợi Server kiểm tra
            response = client.recv(1024).decode(FORMAT)

            # Nếu Username đã tồn tại thì yêu cầu người dùng sử dụng Username khác
            if response == 'Exist':
                currentPage.canvas.itemconfigure(currentPage.notify, text = "This username already exists, please try again!")
                print("Failed to Sign up")
                return

            # Nếu không thì gửi tiếp Password để Server thêm vào dữ liệu
            client.sendall(password.encode(FORMAT))

            print("Successfully Signed up")

            # Chuyển lại trang đăng nhập
            self.showPage(SignInPage)
            # Hiện thông báo đăng ký thành công
            self.frames[SignInPage].canvas.itemconfigure(self.frames[SignInPage].notify, text = "Successfully Signed up! Use your account to login")
            # Xóa các thông báo tại trang đăng ký
            currentPage.canvas.itemconfigure(currentPage.notify, text = "")

        except: self.Error()

    # Đăng nhập
    def Login(self, currentPage, client):
        try:
            # Nhận thông tin tài khoản mà người dùng nhập vào
            username = currentPage.usernameEntry.get()
            password = currentPage.passwordEntry.get()

            # Nếu người dùng bỏ trống
            if username == "" or password == "":
                currentPage.canvas.itemconfigure(currentPage.notify, text = "You must fill all the empty fields!")
                return

            print("You tried to login with username:", username, "- password:", password)

            # Nếu không thì gửi yêu cầu đăng nhập cho Server
            client.sendall('Login'.encode(FORMAT))
            client.recv(1024).decode(FORMAT)

            # Gửi thông tin tài khoản cho Server
            client.sendall(username.encode(FORMAT))
            client.recv(1024).decode(FORMAT)
            client.sendall(password.encode(FORMAT))

            # Đợi Server kiểm tra
            response = client.recv(1024).decode(FORMAT)
            # Nếu tài khoản hợp lệ
            if response == 'True':
                # Đưa tới trang tra cứu
                self.showPage(HomePage)
                # Xóa các dòng thông báo tại trang đăng nhập
                currentPage.canvas.itemconfigure(currentPage.notify, text = "")
                return
            # Nếu tài khoản đang được đăng nhập bởi Client khác thì hiện thông báo
            if response == 'Exist':
                currentPage.canvas.itemconfigure(currentPage.notify, text = "This account is already logged in by another client!")
                print("Failed to Login")
                return
            # Nếu thông tin tài khoản sai thì hiện thông báo
            else: 
                currentPage.canvas.itemconfigure(currentPage.notify, text = "Your username or password is incorrect, please try again!")
                print("Failed to Login")
                return

        except: self.Error()

    # Đăng xuất
    def Logout(self):
        try:
            # Gửi yêu cầu đăng xuất cho Server
            client.sendall('Logout'.encode(FORMAT))
            # Chuyển về trang đăng nhập
            self.showPage(SignInPage)
            print("Logged out!")
        except: self.Error()

    # Tra cứu
    def lookUp(self, currentPage, client):
        currentPage.canvas.itemconfigure(currentPage.info, text = "")
        try:
            # Nhận thônng tin mà người dùng nhập vào
            date = currentPage.dateEntry.get()
            province = currentPage.provinceEntry.get()

            # Nếu người dùng không nhập tên tỉnh thì yêu cầu nhập lại
            if province == "":
                currentPage.canvas.itemconfigure(currentPage.notify, text = "You must insert province's name!")
                return
            
            # Nếu người dùng không nhập ngày thì gán ngày = "None" để Server nhận diện Client không tra cứu theo ngày
            if date == "": 
                print("You tried to search for total cases in", province)
                date = "None"
            else: print("You tried to search for new cases in", province, "in", date)

            # Gửi yêu cầu tra cứu cho Server
            client.sendall('Look up'.encode(FORMAT))
            client.recv(1024).decode(FORMAT)

            # Gửi thông tin ngày và tên tỉnh cho Server
            client.sendall(date.encode(FORMAT))
            client.recv(1024).decode(FORMAT)
            client.sendall(province.encode(FORMAT))

            # Đợi Server kiểm tra
            response = client.recv(1024).decode(FORMAT)
            client.sendall(response.encode(FORMAT))

            # Nếu thông tin nhập vào hợp lệ
            if response == 'True':               
                cases = client.recv(1024).decode(FORMAT)

                # Nếu người dùng không tra cứu theo ngày thì hiển thị tổng số ca
                if date == "None": currentPage.canvas.itemconfigure(currentPage.info, text = "Total cases: " + cases)
                # Nếu người dùng tra cứu theo ngày thì hiển thị số ca mắc mới trong ngày đó
                else: currentPage.canvas.itemconfigure(currentPage.info, text = "New cases (" + date + "): " + cases)
                currentPage.canvas.itemconfigure(currentPage.notify, text = "")

            # Nếu thông tin nhập vào không hợp lệ
            else:
                currentPage.canvas.itemconfigure(currentPage.notify, text = "Invalid province or date!")

        except: self.Error()

    # Thoát
    def Exit(self):
        try:
            # Gửi yêu cầu thoát cho Server và thoảt chương trình
            client.sendall('Exit'.encode(FORMAT))
            self.destroy()
        except: self.Error()
      
    # Thông báo lỗi khi Server đóng hoặc mất kết nối đột ngột
    def Error(self):
        messagebox.showerror('Server Error', 'Error: Server has been closed!');
        self.destroy()

# Tạo socket Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Chạy ứng dụng
app = App()
app.mainloop()

client.close()