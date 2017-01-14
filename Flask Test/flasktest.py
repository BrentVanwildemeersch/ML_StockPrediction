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
    symbol = request.json['code']
    time = request.json['time']
    data = getFinancialData(symbol,time)
    global switchvalue
    switchvalue =1


    for switchvalue in range(1,5):
        getCurrentData(data)
        switchvalue +=1





    return json.dumps({"pricelow":pricelow1,"currentValue":currentprice0,"predictedclose0":predictedclose0,"predictedclose1":predictedclose1})



def getFinancialData(symbol, Day_amount):
        stocks = [symbol]
        endDate = datetime.now().date()
        startDate = (endDate - timedelta(days=int(5000)))

        df = web.DataReader(symbol,"yahoo",startDate,endDate)
        df =df[['Open','Low','High','Close']]
        return df

def getCurrentData(data):
    global currentprice0
    currentprice0 = 0
    currentprice1=0
    currentprice2=0
    currentprice3=0
    currentprice4=0
    global currentprice1
    global currentprice2
    global currentprice3
    global currentprice4
    global pricelow0
    global pricelow1
    global pricelow2
    global pricelow3
    global pricehigh0
    global pricehigh1
    global pricehigh2
    global pricehigh3

    laststats = data.tail(1)
    currentprice0 = laststats.Close.values[0]
    pricelow0 = laststats.Low.values[0]
    pricehigh0 = laststats.High.values[0]
    getPredictedOpen(data)
    return currentprice0,pricelow0,pricehigh0

def getPredictedOpen(data):
    global predictedopen0
    global predictedopen1
    global predictedopen2
    global predictedopen3
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
    if switchvalue==1:
        predictedopen1=0
        lowpricex2 = pricelow0**2
        highpricex2 = pricehigh0**2
        prediction= (regr_open.predict([pricelow0,lowpricex2,pricehigh0,highpricex2,currentprice0]))
        predictedopen0= prediction[0][0]
        getpredictedLowHigh(data)
    elif switchvalue==2:
        predictedopen2 = 0
        lowpricex2 = pricelow1 ** 2
        highpricex2 = pricehigh1 ** 2
        prediction = (regr_open.predict([pricelow1, lowpricex2, pricehigh1, highpricex2, currentprice1]))
        predictedopen1 = prediction[0][0]
        getpredictedLowHigh(data)
    elif switchvalue==3:
        predictedopen3 = 0
        lowpricex2 = pricelow2 ** 2
        highpricex2 = pricehigh2 ** 2
        prediction = (regr_open.predict([pricelow2, lowpricex2, pricehigh2, highpricex2, currentprice2]))
        predictedopen0 = prediction[0][0]
        getpredictedLowHigh(data)
    elif switchvalue==4:
        predictedopen2 = 0
        lowpricex2 = pricelow3 ** 2
        highpricex2 = pricehigh3 ** 2
        prediction = (regr_open.predict([pricelow3, lowpricex2, pricehigh3, highpricex2, currentprice3]))
        predictedopen0 = prediction[0][0]
        getpredictedLowHigh(data)


