from flask import Flask, request, jsonify
import backend.data.user_data.users

app = Flask(__name__)

@app.route('/register', methods=['POST'], strict_slashes=False)
def register():
    username = request.form['username']
    password_raw = request.form['password']



    return jsonify(username=username, password=password_raw)

@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    username = request.form['username']
    password_raw = request.form['password']

    return jsonify(login=True)
    # Now we do a match in our database and if it returns true then we will authenticate the user

# Grab recommended anime | Login | Add show | Remove show

if __name__ == '__main__':
    app.run(debug=True)