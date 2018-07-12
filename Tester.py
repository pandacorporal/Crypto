# Copyright (c) 2018 A&D
# Small tester to measure the effectiveness of the CryptoTrainer
import sys
import time
import os
import pickle
import pathlib
import PriceSymbolsUpdater
import random
from AutoTrader import getbinanceprice
from Generics import PARAMETERS, superParams, priceSymbols, removeEmptyInnerLists, combinableparams, normalizationValuesToStore


basesource = r'wss://stream.binance.com:9443'

# setup the relative file path
dirname = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dirname, '')

# param file name + path
paramPaths = filename

# makes the directorys in the path variable if they do not exist
pathlib.Path(paramPaths).mkdir(parents=True, exist_ok=True)

paramCompletePath = os.path.join(paramPaths, "param.pickle")

# open a file for appending (a). + creates file if does not exist
file = open(paramCompletePath, "w+")


# list of colors that can be copied into the fivethirtyeightfile
colors = ['008fd5', 'fc4f30', 'e5ae38', '6d904f', '8b8b8b', '810f7c', 'f2d4b6', 'f2ae1b', 'f4bbc2', '1209e0', 'b0dlc5',
          'dd1d36', '55b4d4', 'ff8f40', 'd35058', '252a8b', '623b19', 'b8962e', 'ff66be', '35679a', '7fffd4', '458b74',
          '8a2be2', 'ff4040', '8b2323', 'ffd39b', '98f5ff', '53868b', '7fff00', '458b00', 'd2691e', 'ff7256', '6495ed',
          'fff8dc', '00ffff', '008b8b', 'ffb90f', '006400', 'caff70', 'ff8c00', 'cd6600', '9932cc', 'bf3eff', '8fbc8f',
          'c1ffc1', '9bcd9b', '97ffff', '00ced1', '9400d3', 'ff1493', '8b0a50', '00bfff', '1e90fff', 'b22222', 'ff3030',
          '228b22', 'ffd700', 'adff2f', 'ff69b4', 'ff6a6a', '7cfc00', 'bfefff', 'ee9572', '20b2aa', 'ff00ff', '66cdaa',
          '0000cd', 'e066ff', '00fa9a', '191970', 'b3ee3a', 'ff4500', 'ff83fa', 'bbffff', 'ff0000', '4169e1', '54ff9f',
          '87ceeb', 'a0522d', '836fff', '00ff7f', '008b45', '63b8ff', 'd2b48c', 'ffe1ff', 'ff6347', '8b3626', '00f5ff',
          '00868b', 'ee82ee', 'ff3e96', 'f5deb3', 'd02090', 'ffff00', '9acd32', '00c5cd', 'ff7256', '00cdcd', 'eead0e',
          '6e8b3d', 'ee7800', 'b23aee', '483d8b', '00b2ee', 'ee2c2c', 'ffc125', '00cd00', 'ee6aa7', 'ee6363', 'f08080',
          'eedd82', 'ffb6c1', '87cefa', 'b03060', '3cb371', '191970', 'c0ff3e', 'db7093', '98fb98', 'ff82ab', 'cdaf95',
          'ffbbff', 'b0e0e6']


def main():
    global  priceSymbols
    priceSymbols = PriceSymbolsUpdater.chooseUpdate('binance')

    randnum = 1000000

    while(randnum != 0):
        randnum = int(random.uniform(0, 1) * 10)
        print(randnum)

    quit()



    randomizeParamsList(PARAMETERS, 'COMBINED_PARAMS', 100, 10, 50, 0, combinableparams, 10, 20)

    print(PARAMETERS)

    randomizeParamsList(PARAMETERS, 'COMBINED_PARAMS_MODIFIERS', 100, 10, 50, 0, combinableparams, 10, 20)

    print(PARAMETERS)


# setup the stored crypto calculations dictionary of lists and the corresponding dictionary with the max calcualted values
# for each of the combined parameters

def setupStoredCalculationsForCombinedParams(storeCombinedParamsValues, storedCombinedParamsValuesMaxs,
                                             combinedparamslist,
                                             priceSymbols):
    """
    :param storeCombinedParamsValues: the dictionary of combined parameters calculations to store
    :param storedCombinedParamsValuesMaxs: the dictionary of the max for each combined parameter
    :param combinedparamslist: the list of lists where each sublist has parameters to combine to form a new parameter
    :param priceSymbols: the dictionary of price symbols
    :return:
    """

    for combinedparamindex in range(len(combinedparamslist)):
        # loop through all the crypto types
        for key, currencyname in priceSymbols.items():
            # if the crypto currency name does not have a dictionary for its combined param data
            if currencyname not in storeCombinedParamsValues:
                # make a dictionary to hold the data of the current crypto
                storeCombinedParamsValues.update({currencyname: {}})

            # add a spot to store the data of this type for the current crypto
            storeCombinedParamsValues[currencyname].update({combinedparamindex: 0.0})

        # add a float to hold the max value for each combined parameter calculation type
        storedCombinedParamsValuesMaxs.update({combinedparamindex: 0.0})

