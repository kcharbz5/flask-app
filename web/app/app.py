from flask import Flask, json, render_template, request
from configparser import ConfigParser

from lib.db.mongo import UserDatabase

app = Flask(__name__)
db = UserDatabase()

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def show_sign_up():
    return render_template('signup.html')

@app.route('/showSignIn')
def show_sign_in():
    return render_template('signin.html')

@app.route('/test_add')
def test_add_user():
    db.add_user('john_doe', 'pass')

@app.route('/test_rm')
def test_remove_user():
    db.remove_user('john_doe')

@app.route('/test_check')
def test_check_user():
    return str(db.check_user('john_doe', 'pass'))

@app.route('/signIn', methods=['POST'])
def sign_in():
 
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _password = request.form['inputPassword']
    
        # validate the received values
        if _name and _password:
            
            if db.check_user(_name, _password):
                return json.dumps({'message' : 'Worked!!!'})

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/signUp', methods=['POST'])
def sign_up():
 
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _first_name = request.form['firstName']
        _last_name = request.form['lastName']
        _address = request.form['address']
    
        # validate the received values
        if _name and _password:
            db.add_user(
                _name, 
                _password, 
                email=str(_email),
                first_name=str(_first_name),
                last_name=str(_last_name),
                street=str(_address)
                )

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')