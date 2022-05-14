from bs4 import BeautifulSoup as bs4
from time import sleep
import requests
import sqlite3
import pandas as pd
import pandas.io.sql
import itertools


class MakeWordList:
    def __init__(self):
        self.url = 'https://ejje.weblio.jp/content/'
        self.word = []
        self.result = []
        print("""
Select which language word list you make 
1: English(word), Japanese translation 
2: Japanese(word), English translation
""")
        self.mode = input("input here: ")

    def make_english_database(self):
        dbname = 'asset/word_english.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE word(id INTEGER PRIMARY KEY AUTOINCREMENT, word STRING, result STRING)'
        )
        conn.commit()
        conn.close()

    def make_japanese_database(self):
        dbname = 'asset/word_japanese.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE word(id INTEGER PRIMARY KEY AUTOINCREMENT, word STRING, result STRING)'
        )
        conn.commit()
        conn.close()

    def read_database(self, mode):
        if mode == '1':
            dbname = 'asset/word_english.db'
        else:
            dbname = 'asset/word_japanese.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        df_word = pd.read_sql('SELECT word FROM word', conn).values.tolist()
        df_word = itertools.chain.from_iterable(df_word)
        df_result = pd.read_sql('SELECT result FROM word', conn).values.tolist()
        df_result = itertools.chain.from_iterable(df_result)

        dic = dict(zip(list(df_word), list(df_result)))
        cur.execute('DELETE FROM word')

        conn.commit()

        cur.close()
        conn.close()

        return dic

    def prepare(self, mode):
        word = input('input word in here: ').strip().split()

        with open('asset/word.txt', 'r') as f:
            for i in f:
                word.append(i.replace(' ', '').replace('\n', ''))
        d = self.read_database(self.mode)

        self.word = set(word) - set(d.keys())
        if len(word) == 0:
            self.word = []

        for i in self.word:
            url = self.url + i
            res = requests.get(url)
            soup = bs4(res.text, 'lxml')
            if mode == "1":
                result = soup.find("span", class_="content-explanation ej").get_text().replace(' ', '').replace('\n', '')
                self.result.append(result)
            else:
                result = soup.find("span", class_="content-explanation je").get_text().replace(' ', '').replace('\n', '')
                self.result.append(result)
            sleep(5)

        dic2 = dict(zip(list(self.word), self.result))

        return dic2

    def main(self):
        try:
            dic = self.read_database(self.mode)
            dic2 = self.prepare(self.mode)

            dct3 = dic | dic2

            if self.mode == '1':
                dbname = 'asset/word_english.db'
            else:
                dbname = 'asset/word_japanese.db'
            conn = sqlite3.connect(dbname)
            cur = conn.cursor()

            for i in range(len(dct3.keys())):
                sql = 'INSERT INTO word(id, word, result) values(' + str(i) + ',' + '"' + str(
                    list(dct3.keys())[i]) + '"' + ',' + '"' + str(list(dct3.values())[i]) + '"' + ')'
                cur.execute(sql)

            conn.commit()
            cur.close()
            conn.close()

            with open('asset/word.txt', 'w') as f:
                f.write('')

        except pandas.io.sql.DatabaseError:
            if self.mode == '1':
                self.make_english_database()
                dic = self.read_database(self.mode)
                dic2 = self.prepare(self.mode)

                dct3 = dic | dic2

                if self.mode == '1':
                    dbname = 'asset/word_english.db'
                else:
                    dbname = 'asset/word_japanese.db'
                conn = sqlite3.connect(dbname)
                cur = conn.cursor()

                for i in range(len(dct3.keys())):
                    sql = 'INSERT INTO word(id, word, result) values(' + str(i) + ',' + '"' + str(
                        list(dct3.keys())[i]) + '"' + ',' + '"' + str(list(dct3.values())[i]) + '"' + ')'
                    cur.execute(sql)

                conn.commit()
                cur.close()
                conn.close()

                with open('asset/word.txt', 'w') as f:
                    f.write('')

            elif self.mode == '2':
                self.make_japanese_database()
                dic = self.read_database(self.mode)
                dic2 = self.prepare(self.mode)

                dct3 = dic | dic2

                if self.mode == '1':
                    dbname = 'asset/word_english.db'
                else:
                    dbname = 'asset/word_japanese.db'
                conn = sqlite3.connect(dbname)
                cur = conn.cursor()

                for i in range(len(dct3.keys())):
                    sql = 'INSERT INTO word(id, word, result) values(' + str(i) + ',' + '"' + str(
                        list(dct3.keys())[i]) + '"' + ',' + '"' + str(list(dct3.values())[i]) + '"' + ')'
                    cur.execute(sql)

                conn.commit()
                cur.close()
                conn.close()

                with open('asset/word.txt', 'w') as f:
                    f.write('')

            else:
                raise ValueError("Please input '1' or '2'")


if __name__ == '__main__':
    MakeWordList().main()