# setup the stored crypto calculations dictionary of lists and the corresponding dictionary with the max
# calculated values
def setupStoredCryptoCalculationsandMaxes(cryptoCalcualtionsStored, maxCalculationsStored, normalizationValuesToStore,
                                          priceSymbols):
    """
    :param cryptoCalcualtionsStored: the dictionary with lists for all the calculations that need to be stored for each crypto
    :param maxCalculationsStored: the dictionary containing the maximum values for each calculation
    :param normalizationValuesToStore: the list of names given to each type of calculation to be stored for
    the normalization of the individual values when deciding a score
    :param priceSymbols: the dictionary of crypto currency symbols
    :return:
    """
    # run through each normalization value name
    for valuename in normalizationValuesToStore:
        # loop through all the crypto types
        for key, currencyname in priceSymbols.items():
            # check if the currency already had a dictionary for its data made
            if currencyname not in cryptoCalcualtionsStored:
                # make a a new dictionary to hold all the data for that crypto
                cryptoCalcualtionsStored.update({currencyname: {}})

            # add a spot to store the data of this type for the current crypto
            cryptoCalcualtionsStored[currencyname].update({valuename: 0.0})
        # add a float to hold the eventually calculated maximum for value for each calculation type
        maxCalculationsStored.update({valuename: 0.0})

def setuptestdict(testdict, valuetoset, headers, subheaders):

    for header in headers:
        testdict.update({header: {}})
        for subheader in subheaders:
            testdict[header].update({subheader: valuetoset})


def testmodifylistindict(listindict):

    for index in range(len(listindict)):
        listindict[index] += 2


def setupcompoundinteresttest():

    maxyears = 42

    returnedyears = 0

    guessrate = 0.1

    expectedamount = 14000000000

    amount = 0

    while (amount < expectedamount):
        numyears, amount = calculaterateofcompoundinterest(5000000, expectedamount, guessrate, maxyears)

        guessrate += 0.01

        print(guessrate)



def calculaterateofcompoundinterest(principal,  amountexpected, guessrate, maxyears):

    curramount = principal

    numyears = 0

    while(curramount < amountexpected and numyears < maxyears):

        curramount = curramount * guessrate + curramount

        curramount -= curramount * 0.5

        numyears += 1



    return numyears, curramount


