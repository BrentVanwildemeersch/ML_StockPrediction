from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/receiveData", methods=['POST'])
def recieveData():
    symbol = request.json['code']
    symbol = request.json['time']
    return
#

if __name__ == "__main__":
    app.run(debug=True)