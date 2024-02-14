from distutils.log import debug
import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    
    #val1, val2, val3, val4, val5, val6, val7, val8,val9,val10,val11,val12,val13,val14,val15 = float(request.form['1']), float(request.form['2']), float(request.form['3']), float(request.form['4']), float(request.form['5']), float(request.form['6']), float(request.form['7']), float(request.form['8']), float(request.form['9']), float(request.form['10']), float(request.form['11']), float(request.form['12']), float(request.form['13']), float(request.form['14']), float(request.form['15'])
    #final4 = np.array([val2,val5,val6,val7,val8,val9,val10,val11,val12,val13,val14,val15]).reshape(1,-1)
    model = joblib.load('model.sav')
    int_features= [float(x) for x in request.form.values()]
    final4=[np.array(int_features)]
    predict = model.predict(final4)
    #predict = round(predict[0], 2)
    print(predict)
    #predict = round(predict[0], 2)
    #val = round(predict * 82.71,2)
    
    return render_template('result.html', result = predict)
    


@app.route('/notebook')
def notebook():
	return render_template('Notebook.html')

@app.route('/about')
def about():
	return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)
