import sqlite3

class Users:
    def __init__(self, db_dir):
        self.__db_dir = db_dir
        self.__conn = sqlite3.connect(db_dir)
        self.__cursor = self.__conn.cursor()

    def createTable(self):
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, anime_list BLOB)')
        self.__conn.commit()

    def createUser(self, username, password, anime_list):
        self.__cursor.execute('INSERT INTO users (username, password, anime_list) VALUES (?, ?, ?)', (username, password, anime_list.encode()))
        self.__conn.commit()

    def findUser(self, username):
        self.__cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        user_data = self.__cursor.fetchall()

        return user_data

    def updateUser(self, curr_username, username=False, password=False, anime_list=False):
        user_data = self.findUser(curr_username)

        if not username:
            username = user_data[0]

        if not password:
            password = user_data[1] # I'll have to check what is being printed out for these ones

        if not anime_list:
            anime_list = user_data[2].decode()

        self.__cursor.execute('UPDATE users SET username=?, password=?, anime_list=?', (username, password, anime_list.encode()))