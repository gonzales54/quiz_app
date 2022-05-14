from bs4 import BeautifulSoup as bs4
import requests


class Translate:
    def __init__(self):
        self.url = 'https://ejje.weblio.jp/content/'
        print('If you want to finish, input "1"')

    def input(self):
        word = input('Input word')
        return word

    def search(self, word):
        url = self.url + word
        res = requests.get(url)
        soup = bs4(res.text, 'lxml')
        result = soup.find("span", class_="content-explanation ej").get_text().replace(' ', '').replace('\n', '')
        return result

    def main(self):
        while True:
            word = input('Input Here: ')
            if word != "1":
                print(self.search(word))

            else:
                return False


if __name__ == '__main__':
    Translate().main()
