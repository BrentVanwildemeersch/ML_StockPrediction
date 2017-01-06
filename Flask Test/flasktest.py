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

        X = df.ix[:,0:1]
        Y = df.ix[:,3:4]

        from sklearn.cross_validation import train_test_split

        X_train, X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.8)



        regr_bp = linear_model.LinearRegression()
        regr_bp.fit(X_train,Y_train)








        # return X

        return







if __name__ == "__main__":
    app.run(debug=True)



