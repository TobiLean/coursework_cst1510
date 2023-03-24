#!/usr/bin/env python
import pickle
import tkinter as Tk
from socket import *
import threading as thread
from tkinter import messagebox
import schedule
import time
# import requests
# from bs4 import BeautifulSoup


HOST = "localhost"
PORT = 5500
ADDRESS = (HOST, PORT)
BUFSIZE = 4096
global s
s = socket(AF_INET, SOCK_STREAM)
s.connect(ADDRESS)

root = Tk.Tk()
root.title("Investy | Login")
root.geometry("300x300+300+300")
root.resizable(False, False)
root.iconbitmap("favicon.ico")

fNameVar = Tk.StringVar()
lNameVar = Tk.StringVar()
userNameVar = Tk.StringVar()
passwordVar = Tk.StringVar()
userIDVar = Tk.StringVar()
depositVar = Tk.StringVar()
buyVar = Tk.StringVar()
buyAmount = Tk.StringVar()
buyQuantity = Tk.StringVar()
global wrong
wrong = False
global closewin
closewin = False
global check
check = 0


# def onClosing():
#     if messagebox.askokcancel("Want to quit?"):
#         # quitMessage = ["quit"]
#         # quitMessage = str(quitMessage)
#         # s.send(quitMessage.encode())
#         root.destroy()

# root.protocol("WM_DELETE_WINDOW", onClosing)


# fNameVar = Tk.StringVar()
# lNameVar = Tk.StringVar()
# userNameVar = Tk.StringVar()
# passwordVar = Tk.StringVar()

# # frame1 = Frame(root, width=50, height=50, bg="red")

# fNameEntry = Tk.Entry(root, width=30, textvariable=fNameVar).place(x=300, y=50)
# lName = Tk.Label(root, text = "Last Name:").place(x = 220, y = 85)
# fNameEntry = Tk.Entry(root, width=30, textvariable=lNameVar).place(x=300, y=85)
# userName = Tk.Label(root, text = "User Name:").place(x = 220, y = 120)
# userNameEntry = Tk.Entry(root, width=30, textvariable=userNameVar).place(x=300, y=120)
# password = Tk.Label(root, text = "Password:").place(x = 220, y = 155)
# passwordEntry = Tk.Entry(root, width=30, textvariable=passwordVar).place(x=300, y=155)

# def deleteLabel():
#     l.config(text="poo")

def signUp():

    global sign_up
    sign_up = Tk.Toplevel(root)
    # root = Tk.Tk()
    sign_up.title("Investy | SignUp")
    sign_up.geometry("550x400+300+200")
    sign_up.resizable(False, False)
    sign_up.iconbitmap("favicon.ico")

    fName = Tk.Label(sign_up, text = "First Name:")
    fName.place(x = 220, y = 50)
    fNameEntry = Tk.Entry(sign_up, width=30, textvariable=fNameVar)
    fNameEntry.place(x=220, y=70)
    lName = Tk.Label(sign_up, text = "Last Name:")
    lName.place(x = 220, y = 100)
    lNameEntry = Tk.Entry(sign_up, width=30, textvariable=lNameVar)
    lNameEntry.place(x=220, y=120)
    userName = Tk.Label(sign_up, text = "User Name:")
    userName.place(x = 220, y = 150)
    userNameEntry = Tk.Entry(sign_up, width=30, textvariable=userNameVar)
    userNameEntry.place(x=220, y=170)
    password = Tk.Label(sign_up, text = "Password:")
    password.place(x = 220, y = 200)
    passwordEntry = Tk.Entry(sign_up, width=30, textvariable=passwordVar)
    passwordEntry.place(x=220, y=220)
    confirmButton = Tk.Button(sign_up, text="OKAY", width=20, command=lambda: pushToServer("s"))
    confirmButton.pack(side=Tk.LEFT)
    confirmButton = Tk.Button(sign_up, text="Deposit Now", width=20, command= deposit)
    confirmButton.pack(side=Tk.BOTTOM)
    depositLabel = Tk.Label(sign_up, text = "Initial Amount:")
    depositLabel.place(x = 220, y = 250)
    depositEntry = Tk.Entry(sign_up, width=30, textvariable=depositVar)
    depositEntry.place(x=220, y=270)


