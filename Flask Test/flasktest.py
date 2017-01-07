from flask import Flask, request
from flask import render_template
from datetime import datetime,timedelta
import pandas_datareader.data as web
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import tensorflow as tf

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

        X_train,X_test,Y_train,Y_test = train_test_split(X_predictOpen,Y_predictOpen, test_size=0.5)

        regr_open = linear_model.LinearRegression()
        regr_open.fit(X_train,Y_train)
        score_open = regr_open.score(X_test,Y_test)

        # voorspellen openingswaarde nieuwe dag
        # return X_predictOpen
         # return regr_open.predict([[41.119999,1690.854318,41.830002,1749.749067,41.599998]])

# voorspellen van de low en high variabelen van de nieuwe dag

        df_predictLowHigh = df[['Close','Open','High','Low']]
        df_predictLowHigh.Close = df_predictLowHigh.Close.shift(1)
        df_predictLowHigh = df_predictLowHigh.ix[1:]

        # multiple regression om low high te gaan voorspellen
        df_predictLowHigh.insert(1,"Close x2", df_predictLowHigh.Close**2)
        df_predictLowHigh.insert(2,"Close x3",df_predictLowHigh.Close**3)
        df_predictLowHigh.insert(4,"Open x2",df_predictLowHigh.Open**2)
        df_predictLowHigh.insert(5, "Open x3", df_predictLowHigh.Open ** 3)

        X_predictLowHigh = df_predictLowHigh.ix[:,0:6]
        Y_predictLowHigh = df_predictLowHigh.ix[:,6:8]

        X_predictLowHigh_train,X_predictLowHigh_test,Y_predictLowHigh_train,Y_predictLowHigh_test= train_test_split(X_predictLowHigh,Y_predictLowHigh,test_size=0.5)

        regr_LowHigh = linear_model.LinearRegression()
        regr_LowHigh.fit(X_predictLowHigh_train,Y_predictLowHigh_train)
        score_LowHigh = regr_LowHigh.score(X_predictLowHigh_test,Y_predictLowHigh_test)




        # return regr_LowHigh.predict([[26.809999,718.7760464,19270.38508,27.0000,729,19683]])

# opzetten van neuraal netwerk
        X_total = df.ix[:,0:3]
        Y_total = df.ix[:,3:4]
        X_total_train, X_total_test, Y_total_train,Y_total_test = train_test_split(X_total,Y_total,test_size=0.4)

        # Parameters
        learning_rate = 000.1
        training_epoche = 15
        batch_size=100
        display_step=1

        # Network Parameters
        n_hidden_1 = 32
        n_hidden_2 = 32
        n_input  = 3  #number of neurons in the input layer
        n_output = 1 #number of neurons in the output layer

        x= tf.placeholder("float",[None,n_input])
        y = tf.placeholder("float",[None,n_output])


        weights={
            'h1': tf.Variable(tf.random_normal([n_input,n_hidden_1])),
            'h2': tf.Variable(tf.random_normal([n_hidden_1,n_hidden_2])),
            'out': tf.Variable(tf.random_normal([n_hidden_2,n_output]))
        }
        biases = {
            'b1': tf.Variable(tf.random_normal([n_hidden_1])),
            'b2': tf.Variable(tf.random_normal([n_hidden_2])),
            'out': tf.Variable(tf.random_normal([n_output]))
        }

        # Construct our model
        pred= multilayer_perceptron(x,weights,biases)

        # Define loss and optimizer
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred,y))
        optimizer= tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

        # initializing variables
        init = tf.initialize_all_variables()

        return None



def multilayer_perceptron (x,weights,biases):
    # hidden layer with relu activation
    layer1 = tf.add(tf.matmul(x,weights['h1']),biases['b1'])
    layer1 = tf.nn.relu(layer1)

    #Hidden layer with relu activation
    layer2 = tf.add(tf.matmul(layer1,weights['h2']),biases['b2'])
    layer2 = tf.nn.relu(layer2)

    #output layer with linear activation
    outlayer = tf.matmul(layer2,weights,weights['out']) + biases['out']
    return outlayer














if __name__ == "__main__":
    app.run(debug=True)



