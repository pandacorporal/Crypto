import time
import requests
import os
import pickle
import sys
import pathlib

#todo figure out if it is better to insert items at front of the lists or to just remake the lists in reverse order



#dictionary that contains all the symbols for the binance API calls
priceSymbols = {'bitcoin': 'BTCUSDT', 'ripple': "XRPBTC",
                'ethereum': 'ETHBTC', 'BCC': 'BCCBTC',
                'LTC': 'LTCBTC', 'Dash': 'DASHBTC',
                'Monero': 'XMRBTC', 'Qtum': 'QTUMBTC', 'ETC': 'ETCBTC',
                'Zcash': 'ZECBTC', 'ADA': 'ADABTC', 'ADX': 'ADXBTC', 'AION' : 'AIONBTC', 'AMB': 'AMBBTC', 'APPC': 'APPCBTC', 'ARK': 'ARKBTC', 'ARN': 'ARNBTC', 'AST': 'ASTBTC', 'BAT': 'BATBTC', 'BCD': 'BCDBTC', 'BCPT': 'BCPTBTC', 'BNB': 'BNBBTC', 'BNT': 'BNTBTC', 'BQX': 'BQXBTC', 'BRD': 'BRDBTC', 'BTS': 'BTSBTC', 'CDT': 'CDTBTC', 'CMT': 'CMTBTC', 'CND': 'CNDBTC', 'CTR':'CTRBTC', 'DGD': 'DGDBTC', 'DLT': 'DLTBTC', 'DNT': 'DNTBTC', 'EDO': 'EDOBTC', 'ELF': 'ELFBTC', 'ENG': 'ENGBTC', 'ENJ': 'ENJBTC', 'EOS': 'EOSBTC', 'EVX': 'EVXBTC', 'FUEL': 'FUELBTC', 'FUN': 'FUNBTC', 'GAS': 'GASBTC', 'GTO': 'GTOBTC', 'GVT': 'GVTBTC', 'GXS': 'GXSBTC', 'HSR': 'HSRBTC', 'ICN': 'ICNBTC', 'ICX': 'ICXBTC', 'IOTA': "IOTABTC", 'KMD': 'KMDBTC', 'KNC': 'KNCBTC', 'LEND': 'LENDBTC', 'LINK':'LINKBTC', 'LRC':'LRCBTC', 'LSK':'LSKBTC', 'LUN': 'LUNBTC', 'MANA': 'MANABTC', 'MCO': 'MCOBTC', 'MDA': 'MDABTC', 'MOD': 'MODBTC', 'MTH': 'MTHBTC', 'MTL': 'MTLBTC', 'NAV': 'NAVBTC', 'NEBL': 'NEBLBTC', 'NEO': 'NEOBTC', 'NULS': 'NULSBTC', 'OAX': 'OAXBTC', 'OMG': 'OMGBTC', 'OST': 'OSTBTC', 'POE': 'POEBTC', 'POWR': 'POWRBTC', 'PPT': 'PPTBTC', 'QSP': 'QSPBTC', 'RCN': 'RCNBTC', 'RDN': 'RDNBTC', 'REQ': 'REQBTC', 'SALT': 'SALTBTC', 'SNGLS': 'SNGLSBTC', 'SNM': 'SNMBTC', 'SNT': 'SNTBTC', 'STORJ': 'STORJBTC', 'STRAT': 'STRATBTC', 'SUB': 'SUBBTC', 'TNB': 'TNBBTC', 'TNT': 'TNTBTC', 'TRIG': 'TRIGBTC', 'TRX': 'TRXBTC', 'VEN': 'VENBTC', 'VIB': 'VIBBTC', 'VIBE': 'VIBEBTC', 'WABI': 'WABIBTC', 'WAVES': 'WAVESBTC', 'WINGS': 'WINGSBTC', 'WTC': 'WTCBTC', 'XVG': 'XVGBTC', 'XZC': 'XZCBTC', 'YOYO': 'YOYOBTC', 'ZRX': 'ZRXBTC'}