def welcome():
    global welcomeWindow
    global frameRight

    def home():
        global frameRight
        global totalCashLabel
        global totalInvestmentLabel
        welcomeWindow.title(f"Investy | Welcome | Home | {auth[0][0]}")
        frameRight.config(bg="black")
        userID = Tk.Label(frameRight, text=f"Client ID: {auth[0][0]}", fg="green", bg="black")
        userID.place(x=100, y=200)
        totalInvestmentLabel = Tk.Label(frameRight, text=f"Total Investment Value: {totalInvestment}", fg="green", bg="black")
        totalInvestmentLabel.place(x=100, y=230)
        totalCashLabel = Tk.Label(frameRight, text=f"Total Cash to Invest: {totalCash}", fg="green", bg="black")
        totalCashLabel.place(x=100, y=260)
        gainLossLabel = Tk.Label(frameRight, text=f"Gain/Loss: {gainLoss}", fg="green", bg="black")
        gainLossLabel.place(x=100, y=290)
        confirmButton = Tk.Button(frameRight, text="Deposit Now", width=20, command= deposit)
        confirmButton.place(x=250, y=350)

    welcomeWindow = Tk.Toplevel(root)
    welcomeWindow.title("Investy | Welcome")
    welcomeWindow.geometry("550x400+300+200")
    welcomeWindow.resizable(False, False)
    welcomeWindow.iconbitmap("favicon.ico")
    # welcome.wm_attributes("-transparentcolor", "black")
    frameLeft = Tk.Frame(welcomeWindow, width=150, height=400, bg="blue")
    frameLeft.pack(side=Tk.LEFT)
    logo = Tk.Label(frameLeft, text="Investy", font=("Helvetica 18 bold"), fg="white", bg="blue")
    logo.place(x = 35, y = 10)
    frameRight = Tk.Frame(welcomeWindow, width=400, height=400, bg="white")
    frameRight.pack(side=Tk.RIGHT)

    home()

    investNowButton = Tk.Button(frameLeft, text="Invest Now", width=10, command=investNow)
    investNowButton.place(x = 35, y = 150)
    portfolioButton = Tk.Button(frameLeft, text="Portfolio", width=10, command=portfolioView)
    portfolioButton.place(x = 35, y = 200)
    moneyInOutButton = Tk.Button(frameLeft, text="Money In/Out", width=10, command=moneyInOut)
    moneyInOutButton.place(x = 35, y = 250)
    homeButton = Tk.Button(frameLeft, text="Home", width=10, command=home)
    homeButton.place(x = 35, y = 300)
    # thread.wait()
    # root.after(1000, root.destroy())


def investNow():
    global frameRight
    global getStuff
    global assets
    global bitcoin
    global bitcoinPrice
    global ethereum
    global ethereumPrice
    global binance
    global binancePrice
    global gold
    global goldPrice
    global silver
    global silverPrice
    global buyStatus
    welcomeWindow.title(f"Investy | Welcome | Invest | {auth[0][0]}")
    frameRight.config(bg="red")
    bitcoin = Tk.Label(frameRight, text=f"loading", bg="red")
    bitcoin.place(x=10, y=40)
    bitcoinPrice = Tk.Label(frameRight, text=f"loading", bg="red")
    bitcoinPrice.place(x=10, y=60)
    ethereum = Tk.Label(frameRight, text=f"loading", bg="red")
    ethereum.place(x=10, y=80)
    ethereumPrice = Tk.Label(frameRight, text=f"loading", bg="red")
    ethereumPrice.place(x=10, y=100)
    binance = Tk.Label(frameRight, text=f"loading", bg="red")
    binance.place(x=10, y=120)
    binancePrice = Tk.Label(frameRight, text=f"loading", bg="red")
    binancePrice.place(x=10, y=140)
    gold = Tk.Label(frameRight, text=f"loading", bg="red")
    gold.place(x=10, y=160)
    goldPrice = Tk.Label(frameRight, text=f"loading", bg="red")
    goldPrice.place(x=10, y=180)
    silver = Tk.Label(frameRight, text=f"loading", bg="red")
    silver.place(x=10, y=200)
    silverPrice = Tk.Label(frameRight, text=f"loading", bg="red")
    silverPrice.place(x=10, y=220)

    getStuff = Tk.Button(frameRight, text="Go", width=10, command=lambda: pushToServer("i"))
    getStuff.place(x = 100, y = 25)

    buyButton = Tk.Button(frameRight, text="Buy", width=10, command=buy)
    buyButton.place(x = 100, y = 75)
    # frame1 = Tk.Frame(welcomeWindow, width=400, height=400, bg="red")
    # frame1.pack(side=Tk.RIGHT)

global n
n = 0

