from flask import Flask, request
from flask import render_template
from datetime import datetime,timedelta
import pandas_datareader.data as web
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Activation
from keras.optimizers import SGD
from keras.layers import Dense
from keras.utils import np_utils
from keras.layers import LSTM
from TFMLP import MLPR
import matplotlib.pyplot as mpl
import numpy as np
import json
# declaratie globale variabelen

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/receiveData", methods=['POST'])
def recieveData():
    global globaldata
    global symbol
    global time
    symbol = request.json['code']
    time = request.json['time']
    globaldata = getFinancialData(symbol,time)
    getCurrentData(globaldata)
    data_closed = getHistory(globaldata)

    return json.dumps({"data_predictlow":dataPredict_low,"data_predictHigh":dataPredict_high,"data_closed1day":closed_1day,"data_closed2day":closed_2day,"data_closed3day":closed_3day,"data_closed4day":closed_4day,"data_closed5day":closed_5day,"currentValue":currentprice0,"predictedclose0":predictedclose0,"pricelow":predictedpricelow0,"pricehigh":predictedpricehigh0})
@app.route("/getNextDay", methods=['Post'])
def getNextDay():

    close = request.json['close']
    high = request.json['high']
    low = request.json['low']
    currentprice0 = close
    pricelow0 = low
    pricehigh0=high

    getCurrentData(globaldata)

    return  json.dumps({"currentValue":currentprice0,"predictedclose0":predictedclose0,"pricelow":predictedpricelow0,"pricehigh":predictedpricehigh0})

def getFinancialData(symbol, Day_amount):
        stocks = [symbol]
        endDate = datetime.now().date()
        startDate = (endDate - timedelta(days=int(5000)))

        df = web.DataReader(symbol,"yahoo",startDate,endDate)
        df =df[['Open','Low','High','Close']]
        return df

def getCurrentData(data):
    global currentprice0
    global pricelow0
    global pricehigh0


    laststats = data.tail(1)
    currentprice0 = laststats.Close.values[0]
    pricelow0 = laststats.Low.values[0]
    pricehigh0 = laststats.High.values[0]
    getPredictedOpen(data)
    return currentprice0,pricelow0,pricehigh0

def getPredictedOpen(data):
    global predictedopen0

    df_predictOpen = data[['Low', 'High', 'Close', 'Open']]
    df_predictOpen.Open = df_predictOpen.Open.shift(-1)

    df_predictOpen = df_predictOpen.ix[:-1]




    # multiple regression, importeren van gekwadrateerde variabelen
    df_predictOpen.insert(1, 'Low x 2', df_predictOpen.Low ** 2)
    df_predictOpen.insert(3, 'High x 2', df_predictOpen.High ** 2)
    # df_predictOpen.insert(5, 'Close x 2', df_predictOpen.Close ** 2)

    # opdelen van dataframe in X & Y
    X_predictOpen = df_predictOpen.ix[:, 0:5]
    Y_predictOpen = df_predictOpen.ix[:, 5:6]

    X_train, X_test, Y_train, Y_test = train_test_split(X_predictOpen, Y_predictOpen, test_size=0.5)

    regr_open = linear_model.LinearRegression()
    regr_open.fit(X_train, Y_train)
    score_open = regr_open.score(X_test, Y_test)


    lowpricex2 = pricelow0**2
    highpricex2 = pricehigh0**2
    prediction= (regr_open.predict([pricelow0,lowpricex2,pricehigh0,highpricex2,currentprice0]))
    predictedopen0= prediction[0][0]
    getpredictedLowHigh(data)