# randomize the list parameters. used to modify the list of lists of parameters to combine (to make new parameters)
# and to modify the list of the modifiers for each list of parameters to combine
# combinedparams = [[param1, param2], [param3, param1,param5]]
# combinedparamsmodifiers = [modifier1, modifier2]
def randomizeParamsList(params, keytochange, randcheckrange, checkthreshold, range, lowvalueofrange,
                            combinableparams,
                            stopchangingparamsthreshold, removeparamsthreshold):
        """
        :param params: the parameter dictionary to be changed
        :param keytochange: the key value to change
        :param randcheck: the value used to set a range of random values to be used to determine if a parameter should be randomized
        :param checkthreshold: the value that the random check value has to be higher than to allow the parameter to be randomized
        :param range: the range used to make a random value to change the parameter
        :param lowvalueofrange: the low value of that range of values to change the parameter by
        :param combinableparams: the list of parameters that can be combined to form new parameters
        :param stopchangingparamsthreshold: the randomized value must be above this to keep changing a set of parameters
        to combine
        :param removeparamsthreshold: the randomized value must be below this to remove a parameter and above it
        to add one (implied that it is already above the stopchangingparamsthreshold)
        :return: the modified parameter dictionary
        """

        # if the param list is the list of combined params
        # this should be a list of lists where each list is made of the parameters to be combined
        # the first letter of each parameter is whether it should be added (+) or multipled (*) to the
        # rest of the parameters
        if keytochange == 'COMBINED_PARAMS':

            # the upperlimit of the range of random values (is not included in range)
            upperlimitofrange = randcheckrange

            # loop through the lists of the combined parameters
            for listofcombinedparams in params[keytochange]:

                # first generate a value to make a decision
                modifiyparamdecision = int(random.uniform(0, 1) * upperlimitofrange)

                # while the decision value is not to add or remove a parameter or when there are no parameters left in the list
                while (modifiyparamdecision <= stopchangingparamsthreshold or len(listofcombinedparams) == 0):

                    # if we choose to remove a parameter
                    if modifiyparamdecision <= removeparamsthreshold:
                        # generate a value corresponding to an index in the list of parameters to combined
                        # the value is used to decide which parameter to remove
                        indexofparamtoremove = int(random.uniform(0, 1) * len(listofcombinedparams))

                        # remove the specified parameter
                        listofcombinedparams.remove(indexofparamtoremove)

                    # if we choose to add a parameter
                    elif modifiyparamdecision > removeparamsthreshold:

                        # the upper limit that is not included in the add or multiply or subtract parameter decision below
                        rangeofdecision = 3

                        # the three decisions that can be made about what to do with this parameter
                        addition = 0
                        subtraction = 1
                        multiplication = 3

                        # generate a value to determine if this parameter will be added or multipled or subtracted
                        # so if added then paramtocombine + alltheothercombinedparams
                        # and if multipled paramtocombine * alltheothercombinedparams
                        # and if subtracted paramtocombine - alltheothercominedparams
                        includeparamdecision = int(random.uniform(0, 1) * rangeofdecision)

                        # generate a value corresponding to an index in the list of parameters that can be combined
                        # the value is used to decide which parameter to add to the current list of combined parameters
                        indexofparamtoinclude = int(random.uniform(0, 1) * len(combinableparams))

                        # depending on what we want to do with this parameter we add it to the list
                        # of parameters to combine for this particular new parameter and we add a symbol
                        # to the front of the parameter name indicating what to do with this parameter
                        if includeparamdecision == addition:
                            listofcombinedparams.append("+ {}".format(combinableparams[indexofparamtoinclude]))
                        elif includeparamdecision == multiplication:
                            listofcombinedparams.append("* {}".format(combinableparams[indexofparamtoinclude]))
                        elif includeparamdecision == subtraction:
                            listofcombinedparams.append("- {}".format(combinableparams[indexofparamtoinclude]))

                        else:
                            print("not a valid decision {}".format(includeparamdecision))
                            quit(-1)

                        # instantiate a new modifier value in the corresponding list of combined parameters modifiers
                        # each list of combined parameters gets one modifier
                        # so combinedparams =  [[param1, param2], [param1, param3, param4]
                        # would have combinedparamsmodifiers = [modifier1, modifier2]
                        newmodifiervalue = (random.uniform(-1, 1) * range) + lowvalueofrange

                        # add the new modifier value to the end of the parameter list of modifiers
                        params['COMBINED_PARAMS_MODIFIERS'].append(newmodifiervalue)

                    # generate a new value for the next decision
                    modifiyparamdecision = int(random.uniform(0, 1) * upperlimitofrange)

            # go through the list of lists of combined parameters and remove any lists that are empty
            # simultaneously delete any entries from the list of the modifiers for the combined parameters
            # that correspond to the empty combined parameter lists
            # so if param1 = [[1,2],[]] and param2 = [1,2]
            # then the method changes them to param1 = [[1,2]] and param2 = [1]
            removeEmptyInnerLists(params[keytochange], params['COMBINED_PARAMS_MODIFIERS'])

        # if the param list is the list of combined param modifiers
        elif keytochange == 'COMBINED_PARAMS_MODIFIERS':

            # ensure that the list of combined params modifiers has one modifier for every list in the list of lists
            # of parameters to combine (to make new parameters)
            if (len(params[keytochange]) != len(params['COMBINED_PARAMS'])):
                print("the combined parameter list and the list of its modifiers are not equal length")
                print("combined parameter list length {}".format(len(params['COMBINED_PARAMS'])))
                print("combined parameter modifier list length {}".format(len(params[keytochange])))
                exit(-1)

            # iterate through the list of the combined params modifiers
            # one modifier for each list of combined params
            for modifierindex in range(len(params[keytochange])):

                # generate a value to be used to determine if this modifier will be changed
                randcheck = int(random.uniform(0, 1) * randcheckrange)

                # if the random value is above the threshold set for allowing modification
                if randcheck > checkthreshold:
                    # generate the random value to modify the modifier with
                    randval = (random.uniform(-1, 1) * range) + lowvalueofrange

                    # modify the combined parameter modifier by that random value generated
                    params[keytochange][modifierindex] += randval

        else:
            print("not a valid list key: {}".format(keytochange))
            quit(-1)

#test the modification of a dictionary
def testmodifydict(dict):
    """
    :param dict: dict to modify
    :return:
    """

    dict['first'] = 100

