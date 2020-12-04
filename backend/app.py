from flask import Flask, request, jsonify, session
from data.user_data.users import Users
import os
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = "s4fQuS10jQD4cGH8bKxHWXBOLp2PYRXOiiTGCuVqgAJmVElxId" # Change me for production

db_path = os.path.join(os.getcwd(), 'backend/data/user_data/users.db')
db = Users(db_path)
db.createTable()

@app.route('/register', methods=['POST'], strict_slashes=False)
def register():
    username = request.form['username']
    password_raw = request.form['password']

    user = db.findUser(username)
    if user != None:
       return jsonify(success=False) 
    
    password = hashlib.sha512(password_raw.encode()).hexdigest() 

    db.insertUser(username, password, [], [])

    session['username'] = username
    return jsonify(success=True) # Probably send some session information too

@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    username = request.form['username']
    password_raw = request.form['password']
    
    users = db.findUser(username)
    if len(users) == 0:
        return jsonify(success=False)

    password = hashlib.sha512(password_raw.encode()).hexdigest()
    print(users)
    if password == users[1]:
        session['username'] = username

        return jsonify(success=True)

    return jsonify(success=False)


@app.route('/get_list/<username>', methods=['GET'], strict_slashes=False)
def getList(username):
    user = db.findUser(username)

    if user == None:
        return jsonify(list=None)
    
    return jsonify(list=user[2])

@app.route('/add_show', methods=['POST'], strict_slashes=False)
def addShow():
    # How to get the username of this user? Might need to use a session - this will also keep control of the blacklist which will not be removed

    pass

@app.route('/remove_show', methods=['POST'], strict_slashes=False)
def removeShow():
    pass

@app.route('remove_show', methods=['GET'], strict_slashes=False)
def recommendShows():
    pass

if __name__ == '__main__':
    app.run(debug=True)