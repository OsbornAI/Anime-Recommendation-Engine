import sqlite3

class Users:
    def __init__(self, db_dir):
        self.__db_dir = db_dir

    def createTable(self):
        try:
            conn = sqlite3.connect(self.__db_dir)
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, anime_list TEXT, blacklist TEXT)")
            conn.commit()

            cursor.close()
            conn.close()

            return True
        
        except:
            return False

    def insertUser(self, username, password, anime_list, blacklist):
        try:
            conn = sqlite3.connect(self.__db_dir)
            cursor = conn.cursor()

            anime_list = ",".join(anime_list)
            blacklist = ",".join(blacklist)

            cursor.execute("INSERT INTO users (username, password, anime_list, blacklist) VALUES (?, ?, ?, ?)", (username, password, anime_list, blacklist))
            conn.commit()

            cursor.close()
            conn.close()

            return True
        
        except:
            return False

    def findUser(self, username):
        try:
            conn = sqlite3.connect(self.__db_dir)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user_data = cursor.fetchone() # Because there should never be anymore
            if user_data == None:
                return False

            user_data = list(user_data)
            user_data[2] = user_data[2].split(',')
            user_data[3] = user_data[3].split(',')

            cursor.close()
            conn.close()

            return user_data
        
        except:
            return False

    def updateUser(self, curr_username, username, password, anime_list, blacklist):
        try:
            conn = sqlite3.connect(self.__db_dir)
            cursor = conn.cursor()

            anime_list = ",".join(anime_list)
            blacklist = ",".join(blacklist)

            cursor.execute("UPDATE users SET username=?, password=?, anime_list=?, blacklist=? WHERE username=?", (username, password, anime_list, blacklist, curr_username))
            conn.commit()

            cursor.close()
            conn.close()

            return True
        
        except Exception as e:
            print(e)
            return False