#dictionarys to store the data after its read in from a text file.
cryptoOpenPriceData = {}
cryptoClosePriceData = {}
cryptoVolumeData = {}
cryptoHighData = {}
cryptoLowData = {}
stepsize = {}

#path to save the different text files in
#cryptoPaths = r'C:\Users\DrewG\Documents\GitHub\Crypto\CryptoData'
cryptoPaths = r'C:\Users\katso\Documents\GitHub\Crypto\CryptoData'
cryptoPaths = r'C:\Users\DrewG\Documents\GitHub\Crypto\CryptoData'
#cryptoPaths = r'C:\Users\katso\Documents\GitHub\Crypto\CryptoData'
#makes the directorys in the path variable if they do not exist
pathlib.Path(cryptoPaths).mkdir(parents=True, exist_ok=True)


logPath = r'C:\Users\katso\Documents\GitHub\Crypto\CryptoDataDebug.txt'
#logPath = r'C:\Users\DrewG\Documents\GitHub\Crypto\CryptoDataDebug.txt'
#logPath = r'C:\Users\katso\Documents\GitHub\Crypto\CryptoDataDebug.txt'
logPath = r'C:\Users\DrewG\Documents\GitHub\Crypto\CryptoDataDebug.txt'


file = open(logPath, "w")

#one day in ms
ONE_DAY = 86400000
ONE_THIRD_DAY = 28800000
COUNT = 21

def getData(numDays):

  #code for writing the values into three text files for each crypto: an open price, close price, and volume file.
  for key, value in priceSymbols.items():
        #creating the file path lengths and opening them
        openPriceCryptoPath = os.path.join(cryptoPaths, value + "OpenPrice" + ".txt")
        closePriceCryptoPath = os.path.join(cryptoPaths, value + "ClosePrice" + ".txt")
        volumeCryptoPath = os.path.join(cryptoPaths, value + "Volume" + ".txt")
        highCryptoPath = os.path.join(cryptoPaths, value + "High" + ".txt")
        lowCryptoPath = os.path.join(cryptoPaths, value + "Low" + ".txt")
        oprice = open(openPriceCryptoPath, "w")
        cprice = open(closePriceCryptoPath, "w")
        volume = open(volumeCryptoPath, "w")
        highPrice = open(highCryptoPath, "w")
        lowPrice = open(lowCryptoPath, "w")

        #while loop with a counter to make sure that the start and endtime stay one day apart but go backwards in time, numdays amount of days
        timeBackwards = 0
        while(timeBackwards < ONE_DAY*numDays):
            endTime = requests.get("https://api.binance.com/api/v1/time")
            endTime = endTime.json()
            endTime = endTime['serverTime'] - timeBackwards
            startTime = endTime - ONE_THIRD_DAY
            parameters = {'symbol': value, 'startTime': startTime, 'endTime': endTime, 'interval': '1m'}
            data = requests.get("https://api.binance.com/api/v1/klines", params=parameters)
            data = data.json()
            print("Length of data set: {} coin associated with data set: {} data set: {}".format(len(data), value, data))
            for i in reversed(data):
                oprice.write("{},".format(i[1]))
                highPrice.write("{}, ".format(i[2]))
                lowPrice.write("{}, ".format(i[3]))
                cprice.write("{},".format(i[4]))
                volume.write("{},".format(i[5]))
            timeBackwards += ONE_THIRD_DAY

  #closing all the files once we're done
  oprice.close()
  highPrice.close()
  lowPrice.close()
  cprice.close()
  volume.close()

#get the binance step sizes of each crypto (the step size is the minimum significant digits allowed by binance for crypto to be traded in)
def binStepSize():
    #getting the dictionary of a lot of aggregate data for all symbols
    global stepsize
    stepsizeinfo = requests.get("https://api.binance.com/api/v1/exchangeInfo")
    bigdata = stepsizeinfo.json()["symbols"]

    #iterating through the dictionary and adding just the stepsizes into our own dictionary
    for i in bigdata:
        symbol = i["symbol"]
        stepsizem = i["filters"][1]["stepSize"]
        temp = {symbol: stepsizem}
        stepsize.update(temp)


