import sqlite3
import pandas as pd

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

        except:
            return False

    def findAllAnime(self, as_df=True):
        try:
            conn = sqlite3.connect(self.__db_dir)
            cursor = conn.cursor() 

            if not as_df:
                cursor.execute("SELECT * FROM anime")
                animes = cursor.fetchall()

                cursor.close()
                conn.close()

                return animes

            df = pd.read_sql_query("SELECT * FROM anime", conn)

            cursor.close()
            conn.close()

            return df

        except:
            return False
    