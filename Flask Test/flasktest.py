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
    currentprice = getCurrentData(data)



    return json.dumps({"currentValue":currentprice,"openvalue":predictedOpen,"lowhigh":lowhigh})




def getFinancialData(symbol, Day_amount):
        stocks = [symbol]
        endDate = datetime.now().date()
        startDate = (endDate - timedelta(days=int(Day_amount)))

        df = web.DataReader(symbol,"yahoo",startDate,endDate)
        df =df[['Open','Low','High','Close']]
        return df

def getCurrentData(data):
    global currentprice
    global lowprice
    global highprice
    laststats = data.tail(1)
    currentprice = laststats.Close.values[0]
    lowprice = laststats.Low.values[0]
    highprice = laststats.High.values[0]
    getPredictedOpen(data)
    return currentprice

def getPredictedOpen(data):
    global predictedOpen
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

    # voorspellen openingswaarde nieuwe dag
    # return X_predictOpen
    # Berekenen added weights
    lowpricex2 = lowprice**2
    highpricex2 = highprice**2
    prediction= (regr_open.predict([lowprice,lowpricex2,highprice,highpricex2,currentprice]))
    predictedOpen = prediction[0][0]
    getpredictedLowHigh(data)
    return predictedOpen

def getpredictedLowHigh(df):
    global lowhigh
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
    currentpricex2 = currentprice **2
    currentpricex3 = currentprice**3
    predictedopenx2 = predictedOpen**2
    predictedopenx3 = predictedOpen**3
    lowhigh = regr_LowHigh.predict([[currentprice,currentpricex2,currentpricex3,predictedOpen,predictedopenx2,predictedopenx3]])
    return lowhigh

def getpredictedClose(data):
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
    return score_open




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



