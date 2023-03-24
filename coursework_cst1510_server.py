import pickle
from socket import *
import mysql.connector as mysql
import random
import requests
from bs4 import BeautifulSoup
import threading
# from apscheduler.schedulers.background import BlockingScheduler
import schedule
import time


HOST = "localhost"
PORT = 5500
BUFSIZE = 4096
ADDRESS = (HOST, PORT)
ALPHABET = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")


db = mysql.connect(
    host = HOST, 
    user = "root", 
    password = '', 
    database = "project_cst1510dbs"
)

cursor = db.cursor()


def scrape(url="", name="", typeOf=""):
    global modPrice

    if typeOf == "a":
        # url = "https://coinranking.com/coin/Qwsogvtv82FCd+bitcoin-btc"
        page = requests.get(url)
        print(page)
        soup = BeautifulSoup(page.text, features="html.parser")
        price = soup.find("div", {"class":"hero-coin__price"})
        if price is not None:
            modPrice = price.get_text()
            modPrice = modPrice.replace("$", "").replace(",", "").strip()
            print(modPrice)

    if typeOf == "b":
        # url4 = "https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF"
        page = requests.get(url)
        print(page)
        soup = BeautifulSoup(page.text, features="html.parser")
        price = soup.find("td", {"data-test":"ASK-value"})
        if price is not None:
            modPrice = price.get_text()
            modPrice = modPrice.replace(",", "").strip()
            print(modPrice)

    # addAsset = "INSERT INTO assets (AssetName, AssetPrice) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s);"
    # assetValues = (bitcoin_Name, bitcoin_Price, ethereum_Name, ethereum_Price, binance_Name, binance_Price, gold_Name, gold_Price, silver_Name, silver_Price)
    # cursor.execute = (addAsset, assetValues)
    # db.commit()
    # db.close()
    update = "UPDATE assets SET AssetPrice = %s WHERE AssetName = %s"
    updateValues = (modPrice, name)
    cursor.execute(update, updateValues)
    db.commit()

    return modPrice

btc = scrape("https://coinranking.com/coin/Qwsogvtv82FCd+bitcoin-btc", "Bitcoin", "a")
eth = scrape("https://coinranking.com/coin/razxDUgYGNAdQ+ethereum-eth", "Ethereum", "a")
bnb = scrape("https://coinranking.com/coin/WcwrkfNI4FUAe+bnb-bnb", "Binance", "a")
gold = scrape("https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF", "Gold", "b")
silver = scrape("https://finance.yahoo.com/quote/SI%3DF?p=SI%3DF", "Silver", "b")

def simulate(name, price, rangeA=-10, rangeB=10, save=False):
    price = round(float(price), 2)
    # randomNumber = random.randint(rangeA, rangeB)
    randomNumber = round(random.uniform(rangeA, rangeB), 2)
    print(randomNumber)
    # randomNumber = str(randomNumber)
    simulatedPrice = price + randomNumber
    simulatedPrice = str(simulatedPrice)
    print(f"{name} is {simulatedPrice}")

    if save == True:
        update = "UPDATE assets SET AssetPrice = %s WHERE AssetName = %s"
        updateValues = (simulatedPrice, name)
        cursor.execute(update, updateValues)
        db.commit()

# def scrape():

#     url1 = "https://coinranking.com/coin/Qwsogvtv82FCd+bitcoin-btc"
#     page1 = requests.get(url1)
#     soup1 = BeautifulSoup(page1.text, features="html.parser")
#     bitcoin_Name = "Bitcoin"
#     bitcoinPrice = soup1.find("div", {"class":"hero-coin__price"})
#     if bitcoinPrice is not None:
#         bitcoin_Price = bitcoinPrice.get_text()
#         bitcoin_Price = bitcoin_Price.replace("$", "").replace(",", "").strip()
#         print(bitcoin_Price)