def getOpenPrice(interval, minutesBack):
    if(cryptoOpenPriceData == {}):
        #iterating through all the crypto symbols
        for key, value in priceSymbols.items():
            #the number of number of minutes we have gone back so far
            mins = 0

            # creating the path lengths and opening the openprice file with read permissions
            openPriceCryptoPath = os.path.join(cryptoPaths, value + "OpenPrice" + ".txt")
            oprice = open(openPriceCryptoPath, "r")

            #reading through the file
            odata = oprice.readlines()

            # iterating through each file and adding the correct open prices to the dictionary goes through in reverse to make it oldest to newest
            for line in odata:
                words = line.split(",")
                #iterate through each data point in the line
                for i in words:
                    #check to see that the datapoint is between the endpoint and startpoint of the interval to train on
                    if mins > minutesBack and mins <= (minutesBack + interval):

                        # if there is not already a dictionary created for the value create one and put the first value in it
                        if (cryptoOpenPriceData == {} or value not in cryptoOpenPriceData):
                            temp = {value: [i]}
                            cryptoOpenPriceData.update(temp)
                        # otherwise append the price to the list that is already there
                        else:
                            cryptoOpenPriceData[value].append(i)
                    mins+=1

        #makes a new dictionary if the dicitonary is not made yet and puts the values for each crypto in reverse
        # this is because crypto stat has data ordered newest to oldest and thus it has to be reversed before
        # it can be used to train oldest to newest in the evalutator

        for key, value in priceSymbols.items():
            reversedData = []
            for i in reversed(cryptoOpenPriceData[value]):
                reversedData.append(i)
            cryptoOpenPriceData.update({value: reversedData})

    return cryptoOpenPriceData


def getClosePrice(interval, minutesBack):
    if(cryptoClosePriceData == {}):
        #iterating through all the crypto symbols
        for key, value in priceSymbols.items():
            #the number of number of minutes we have gone back so far
            mins = 0
            #creating the path lengths and opening the close price file with read permissions
            closePriceCryptoPath = os.path.join(cryptoPaths, value + "ClosePrice" + ".txt")
            cprice = open(closePriceCryptoPath, "r")

            #reading through the file
            cdata = cprice.readlines()

            #iterating through each file and adding the correct close price to the dictionary goes through in reverse to make it oldest to newest
            for line in cdata:
                words = line.split(",")
                # iterate through each data point in the line
                for i in words:
                    # check to see that the datapoint is between the endpoint and startpoint of the interval to train on
                    if mins > minutesBack and mins <= (minutesBack + interval):
                        if (cryptoClosePriceData == {} or value not in cryptoClosePriceData):
                            temp = {value: [i]}
                            cryptoClosePriceData.update(temp)
                        else:
                            cryptoClosePriceData[value].append(i)
                    mins+=1

        #makes a new dictionary if the dicitonary is not made yet and puts the values for each crypto in reverse
        # this is because crypto stat has data ordered newest to oldest and thus it has to be reversed before
        # it can be used to train oldest to newest in the evalutator

        for key, value in priceSymbols.items():
            reversedData = []
            for i in reversed(cryptoClosePriceData[value]):
                reversedData.append(i)
            cryptoClosePriceData.update({value: reversedData})

    return cryptoClosePriceData

def getVolume(interval, minutesBack):
    if(cryptoVolumeData == {}):
        #iterate through all the crypto symbols
        for key, value in priceSymbols.items():
            # the number of number of minutes we have gone back so far
            mins = 0
            # creating the path lengths and opening the files with read permissions
            volumeCryptoPath = os.path.join(cryptoPaths, value + "Volume" + ".txt")
            volume = open(volumeCryptoPath, "r")

            # reading through the volume file of the files
            vol = volume.readlines()

            # iterating through each file and adding the volume data to the dictionary
            for line in vol:
                openprice = line.split(",")
                # iterate through each data point in the line goes through in reverse to make it oldest to newest
                for i in openprice:
                    # check to see that the datapoint is between the endpoint and startpoint of the interval to train on
                    if mins > minutesBack and mins <= (minutesBack + interval):
                        if (cryptoVolumeData == {} or value not in cryptoVolumeData):
                            temp = {value: [i]}
                            cryptoVolumeData.update(temp)
                        else:
                            cryptoVolumeData[value].append(i)
                    mins+=1

        #makes a new dictionary if the dicitonary is not made yet and puts the values for each crypto in reverse
        # this is because crypto stat has data ordered newest to oldest and thus it has to be reversed before
        # it can be used to train oldest to newest in the evalutator

        for key, value in priceSymbols.items():
            reversedData = []
            for i in reversed(cryptoVolumeData[value]):
                reversedData.append(i)

            cryptoVolumeData.update({value: reversedData})

    return cryptoVolumeData

