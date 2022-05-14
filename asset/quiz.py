import itertools
import random
from time import sleep

import sqlite3
import pandas as pd
import pandas.io.sql


class Quiz:
    def __init__(self):
        print("""
Select which language quiz you want to do
1: English
2: Japanese
""")
        # self.mode = input('Input mode here(1 or 2): ')
        self.mode = "2"

    def quiz(self, mode):
        flg = 0
        try:
            if mode == "1":
                dbname = 'word_english.db'
            else:
                dbname = 'word_japanese.db'
            conn = sqlite3.connect(dbname)
            cur = conn.cursor()

            df_word = pd.read_sql('SELECT word FROM word', conn).values.tolist()
            df_result = pd.read_sql('SELECT result FROM word', conn).values.tolist()
            df_word = list(itertools.chain.from_iterable(df_word))
            df_result = list(itertools.chain.from_iterable(df_result))

            lng = len(df_word)

            l = list(range(lng))
            array_quiz_num = [[j for j in random.sample(l, 3)] for i in
                              range(0, lng)]

            for i in range(lng):
                answer = random.randint(0, 2)
                print("what does this word '{}' mean?".format(df_word[array_quiz_num[i][answer]]))
                for j in range(len(array_quiz_num[i])):
                    print("[{}] : {}".format(j + 1, df_result[array_quiz_num[i][j]]))

                inp = input('Input Answer: ')

                if inp == str(answer + 1):
                    print('Correct')
                    flg += 1
                    sleep(1)
                else:
                    print('Incorrect')
                print('\n')

                if i == lng - 1:
                    print('Your Score is {}/{}'.format(flg, lng))
                    sleep(3)
                    exit()

            cur.close()
            conn.close()

        except pandas.io.sql.DatabaseError:
            print('\033[31m' + 'Please Make Word List' + '\033[0m')
            sleep(2)
            exit()

    def main(self):
        self.quiz(self.mode)


if __name__ == '__main__':
    Quiz().main()
