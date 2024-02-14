from flask import Flask, request, render_template
import joblib
import sqlite3
import numpy as np

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

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('user', '')
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        number = request.form.get('mobile', '')
        password = request.form.get('password', '')

        with sqlite3.connect('signup.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO `info` (`user`, `email`, `password`, `mobile`, `name`) VALUES (?, ?, ?, ?, ?)",
                        (username, email, password, number, name))
            con.commit()
    
    return render_template("signin.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        mail1 = request.form.get('user', '')
        password1 = request.form.get('password', '')

        with sqlite3.connect('signup.db') as con:
            cur = con.cursor()
            cur.execute("SELECT `user`, `password` FROM info WHERE `user` = ? AND `password` = ?", (mail1, password1,))
            data = cur.fetchone()

            if data is None:
                return render_template("signin.html")
            elif mail1 == 'admin' and password1 == 'admin':
                print(mail1)
                return render_template("index.html")
            elif mail1 == str(data[0]) and password1 == str(data[1]):
                return render_template("index.html")
            else:
                return render_template("signup.html")

    return render_template("signin.html")


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    model = joblib.load('model.sav')

    try:
        # Convert form values to float for prediction
        int_features = [float(x) for x in request.form.values()]
        final4 = [np.array(int_features)]
        predict = model.predict(final4)
        result = predict[0]
        return render_template('result.html', result=result)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/notebook')
def notebook():
    return render_template('Notebook.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