def getpredictedLowHigh(df):

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

    if switchvalue ==1:
        currentpricex2 = currentprice0 **2
        currentpricex3 = currentprice0**3
        predictedopenx2 = predictedopen0**2
        predictedopenx3 = predictedopen0**3
        lowhigh = regr_LowHigh.predict([[currentprice0,currentpricex2,currentpricex3,predictedopen0,predictedopenx2,predictedopenx3]])
        pricehigh0= lowhigh[0][0]
        pricehigh1= pricehigh0
        pricelow0 = lowhigh[0][1]
        pricelow1 = pricelow0
        getpredictedClose(df)
    elif switchvalue==2:
        currentpricex2 = currentprice1 ** 2
        currentpricex3 = currentprice1 ** 3
        predictedopenx2 = predictedopen1 ** 2
        predictedopenx3 = predictedopen1 ** 3
        lowhigh = regr_LowHigh.predict(
            [[currentprice1, currentpricex2, currentpricex3, predictedopen1, predictedopenx2, predictedopenx3]])
        pricehigh1 = lowhigh[0][0]
        pricehigh2 = pricehigh1
        pricelow1 = lowhigh[0][1]
        pricelow2 = pricelow1
        getpredictedClose(df)
    elif switchvalue == 3:
        currentpricex2 = currentprice2 ** 2
        currentpricex3 = currentprice2 ** 3
        predictedopenx2 = predictedopen2 ** 2
        predictedopenx3 = predictedopen2 ** 3
        lowhigh = regr_LowHigh.predict(
            [[currentprice2, currentpricex2, currentpricex3, predictedopen2, predictedopenx2, predictedopenx3]])
        pricehigh2 = lowhigh[0][0]
        pricehigh3 = pricehigh2
        pricelow2 = lowhigh[0][1]
        pricelow3 = pricelow2
        getpredictedClose(df)
    elif switchvalue==4:
        currentpricex2 = currentprice3 ** 2
        currentpricex3 = currentprice3 ** 3
        predictedopenx2 = predictedopen3 ** 2
        predictedopenx3 = predictedopen3 ** 3
        lowhigh = regr_LowHigh.predict(
            [[currentprice3, currentpricex2, currentpricex3, predictedopen3, predictedopenx2, predictedopenx3]])
        pricehigh0 = lowhigh[0][0]
        pricelow0 = lowhigh[0][1]
        getpredictedClose(df)


def getpredictedClose(data):
    global predictedclose0
    global predictedclose1
    global predictedclose2
    global predictedclose3

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
    if switchvalue==1:
        predictedclose1=0
        openx2 = predictedopen0 ** 2
        lowpricex2 = pricelow0 ** 2
        highpricex2 = pricehigh0 ** 2

        predictedclose0 = regr_Close.predict(
            ([[predictedopen0, openx2, pricelow0, lowpricex2, pricehigh0, highpricex2]]))
        predictedclose0 = predictedclose0[0][0]
        currentprice1= predictedclose0
        return currentprice1,predictedclose0
    elif switchvalue==2:
        predictedclose2=0
        openx2 = predictedopen1 ** 2
        lowpricex2 = pricelow1 ** 2
        highpricex2 = pricehigh1 ** 2
        predictedclose1 = regr_Close.predict(
            ([[predictedopen1, openx2, pricelow1, lowpricex2, pricehigh1, highpricex2]]))
        predictedclose1 = predictedclose1[0][0]
        predictedclose0 = 0
        return predictedclose1
    elif switchvalue==3:
        predictedclose3
        openx2 = predictedopen2 ** 2
        lowpricex2 = pricelow2 ** 2
        highpricex2 = pricehigh2 ** 2

        predictedclose2 = regr_Close.predict(
            ([[predictedopen2, openx2, pricelow2, lowpricex2, pricehigh2, highpricex2]]))
        predictedclose2 = predictedclose2[0][0]

    elif switchvalue==4 :
        openx2 = predictedopen3 ** 2
        lowpricex2 = pricelow3 ** 2
        highpricex2 = pricehigh3 ** 2

        predictedclose3 = regr_Close.predict(
            ([[predictedopen3, openx2, pricelow3, lowpricex2, pricehigh3, highpricex2]]))
        predictedclose3 = predictedclose3[0][0]










def multilayer_perceptron (x,weights,biases):
    # hidden layer with relu activation
    layer1 = tf.add(tf.matmul(x,weights['h1']),biases['b1'])
    layer1 = tf.nn.relu(layer1)

    #Hidden layer with relu activation
    layer2 = tf.add(tf.matmul(layer1,weights['h2']),biases['b2'])
    layer2 = tf.nn.relu(layer2)

    # #output layer with linear activation
    outlayer = tf.matmul(layer2,weights['out']) + biases['out']
    return outlayer


if __name__ == "__main__":
    app.run(debug=True)



