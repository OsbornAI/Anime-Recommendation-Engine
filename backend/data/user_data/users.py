import sqlite3

# Implement a way to check if these operations succeeded or not
class Users:
    def __init__(self, db_dir):
        self.__db_dir = db_dir

    def createTable(self):
        conn = sqlite3.connect(self.__db_dir)
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, anime_list TEXT)')
        conn.commit()

        cursor.close()
        conn.close()

    def insertUser(self, username, password, anime_list):
        conn = sqlite3.connect(self.__db_dir)
        cursor = conn.cursor()

        anime_list = ",".join(anime_list)

        cursor.execute('INSERT INTO users (username, password, anime_list) VALUES (?, ?, ?)', (username, password, anime_list))
        conn.commit()

        cursor.close()
        conn.close()

    def findUser(self, username):
        conn = sqlite3.connect(self.__db_dir)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        user_data = cursor.fetchone() # Because there should never be anymore

        user_data = list(user_data)
        user_data[2] = user_data[2].split(',')

        cursor.close()
        conn.close()

        return user_data

    def updateUser(self, curr_username, username=False, password=False, anime_list=False):
        conn = sqlite3.connect(self.__db_dir)
        cursor = conn.cursor()

        user_data = self.findUser(curr_username)

        if not username:
            username = user_data[0]

        if not password:
            password = user_data[1] # I'll have to check what is being printed out for these ones

        if not anime_list:
            anime_list = ",".join(user_data[2])

        else:
            anime_list = ",".join(anime_list)

        cursor.execute('UPDATE users SET username=?, password=?, anime_list=?', (username, password, anime_list))

        cursor.close()
        conn.close()