# reads pickle from a file into the passed parameter dictionary
def readParamPickle(directory, idnum):
    """
    :param directory: the path of the pickle file
    :param idnum: the id number for the superparam file
    :return:
    """
    # makes the directorys in the path variable if they do not exist
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    with open(directory + str(idnum) + "superparam.pkl", "rb") as pickle_in:
        paramDict = pickle.load(pickle_in)

    return paramDict



#builds the logs for the trainer file if none is created and prepares the logs for the evaluator files
# makes a log file for this instance of the trainer that is sorted into a folder by the date it was run
# and its name is just its timestamp
def initdirectories(paramspassed, typedirec='storage'):
    """
    :param paramspassed: the parameters passed from the command line or the superTrainer
    :return:
    """

    directory = "{}{}/{}/{}/{}/{}".format(filename, typedirec, paramspassed['website'], paramspassed['day'], paramspassed['hour']
                                          , paramspassed['min'])

    # makes the directorys in the path variable if they do not exist
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    #makes the directory of the associated idnum exist if it does not already
    pathlib.Path("{}/{}".format(directory, paramspassed['idnum'])).mkdir(parents=True, exist_ok=True)

    #if this is a training directory then make a class file for the param variaitons to be picked by the evaluator bots
    #and make log directory for each class
    if typedirec == 'training':
        for numclass in range(superParams['classes']):
            # makes the param directory of the associated class exist if it does not already
            pathlib.Path("{}/{}/{}class/variations".format(directory, paramspassed['idnum'], numclass)).mkdir(parents=True, exist_ok=True)

            # makes the log directory of the associated class exist if it does not already
            pathlib.Path("{}/{}/{}class/logs".format(directory, paramspassed['idnum'], numclass)).mkdir(parents=True, exist_ok=True)




#reads the parameters passed
#determines if the trainer is run standalone or by another function
def readParamsPassed():
    """
    :return: param dictionary storing the parameters passed
    """

    if sys.argv[1] == "Alone":
        print("Alone")
    else:
        for line in sys.stdin:
            if line != '':
                params = line.split()
                passedparams = {'website': params[0], 'day': params[1], 'hour': params[2], 'min': params[3],
                 'idnum': int(params[4])}
    print(passedparams)
    return passedparams

# return the number of price symbols
def get_num_prices():
    count = 0
    for key, value in priceSymbols.items():
        count += 1
    print(count)

# reads pickle from a file


def testReadParamPickle():
    global paramPaths
    pickle_in = open(paramPaths + '/' + "param.pkl", "rb")
    testDict = pickle.load(pickle_in)

    print(testDict)



# write pickle to a file
def testWriteParamPickle(testDict=PARAMETERS, idnum=1, website='', day='', super=False):

    if super:
        path = filename + website + '/' + day
        # makes the directorys in the path variable if they do not exist
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        pickle_out = open(path + '/' + idnum + "superparam.pkl", "wb")
    else:
        pickle_out = open(paramPaths + '/' + "param.pkl", "wb")
    pickle.dump(testDict, pickle_out)
    pickle_out.close()

# gets the minimum $$ amounts that still get the accepted level of percentage lost to overbuying and underselling
# levelToAccess is a parameter that determines how many 'levels' of the bids/asks you get from the api 5,10,20 only


def testCalcMinBidandAsk(acceptedLossPercentage, levelsToAccess):
    prices = {}
    minBid = 0.0
    minAsk = 0.0
    global basesource

    for key, currencyname in priceSymbols.items():
        source = basesource + '/ws/' + str(currencyname) + '@depth' + str(levelsToAccess)
        # try to open with urllib (if source is http, ftp, or file URL)
        try:
            print(source)
        except (IOError, OSError):
            print('error')
            pass


def testCryptoTrainer():
    for line in sys.stdin:
        print("LINEBEGIN" + line + "DONEEND")


def testCalcPercentChange():
    startVal = 1.0
    endVal = 4.0
    result = (((float(endVal) - float(startVal)) / float(startVal)) * 100)

    print(str(result))


# reads in the ttable stored and places it in a pickle file
def readttable(name='ttablesingle'):

    ttabledict = {}

    with open(name, 'r') as infile:
        for line in infile:
            listsplit = line.split()
            degreefreedom = listsplit[0]
            for index in range(len(listsplit)):
                if index == 0:
                    ttabledict.update({listsplit[index]: []})
                else:
                    ttabledict[degreefreedom].append(listsplit[index])

    writedicttopickle(ttabledict, name)

# writes the dict to a pickle file


def writedicttopickle(dict, name):
    pickleFileName = name + ".pkl"

    picklefile = paramPaths + pickleFileName

    with open(picklefile, "wb") as pickle_out:
        pickle.dump(dict, pickle_out)


if __name__ == "__main__":
    main()