def getHighPrice(interval, minutesBack):
    if (cryptoHighData == {}):
        # iterating through all the crypto symbols
        for key, value in priceSymbols.items():
            # the number of number of minutes we have gone back so far
            mins = 0
            # creating the path lengths and opening the close price file with read permissions
            highCryptoPath = os.path.join(cryptoPaths, value + "High" + ".txt")
            hprice = open(highCryptoPath, "r")

            # reading through the file
            hdata = hprice.readlines()

            # iterating through each file and adding the correct close price to the dictionary goes through in reverse to make it oldest to newest
            for line in hdata:
                words = line.split(",")
                # iterate through each data point in the line
                for i in words:
                    # check to see that the datapoint is between the endpoint and startpoint of the interval to train on
                    if mins > minutesBack and mins <= (minutesBack + interval):
                        if (cryptoHighData == {} or value not in cryptoHighData):
                            temp = {value: [i]}
                            cryptoHighData.update(temp)
                        else:
                            cryptoHighData[value].append(i)

                    mins += 1

        # makes a new dictionary if the dicitonary is not made yet and puts the values for each crypto in reverse
        # this is because crypto stat has data ordered newest to oldest and thus it has to be reversed before
        # it can be used to train oldest to newest in the evalutator
        for key, value in priceSymbols.items():
            reversedData = []
            for i in reversed(cryptoHighData[value]):
                reversedData.append(i)
            cryptoHighData.update({value: reversedData})

    return cryptoHighData

def getLowPrice(interval, minutesBack):
    if (cryptoLowData == {}):
        # iterating through all the crypto symbols
        for key, value in priceSymbols.items():
            # the number of number of minutes we have gone back so far
            mins = 0
            # creating the path lengths and opening the close price file with read permissions
            lowCryptoPath = os.path.join(cryptoPaths, value + "Low" + ".txt")
            lprice = open(lowCryptoPath, "r")

            # reading through the file
            ldata = lprice.readlines()

            # iterating through each file and adding the correct close price to the dictionary goes through in reverse to make it oldest to newest
            for line in ldata:
                words = line.split(",")
                # iterate through each data point in the line
                for i in words:
                    # check to see that the datapoint is between the endpoint and startpoint of the interval to train on
                    if mins > minutesBack and mins <= (minutesBack + interval):
                        if (cryptoLowData == {} or value not in cryptoLowData):
                            temp = {value: [i]}
                            cryptoLowData.update(temp)
                        else:
                            cryptoLowData[value].append(i)

                    mins += 1

        # makes a new dictionary if the dicitonary is not made yet and puts the values for each crypto in reverse
        # this is because crypto stat has data ordered newest to oldest and thus it has to be reversed before
        # it can be used to train oldest to newest in the evalutator
        for key, value in priceSymbols.items():
            reversedData = []
            for i in reversed(cryptoLowData[value]):
                reversedData.append(i)
            cryptoLowData.update({value: reversedData})

    return cryptoLowData


def main():
    getData(COUNT)
    with open("Mode.pkl", "rb") as pickle_file:
        test = pickle.load(pickle_file)
    print("Mode: {}".format(test))
    with open("PARAMETERS.pkl", "rb") as pickle_file:
        param = pickle.load(pickle_file)
    print("Parameters: {}".format(param))
    with open("RunTime.pkl", "rb") as pickle_file:
        run = pickle.load(pickle_file)
    print("Runtime: {}".format(run))





if __name__ == "__main__":
    main()