def getpredictedLowHigh(df):
    global predictedpricelow0
    global predictedpricehigh0

    df_predictLowHigh = df[['Close', 'Open', 'High', 'Low']]
    df_predictLowHigh.Close = df_predictLowHigh.Close.shift(1)
    df_predictLowHigh = df_predictLowHigh.ix[1:]

    # multiple regression om low high te gaan voorspellen
    df_predictLowHigh.insert(1, "Close x2", df_predictLowHigh.Close ** 2)
    df_predictLowHigh.insert(2, "Close x3", df_predictLowHigh.Close ** 3)
    df_predictLowHigh.insert(4, "Open x2", df_predictLowHigh.Open ** 2)
    df_predictLowHigh.insert(5, "Open x3", df_predictLowHigh.Open ** 3)

    X_predictLowHigh = df_predictLowHigh.ix[:, 0:6]
    Y_predictLowHigh = df_predictLowHigh.ix[:, 6:8]

    X_predictLowHigh_train, X_predictLowHigh_test, Y_predictLowHigh_train, Y_predictLowHigh_test = train_test_split(
        X_predictLowHigh, Y_predictLowHigh, test_size=0.5)

    regr_LowHigh = linear_model.LinearRegression()
    regr_LowHigh.fit(X_predictLowHigh_train, Y_predictLowHigh_train)
    score_LowHigh = regr_LowHigh.score(X_predictLowHigh_test, Y_predictLowHigh_test)


    currentpricex2 = currentprice0 **2
    currentpricex3 = currentprice0**3
    predictedopenx2 = predictedopen0**2
    predictedopenx3 = predictedopen0**3
    lowhigh = regr_LowHigh.predict([[currentprice0,currentpricex2,currentpricex3,predictedopen0,predictedopenx2,predictedopenx3]])
    predictedpricehigh0= lowhigh[0][0]

    predictedpricelow0 = lowhigh[0][1]
    getpredictedClose(df)


def getpredictedClose(data):
    global predictedclose0


    df_predictClose = data[['Open','Low','High','Close']]

    # add weights to regression
    df_predictClose.insert(1,"Open x2", df_predictClose.Open**2)
    df_predictClose.insert(3,"Low x2", df_predictClose.Low**2)
    df_predictClose.insert(5,"High x2", df_predictClose.High**2)
    # multiple regression on
    X_predictClose = df_predictClose.ix[:,0:6]
    Y_predictClose = df_predictClose.ix[:,6:7]




    X_predictClose_train,X_predictClose_test,Y_predictClose_train,Y_predictClose_test = train_test_split(X_predictClose,Y_predictClose, test_size=0.4)

    regr_Close = linear_model.LinearRegression()
    regr_Close.fit(X_predictClose_train,Y_predictClose_train)
    score_open=regr_Close.score(X_predictClose_test,Y_predictClose_test)

    predictedclose1=0
    openx2 = predictedopen0 ** 2
    lowpricex2 = predictedpricelow0** 2
    highpricex2 = predictedpricehigh0 ** 2

    predictedclose0 = regr_Close.predict(
            ([[predictedopen0, openx2, predictedpricelow0, lowpricex2, predictedpricehigh0, highpricex2]]))
    predictedclose0 = predictedclose0[0][0]
    currentprice1= predictedclose0
    return currentprice1,predictedclose0


def getHistory(data):
    global closed_1day
    global closed_2day
    global closed_3day
    global closed_4day
    global closed_5day
    global dataPredict_close
    global dataPredict_high
    global dataPredict_low
    data_Closed = data[['Close']]
    data_Closed = data_Closed.tail(6)

    dataPredict = data[['Low','High','Close']]
    dataPredict = dataPredict.tail(5)
    dataPredict_low = dataPredict.values[0][0]
    dataPredict_high = dataPredict.values[0][1]
    dataPredict_close = dataPredict.values[0][2]


    closed_1day = data_Closed.values[4][0]
    closed_2day = data_Closed.values[3][0]
    closed_3day = data_Closed.values[2][0]
    closed_4day = data_Closed.values[1][0]
    closed_5day = data_Closed.values[0][0]

    return closed_1day



if __name__ == "__main__":
    app.run(debug=True)