def update():
    global assets
    global n
    n += 1

    bitcoin.configure(text=f"{assets[0]}")
    bitcoinPrice.configure(text=f"{assets[1]}")
    ethereum.configure(text=f"{assets[2]}")
    ethereumPrice.configure(text=f"{assets[3]}")
    binance.configure(text=f"{assets[4]}")
    binancePrice.configure(text=f"{assets[5]}")
    gold.configure(text=f"{assets[6]}")
    goldPrice.configure(text=f"{assets[7]}")
    silver.configure(text=f"{assets[8]}")
    silverPrice.configure(text=f"{assets[9]}")
    # root.after(1000, update)

def update2():
    global buyStatus
    totalInvestmentLabel.config(text=f"Total Investment Value: {buyStatus[0][-1]}")
    print(f"Received Buy Data: {buyStatus}")

def portfolioView():
    global frameRight
    welcomeWindow.title(f"Investy | Welcome | Portfolio | {auth[0][0]}")
    frameRight.config(bg="green")
    Tk.Label(frameRight, text="yppp")
    # frame1 = Tk.Frame(welcomeWindow, width=400, height=400, bg="red")
    # frame1.pack(side=Tk.RIGHT)

def moneyInOut():
    global frameRight
    global getStuff
    welcomeWindow.title(f"Investy | Welcome | Money In - Out | {auth[0][0]}")
    frameRight.config(bg="yellow")
    getStuff.destroy()
    Tk.Label(frameRight, text="perr")

def warn(window,text,size,color,X,Y):
 
    warnVar = Tk.Label(window, text=f"{text}", font=("Arial", size), fg=f"{color}")
    warnVar.place(x=X, y=Y)
    warnVar.after(1000, warnVar.destroy)

    print("stawwp")
    warnVar = Tk.Label(window, text=f"{text}", font=("Arial", size), fg=f"{color}")
    warnVar.place(x=X, y=Y)
    warnVar.after(1000, warnVar.destroy)

    return warnVar

def passwordCheck(phrase=""):
    global log_in
    global sign_up
    wrong = False

    SYMBOLS = ["!", "@", "#", "$", "&"]
    hasDigit = False
    hasUpper = False
    hasLower = False
    hasSymbol = False
    err = 0

    for c in phrase:
        if c.isdigit:
            hasDigit = True
        if c.isupper:
            hasUpper = True
        if c.islower:
            hasLower = True
        if c in SYMBOLS:
            hasSymbol = True

    if len(phrase) < 8:
        warn(sign_up,"Password too short!", 7, "red", 300, 175)
        err = 1
    if not hasDigit:
        warn(sign_up,"Password must contain a number!", 7, "red", 300, 175)
        err = 1
    if not hasUpper:
        warn(sign_up,"Password must contain uppercase!", 7, "red", 300, 175)
        err = 1
    if not hasLower:
        warn(sign_up,"Password must contain a lowercase!", 7, "red", 300, 175)
        err = 1
    if not hasSymbol:
        warn(sign_up,"Password must contain a special symbol!", 7, "red", 300, 175)
        err = 1
    if pushToServer == True:
        print(pushToServer)
        warn(log_in,"Password or User ID wrong", 7, "red", 10, 10)
        # Tk.Label(log_in, text="Password or User ID wrong", font=("Arial", 7), fg="red").place(x=10, y=10)
        print("yam")
        err = 1

    # if err == 0:
    #     welcome()
    # else:
    #     print("nooo123")

    return err
    
def receiveM():
    global assets
    assets = (s.recv(BUFSIZE))
    assets = assets.decode()
    assets = eval(assets)
    print(assets)
    print(f"Received Data: {assets}")
    update()
    schedule.every(15).seconds.do(receiveM)
    # check += 1
    while True:
        schedule.run_pending()
        time.sleep(1)
    return assets

def threaded_receiveM():
    global receiveThread
    receiveThread = thread.Thread(target=receiveM)
    receiveThread.daemon = True
    receiveThread.start()


