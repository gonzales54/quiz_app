from asset import translate, make_wordlist, quiz


def main():
    print("""**Select mode
1:translate (Jan->Eng and Jan <- Eng)  
2:Make own word list  
3:quiz from word list   
""")
    mode = input('Input mode: ')
    if mode == "1":
        translate.Translate().main()

    elif mode == "2":
        make_wordlist.MakeWordList().main()

    else:
        quiz.Quiz().main()


if __name__ == '__main__':
    main()
