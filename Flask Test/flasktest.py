from flask import Flask, request
from flask import render_template
import time
from datetime import datetime,timedelta

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/receiveData", methods=['POST'])
def recieveData():
    symbol = request.json['code']
    time = request.json['time']


    return str(time)

def getFinancialData(symbol, Day_amount):
        stocks = [symbol]
        endDate = datetime.now().date()
        startDate = (endDate - timedelta(days=int(Day_amount)))





if __name__ == "__main__":
    app.run(debug=True)



