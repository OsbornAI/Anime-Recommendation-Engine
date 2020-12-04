from flask import Flask, request, jsonify
from data.user_data.users import Users
from data.scraped_data.anime import Anime
import os
import hashlib
import jwt
import datetime

app = Flask(__name__)
app.config['secret_key'] = "s4fQuS10jQD4cGH8bKxHWXBOLp2PYRXOiiTGCuVqgAJmVElxId"

users_db_path = os.path.join(os.getcwd(), 'backend/data/user_data/users.db') # This will have to be modified according to where it is run from
app.config['users_db'] = Users(users_db_path)
app.config['users_db'].createTable()

anime_db_path = os.path.join(os.getcwd(), 'backend/data/scraped_data/anime.db') # This will have to be modified depending on where it is run from
app.config['anime_db'] = Anime(anime_db_path)

def validateToken(token):
    try:
        data = jwt.decode(token, app.config['secret_key'])

        return data['username']

    except:
        return False

@app.route('/register', methods=['POST'], strict_slashes=False)
def register():
    username = request.form['username']
    password_raw = request.form['password']

    user = app.config['users_db'].findUser(username)
    if user != False:
       return jsonify(success=False) 
    
    password = hashlib.sha512(password_raw.encode()).hexdigest() 

    success = app.config['users_db'].insertUser(username, password, [], [])
    if not success:
        return jsonify(success=False) 

    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['secret_key'])

    return jsonify(success=True, token=token) # Probably send some session information too

@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    username = request.form['username']
    password_raw = request.form['password']
    
    users = app.config['users_db'].findUser(username)
    if not users:
        return jsonify(success=False)

    password = hashlib.sha512(password_raw.encode()).hexdigest()
    if password == users[1]:
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['secret_key'])

        return jsonify(success=True, token=token.decode('utf-8'))

    return jsonify(success=False)

@app.route('/get_list/<username>', methods=['GET'], strict_slashes=False)
def getList(username):
    user = app.config['users_db'].findUser(username)
    if not user:
        return jsonify(success=False)

    return jsonify(success=True, list=user[2])

@app.route('/add_show', methods=['POST'], strict_slashes=False)
def addShow():
    token = request.form['token']
    user = validateToken(token)

    if not user:
        return jsonify(success=False)

    user = app.config['users_db'].findUser(user)
    if not user:
        return jsonify(success=False)

    anime_id = request.form['anime_id']
    anime = app.config['anime_db'].findAnime(anime_id)
    if not anime:
        return jsonify(success=False)

    if anime_id in user[2]:
        return jsonify(success=False) 
    
    user[2].append(anime_id)
    
    if anime_id not in user[3]:
        user[3].append(anime_id)

    update = app.config['users_db'].updateUser(user[0], user[0], user[1], user[2], user[3])
    if not update:
        return jsonify(success=False)

    return jsonify(success=True)

@app.route('/remove_show', methods=['POST'], strict_slashes=False)
def removeShow():
    token = request.form['token']
    user = validateToken(token)

    if not user:
        return jsonify(success=False)

    user = app.config['users_db'].findUser(user)
    if not user:
        return jsonify(success=False)

    anime_id = request.form['anime_id']
    anime = app.config['anime_db'].findAnime(anime_id)
    if not anime:
        return jsonify(success=False)

    if anime_id not in user[2]:
        return jsonify(success=False) 
    
    user[2].remove(anime_id)

    update = app.config['users_db'].updateUser(user[0], user[0], user[1], user[2], user[3])
    if not update:
        return jsonify(success=False)

    return jsonify(success=True)

@app.route('/recommend_shows', methods=['GET'], strict_slashes=False)
def recommendShows():
    pass

if __name__ == '__main__':
    app.run(debug=True)