#     url2 = "https://coinranking.com/coin/razxDUgYGNAdQ+ethereum-eth"
#     page2 = requests.get(url2)
#     soup2 = BeautifulSoup(page2.text, features="html.parser")
#     ethereum_Name = "Ethereum"
#     ethereumPrice = soup2.find("div", {"class":"hero-coin__price"})
#     if ethereumPrice is not None:
#         ethereum_Price = ethereumPrice.get_text()
#         ethereum_Price = ethereum_Price.replace("$", "").replace(",", "").strip()
#         print(ethereum_Price)

#     url3 = "https://coinranking.com/coin/WcwrkfNI4FUAe+bnb-bnb"
#     page3 = requests.get(url3)
#     soup3 = BeautifulSoup(page3.text, features="html.parser")
#     binance_Name = "Binance"
#     binancePrice = soup3.find("div", {"class":"hero-coin__price"})
#     if binancePrice is not None:
#         binance_Price = binancePrice.get_text()
#         binance_Price = binance_Price.replace("$", "").replace(",", "").strip()
#         print(binance_Price)

#     url4 = "https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF"
#     page4 = requests.get(url4)
#     gold_Name = "Gold"
#     soup4 = BeautifulSoup(page4.text, features="html.parser")
#     goldPrice = soup4.find("td", {"data-test":"ASK-value"})
#     if goldPrice is not None:
#         gold_Price = goldPrice.get_text()
#         gold_Price = gold_Price.replace(",", "").strip()
#         print(gold_Price)

#     url5 = "https://finance.yahoo.com/quote/SI%3DF?p=SI%3DF"
#     page5 = requests.get(url5)
#     silver_Name = "Silver"
#     soup5 = BeautifulSoup(page5.text, features="html.parser")
#     silverPrice = soup5.find("td", {"data-test":"ASK-value"})
#     if silverPrice is not None:
#         silver_Price = silverPrice.get_text()
#         silver_Price = silver_Price.replace(",", "").strip()
#         print(silver_Price)

#     # addAsset = "INSERT INTO assets (AssetName, AssetPrice) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s);"
#     # assetValues = (bitcoin_Name, bitcoin_Price, ethereum_Name, ethereum_Price, binance_Name, binance_Price, gold_Name, gold_Price, silver_Name, silver_Price)
#     # cursor.execute = (addAsset, assetValues)
#     # db.commit()
#     # db.close()
#     updateBitcoin = "UPDATE assets SET AssetPrice = %s WHERE AssetName = %s"
#     updateBitcoinValues = (bitcoin_Price, bitcoin_Name)
#     cursor.execute(updateBitcoin, updateBitcoinValues)
#     db.commit()
#     updateEthereum = "UPDATE assets SET AssetPrice = %s WHERE AssetName = %s"
#     updateEthereumValues = (ethereum_Price, ethereum_Name)
#     cursor.execute(updateEthereum, updateEthereumValues)
#     db.commit()
#     updateBinance = "UPDATE assets SET AssetPrice = %s WHERE AssetName = %s"
#     updateBinanceValues = (binance_Price, binance_Name)
#     cursor.execute(updateBinance, updateBinanceValues)
#     db.commit()
#     updateGold = "UPDATE assets SET AssetPrice = %s WHERE AssetName = %s"
#     updateGoldValues = (gold_Price, gold_Name)
#     cursor.execute(updateGold, updateGoldValues)
#     db.commit()
#     updateSilver = "UPDATE assets SET AssetPrice = %s WHERE AssetName = %s"
#     updateSilverValues = (silver_Price, silver_Name)
#     cursor.execute(updateSilver, updateSilverValues)
#     db.commit()




