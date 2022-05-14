import sqlite3

import pandas as pd

if __name__ == '__main__':
    def read():
        dbname = 'asset/word_english.db'
        # dbname = 'asset/word_japanese.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        df = pd.read_sql('SELECT * FROM word', conn)
        print(df)

        cur.close()
        conn.close()


    def write():
        dbname = 'asset/word_english.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        i = "apple"
        j = "リンゴ"
        sql = 'INSERT INTO word(word, result) values(' + '"' + i + '"' + ',' + '"' + j + '"' + ')'
        cur.execute(sql)

        conn.commit()
        cur.close()
        conn.close()

    read()
