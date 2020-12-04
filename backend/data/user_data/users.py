import sqlite3

# Implement a way to check if these operations succeeded or not
class Users:
    def __init__(self, db_dir):
        self.__db_dir = db_dir

    def createTable(self):
        conn = sqlite3.connect(self.__db_dir)
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, anime_list TEXT, blacklist TEXT)')
        conn.commit()

        cursor.close()
        conn.close()

    def insertUser(self, username, password, anime_list, blacklist):
        conn = sqlite3.connect(self.__db_dir)
        cursor = conn.cursor()

        anime_list = ",".join(anime_list)
        blacklist = ",".join(blacklist)

        cursor.execute('INSERT INTO users (username, password, anime_list, blacklist) VALUES (?, ?, ?, ?)', (username, password, anime_list, blacklist))
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
        user_data[3] = user_data[3].split(',')

        cursor.close()
        conn.close()

        return user_data

    def updateUser(self, curr_username, username, password, anime_list, blacklist):
        conn = sqlite3.connect(self.__db_dir)
        cursor = conn.cursor()

        anime_list = ",".join(anime_list)
        blacklist = ",".join(blacklist)

        cursor.execute('UPDATE users SET username=?, password=?, anime_list=? WHERE username=?', (username, password, anime_list, blacklist, curr_username))

        cursor.close()
        conn.close()