def pushToServer(option, item=""):
    global invalid
    global auth
    global totalInvestment
    global gainLoss
    global totalCash
    global password

    if option == "s":
        fN = fNameVar.get()
        lN = lNameVar.get()
        uN = userNameVar.get()
        pW = passwordVar.get()
        dV = depositVar.get()
        bio = [fN, lN, uN, pW, dV, "signup"]
        bio = str(bio)
        # pickled_bio = pickle.dumps(bio)

        if passwordCheck(pW) == 1:
            passwordCheck(pW)
        else:
            # s = socket(AF_INET, SOCK_STREAM)
            # s.connect(ADDRESS)
            s.sendall(bio.encode())
            auth = s.recv(BUFSIZE)
            auth = auth.decode()
            auth = eval(auth)
            totalInvestment = auth[0][2]
            gainLoss = auth[0][3]
            totalCash = auth[0][4]
            print(auth[1])
            global userID
        print(f"Received Data: {auth}")
    if option == "l":
        uID = userIDVar.get()
        pW = passwordVar.get()
        bio = [uID, pW, "login"]
        bio = str(bio)

        if passwordCheck(pW) == 1:
            passwordCheck(pW)
        else:
            global wrong
            # s = socket(AF_INET, SOCK_STREAM)
            # s.connect(ADDRESS)
            s.sendall(bio.encode())
            auth = (s.recv(BUFSIZE))
            auth = auth.decode()
            auth = eval(auth)
            password = auth[0][1]
            totalInvestment = auth[0][2]
            gainLoss = auth[0][3]
            totalCash = auth[0][4]
            # userID = logInData
            print(auth[1])
            if auth[1] == "nouser":
                print(wrong)
                wrong = True
                print("not valid")
            print(f"Received Data: {auth}")
    if option == "i":
        global assets
        global check
        global buyStatus
        
        Message = ["price"]
        Message = str(Message)
        s.send(Message.encode())
        # assets = (s.recv(BUFSIZE))
        # assets = assets.decode()
        # assets = eval(assets)
        # print(assets)
        # print(f"Received Data: {assets}")
        threaded_receiveM()
        print(f"{wrong} no connect")
    if option == "b":
        print("yo")

        def pBuy():
            global change
            global assets
            # global auth
            global totalInvestmentLabel
            change += 1
            print(change)
            print("oga @@ Buy")

            if item == "BitcoinValue":
                itemPrice = assets[1]
            if item == "EthereumValue":
                itemPrice = assets[3]
            if item == "BinanceValue":
                itemPrice = assets[5]
            if item == "GoldValue":
                itemPrice = assets[7]
            if item == "SilverValue":
                itemPrice = assets[9]

            buyDetails = [auth[0][0], buyVar.get(), item, itemPrice, "buy"]
            buyDetails = str(buyDetails)
            s.send(buyDetails.encode())

            buyStatus = (s.recv(BUFSIZE))
            buyStatus = buyStatus.decode()
            buyStatus = eval(buyStatus)
            print(buyStatus)
            print(f"Received Data: {buyStatus}")
            time.sleep(5)

        def run_threaded2(job_func):
            global job_thread
            job_thread = thread.Thread(target=job_func)
            job_thread.daemon = True
            job_thread.start()

        run_threaded2(pBuy)

    if wrong == False:
        global closewin
        welcome()
        closewin = True
    else:
        print("sorry")
    return ""

global change
change = 1

def pushDeposit():
    global change
    global totalCashLabel
    HOST = "localhost"
    PORT = 5500
    ADDRESS = (HOST, PORT)
    change += 1
    print(change)
    print("goat")
    # s = socket(AF_INET, SOCK_STREAM)
    # s.connect(ADDRESS)
    depositDetails = [auth[0][0], depositVar.get(), password, "deposit"]
    depositDetails = str(depositDetails)
    s.sendall(depositDetails.encode())
    depositStatus = (s.recv(BUFSIZE))
    depositStatus = depositStatus.decode()
    depositStatus = eval(depositStatus)
    print(depositStatus)
    totalCashLabel.config(text=f"Total Cash to Invest: {depositStatus[0][-1]}")
    print(f"Received Data: {depositStatus}")


# def receiveBuy():
#     global assets
#     global buyStatus
#     buyStatus = (s.recv(BUFSIZE))
#     buyStatus = buyStatus.decode()
#     buyStatus = eval(buyStatus)
#     print(buyStatus)
#     print(f"Received Data: {buyStatus}")
#     update2()
#     schedule.every(15).seconds.do(receiveBuy)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

#     return buyStatus

# def threaded_receiveBuy():
#     global receiveThread2
#     receiveThread2 = thread.Thread(target=receiveBuy)
#     receiveThread2.daemon = True
#     receiveThread2.start()


