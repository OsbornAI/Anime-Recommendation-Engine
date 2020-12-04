import sqlite3

class Anime:
    def __init__(self, db_dir):
        self.__db_dir = db_dir

    def findAnime(self, anime_id):
        try:
            conn = sqlite3.connect(self.__db_dir)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM anime where anime_id=?", (anime_id,))
            anime = cursor.fetchone()
            if anime == None:
                return False

            cursor.close()
            conn.close()

            return anime

        except Exception as e:
            print(e)
            return False