def randomVarChar():
    randomAlpha = random.randint(1, 26)
    num = random.randint(100, 999)
    alphanum = f"{ALPHABET[randomAlpha]+str(num)}"
    return alphanum

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()
    client, address = s.accept()
    with client:
        print(f"Connected by {address}")
        while True:
            data = (client.recv(BUFSIZE))
            data = data.decode()
            data = eval(data)
            d = data
            print(data)
            if data[-1] == "signup":
                UserID = f"{data[0][0]+randomVarChar()}"
                fName = data[0]
                lName = data[1]
                uName = data[2]
                passWord = data[3]
                deposit = data[4]
                insertTable = "INSERT INTO users (UserID, FirstName, LastName, UserName, Password, Total_Cash) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (UserID, fName, lName, uName, passWord, deposit)
                cursor.execute(insertTable, values)
                insertIDSales = "INSERT INTO sales (UID, BitcoinValue, BitcoinPrice, EthereumValue, EthereumPrice, BinanceValue, BinancePrice, GoldValue, GoldPrice, SilverValue, SilverPrice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values1 = (UserID, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00)
                cursor.execute(insertIDSales, values1)
                # id = pickle.dumps(UserID)
                # client.sendall(id)
                db.commit()
                # cursor.close()
                # db.close()
                checkTable = "SELECT UserID, Password, Total_Investment, Gain_Loss, Total_Cash FROM users WHERE UserID=%s AND Password=%s"
                values2 = (UserID, passWord)
                cursor.execute(checkTable, values2)
                users = cursor.fetchall()
                print(users)
                correct = "validuser"
                if users == []:
                    correct = "nouser"
                print(users)
                auth = [users[0], correct]
                a = str(auth)
                a = a.replace("Decimal", "")
                # u = pickle.dumps(users)
                # p = pickle.dumps(correct)
                client.sendall(a.encode())
                # cursor.close()
                # db.close()
            if data[-1] == "login":
                UserID = data[0]
                passWord = data[1]
                checkTable = "SELECT UserID, Password, Total_Investment, Gain_Loss, Total_Cash FROM users WHERE UserID=%s AND Password=%s"
                values = (UserID, passWord)
                cursor.execute(checkTable, values)
                users = cursor.fetchall()
                correct = "validuser"
                if users == []:
                    correct = "nouser"
                print(users)
                auth = [users[0], correct]
                a = str(auth)
                a = a.replace("Decimal", "")
                # u = pickle.dumps(users)
                # p = pickle.dumps(correct)
                client.sendall(a.encode())
                # cursor.close()
                # db.close()
            if data[-1] == "deposit":
                UserID = data[0]
                cash = data[1]
                password = data[2]
                updateUserCash = "UPDATE users SET Total_Cash = Total_Cash + %s WHERE UserID = %s"
                values3 = (cash, UserID)
                print("money don enter")
                # cursor = db.cursor()
                cursor.execute(updateUserCash, values3)
                checkTable = "SELECT UserID, Total_Cash FROM users WHERE UserID=%s AND Password =%s"
                values4 = (UserID, password)
                cursor.execute(checkTable, values4)
                userCash = cursor.fetchall()
                uc = str(userCash)
                client.sendall(uc.encode())
                db.commit()
                # db.close()
                # checkTable = "SELECT AssetName, AssetPrice FROM assets WHERE UserID=%s AND Password=%s"
            
            if data[-1] == "buy":

                print("test this thing")

                def buy():
                    global item
                    global ratio

                    UserID = data[0]
                    cash = data[1]
                    roundCash = round(float(cash), 2)
                    item = data[2]
                    itemPrice = data[3]

                    print(f"from client: {itemPrice}")
                    checkBalance = "SELECT Total_Cash FROM users WHERE UserID=%s"
                    values5 = (UserID)
                    cursor.execute(checkBalance, values5)
                    userBalance = cursor.fetchall()
                    userBalance = str(userBalance)
                    userBalance = userBalance.replace("[", "")
                    userBalance = userBalance.replace("]", "")
                    userBalance = round(float(userBalance), 2)

                    print(userBalance)

                    assetPurchasePrice = itemPrice
                    assetPurchasePrice = str(assetPurchasePrice)
                    assetPurchasePrice = assetPurchasePrice.replace("[", "")
                    assetPurchasePrice = assetPurchasePrice.replace("]", "")
                    assetPurchasePrice = round(float(assetPurchasePrice), 2)
                    salesTablePriceColumn = item.replace("Value", "Price")
                    
                    ratio = roundCash/assetPurchasePrice

                    if userBalance >= roundCash:
                        print("--Transacting--")
                        new_userBalance = userBalance - roundCash
                        updateUserBalance = "UPDATE users SET Total_Cash = %s WHERE UserID = %s"
                        values6 = (new_userBalance, UserID)
                        cursor.execute(updateUserBalance, values6)
                        updateUserAssetValue = "UPDATE sales SET %s = %s + %s WHERE UID = %s"
                        values7 = (item, item, roundCash, UserID)
                        updateUserAssetPrice = "UPDATE sales SET %s = %s WHERE UID = %s"
                        values9 = (salesTablePriceColumn, itemPrice, UserID)
                        cursor.execute(updateUserAssetPrice, values9)
                        db.commit()
                    else:
                        print("not enough money")
                    
                def run_threaded3(job_func):
                    job_thread = threading.Thread(target=job_func)
                    job_thread.start()
                
                run_threaded3(buy)

                def currentAssetValue():
                    global item
                    global ratio
                    itemName = item.replace("Value", "")
                    checkAsset = "SELECT AssetPrice From assets WHERE AssetName = %s"
                    values8 = (itemName)
                    cursor.execute(checkAsset, values8)
                    new_assetPrice = cursor.fetchall()
                    new_assetPrice = str(new_assetPrice)
                    new_assetPrice = new_assetPrice.replace("[", "")
                    new_assetPrice = new_assetPrice.replace("]", "")
                    new_assetPrice = round(float(new_assetPrice), 2)
                    newValue = ratio * new_assetPrice
                    updateAssetValue = "UPDATE sales SET %s = %s WHERE UID = %s"
                    values10 = (item, newValue, UserID)
                    cursor.execute(updateAssetValue, values10)

                    checkSales = "SELECT BitcoinValue FROM sales WHERE UID = %s"
                    cursor.execute(checkSales, UserID)
                    salesRecord = cursor.fetchall()
                    # assets = assets.remove("")
                    print(salesRecord)
                    # commodities = [assets]
                    sr = str(salesRecord)
                    sr = sr.replace("Decimal", "")
                    sr = sr.replace("(", "")
                    sr = sr.replace(")", "")
                    client.send(sr.encode())
                
                def run_threaded2(job_func):
                    job_thread = threading.Thread(target=job_func)
                    job_thread.start()
                
                schedule.every(15).seconds.do(run_threaded2, currentAssetValue)
                while True:
                    schedule.run_pending()
                    time.sleep(1)

            if data[-1] == "price":
                def run():
                    simulate("Bitcoin", btc, -100, 100, True)
                    simulate("Ethereum", eth, -100, 100, True)
                    simulate("Binance", bnb, -100, 100, True)
                    simulate("Gold", gold, -2, 2, True)
                    simulate("Silver", silver, -2, 2, True)
                    checkAssets = "SELECT * FROM assets"
                    cursor.execute(checkAssets)
                    assets = cursor.fetchall()
                    # assets = assets.remove("")
                    print(assets)
                    # commodities = [assets]
                    cm = str(assets)
                    cm = cm.replace("Decimal", "")
                    cm = cm.replace("(", "")
                    cm = cm.replace(")", "")
                    client.send(cm.encode())

                def run_threaded(job_func):
                    job_thread = threading.Thread(target=job_func)
                    job_thread.start()
                
                schedule.every(15).seconds.do(run_threaded, run)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            
                # db.close()
                # checkTable = "SELECT AssetName, AssetPrice FROM assets WHERE UserID=%s AND Password=%s"
            if not data:
                break



# createTable = "CREATE TABLE assets (AssetName VARCHAR(255), AssetPrice DECIMAL(30,2));"

# alterTable = "ALTER TABLE users  ADD COLUMN Total_Cash BIGINT DEFAULT 0;"
# dropColumn = "ALTER TABLE users DROP COLUMN Total_Investment, DROP COLUMN Gain_Loss, DROP COLUMN Total_Cash;"
# dropTable = "DROP TABLE assets"
# alterDefaults = "ALTER TABLE users MODIFY Total_Cash BIGINT DEFAULT 0"
# deleteAll = "DELETE FROM assets"
# cursor.execute(createTable)
# db.commit()
# db.close()