def pushBuy(item):
    global change
    global assets
    global auth
    global totalInvestmentLabel
    change += 1
    print(change)
    print("let's buy!!")

    if item == "BitcoinValue":
        itemPrice = assets[1]
    if item == "EthereumValue":
        itemPrice = assets[3]
    if item == "BinanceValue":
        itemPrice = assets[5]
    if item == "GoldValue":
        itemPrice = assets[7]
    if item == "SilverValue":
        itemPrice = assets[9]

    buyDetails = [auth[0][0], buyVar.get(), item, itemPrice, "buy"]
    buyDetails = str(buyDetails)
    s.send(buyDetails.encode())

    buyStatus = (s.recv(BUFSIZE))
    buyStatus = buyStatus.decode()
    buyStatus = eval(buyStatus)
    print(buyStatus)
    print(f"Received Data: {buyStatus}")
    # threaded_receiveBuy()


def logIn():

    global log_in
    log_in = Tk.Toplevel(root)
    # root = Tk.Tk()
    log_in.title("Investy | Login")
    log_in.geometry("350x400+300+300")
    log_in.resizable(False, False)
    log_in.iconbitmap("favicon.ico")


    userID = Tk.Label(log_in, text = "User ID:")
    userID.place(x = 100, y = 120)
    userIDEntry = Tk.Entry(log_in, width=30, textvariable=userIDVar)
    userIDEntry.place(x=100, y=140)
    password = Tk.Label(log_in, text = "Password:")
    password.place(x = 100, y = 160)
    passwordEntry = Tk.Entry(log_in, width=30, textvariable=passwordVar)
    passwordEntry.place(x=100, y=180)
    confirmButton = Tk.Button(log_in, text="OKAY", width=20, command=lambda: pushToServer("l"))
    confirmButton.pack(side=Tk.BOTTOM, pady= 40)

    if wrong == True:
        log_in.destroy()

def buy():
    global buy_window

    buy_window = Tk.Toplevel(root)
    # root = Tk.Tk()
    buy_window.title(f"Investy | Deposit Now | yo")
    buy_window.geometry("300x200+300+300")
    buy_window.resizable(False, False)

    buyLabel = Tk.Label(buy_window, text = "Amount:")
    buyLabel.place(x = 30, y = 30)
    buyEntry = Tk.Entry(buy_window, width=30, textvariable=buyVar)
    buyEntry.place(x=30, y=50)
    # option3 = Tk.Radiobutton(buy_window, text="Amount", variable = buyAmount, value="1")
    # option3.place(x = 60, y = 100)
    # option4 = Tk.Radiobutton(buy_window, text="Quantity", variable = buyQuantity, value="2")
    # option4.place(x = 140, y = 100)

    confirmButton = Tk.Button(buy_window, text="Confirm & Pay", width=20, command= lambda: pushToServer("b", "BitcoinValue"))
    confirmButton.pack(side=Tk.BOTTOM)

def deposit():
    global deposit_window

    deposit_window = Tk.Toplevel(root)
    deposit_window.title(f"Investy | Deposit Now | {auth[0][0]}")
    deposit_window.geometry("300x200+300+300")
    deposit_window.resizable(False, False)
    deposit_window.iconbitmap("favicon.ico")

    depositLabel = Tk.Label(deposit_window, text = "Amount:")
    depositLabel.place(x = 30, y = 30)
    depositEntry = Tk.Entry(deposit_window, width=30, textvariable=depositVar)
    depositEntry.place(x=30, y=50)

    # depositDetails = [auth[0][0], depositVar.get(), "deposit"]
    # pickled_deposit = pickle.dumps(depositDetails)

    # def pushDeposit():
    #     with socket(AF_INET, SOCK_STREAM) as s:
    #         s.connect(ADDRESS)
    #         s.sendall(pickled_deposit)
    #         depositStatus = pickle.loads(s.recv(BUFSIZE))
    #         # totalInvestment = auth[0][2]
    #         # gainLoss = auth[0][3]
    #         # totalCash = auth[0][4]
    #         print(depositStatus)
    #     print(f"Received Data: {depositStatus}")

    confirmButton = Tk.Button(deposit_window, text="Confirm", width=20, command= pushDeposit)
    confirmButton.pack(side=Tk.BOTTOM)

# def run():
#     if pushToServer() == False:
#         print("nawa o")

# run()

#main page
t = Tk.Label(root, text = "WELCOME")
t.pack(side=Tk.TOP, pady=40)
logInButton = Tk.Button(root, text="Log In", width=20, command= logIn)
logInButton.pack(side=Tk.BOTTOM, pady=40)
signUpButton = Tk.Button(root, text="Sign Up", width=20, command= signUp)
signUpButton.pack(side=Tk.BOTTOM, pady=0)


if __name__ == '__main__':
    root.mainloop()
