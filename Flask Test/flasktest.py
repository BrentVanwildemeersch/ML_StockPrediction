from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/receiveData", methods=['POST'])
def recieveData():
    symbol = request.json['code']
    time = request.json['time']
    return  symbol

if __name__ == "__main__":
    app.run(debug=True)



def getFinancialData(symbol, date):
    print "Test"