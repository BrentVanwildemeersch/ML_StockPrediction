from flask import Flask, request
from flask import render_template
import time
from datetime import datetime,timedelta
import pandas_datareader.data as web
from sklearn import linear_model
from matplotlib import pyplot as plt
import numpy as np

import sklearn

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/receiveData", methods=['POST'])
def recieveData():
    symbol = request.json['code']
    time = request.json['time']
    data = getFinancialData(symbol,time)

    return str(data)

def getFinancialData(symbol, Day_amount):
        stocks = [symbol]
        endDate = datetime.now().date()
        startDate = (endDate - timedelta(days=int(Day_amount)))

        df = web.DataReader(symbol,"yahoo",startDate,endDate)
        df =df[['Open','Low','High','Close']]

        # first test lineaire regressie voor stock prediction
        #
        # X = df.ix[:,0:1]
        # Y = df.ix[:,3:4]
        #
        # from sklearn.cross_validation import train_test_split
        #
        # X_train, X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3)
        #
        #
        #
        # regr_bp = linear_model.LinearRegression()
        # regr_bp.fit(X_train,Y_train)
        #
        # # open today == close yesteraday
        # openTdy = Y.iloc[len(X)-1][0]
        # # predict today
        # closeTdy =regr_bp.predict(openTdy)
        #
        # # open tommorow = close today
        # # predict close tomorrow
        # closeTomorrow= regr_bp.predict(closeTdy)
        #
        # # predict +1day
        # close_2day = regr_bp.predict(closeTomorrow)
        #
        #
        #
        #
        # return close_2day

#        second test


# voorspellen van de openingswaarde van het aandeel
        df_predictOpen = df[['Low','High','Close','Open']]
        df_predictOpen.Open = df_predictOpen.Open.shift(-1)

        df_predictOpen=df_predictOpen.ix[:-1]

        # multiple regression, importeren van gekwadrateerde variabelen
        df_predictOpen.insert(1,'Low x 2',df_predictOpen.Low**2)
        df_predictOpen.insert(3, 'High x 2', df_predictOpen.High ** 2)
        # df_predictOpen.insert(5, 'Close x 2', df_predictOpen.Close ** 2)

        # opdelen van dataframe in X & Y
        X_predictOpen = df_predictOpen.ix[:,0:5]
        Y_predictOpen = df_predictOpen.ix[:,5:6]

        from sklearn.cross_validation import train_test_split
        X_train,X_test,Y_train,Y_test = train_test_split(X_predictOpen,Y_predictOpen, test_size=0.5)

        regr_open = linear_model.LinearRegression()
        regr_open.fit(X_train,Y_train)
        score = regr_open.score(X_test,Y_test)

        # voorspellen openingswaarde nieuwe dag
        # return X_predictOpen
        # return regr_open.predict([[41.119999,1690.854318,41.830002,1749.749067,41.599998]])

# voorspellen van de low en high variabelen van de nieuwe dag
        df_predictLowHigh = df[['Close','Open','High','Low']]
        df_predictLowHigh = df_predictLowHigh.Close.shift(1)
        return df_predictLowHigh







if __name__ == "__main__":
    app.run(debug=True)



