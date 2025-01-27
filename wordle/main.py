import random


f=open("words.txt","r")
lines=f.readlines()

def gamelogic(word):
    for i in range(len(word)):
        print("X",end='')
    print("\n")
    chances=5
    while chances>0:
        guess=input("Enter a letter: ")
        guesses=''
        for i in word:
            if i in guesses:
                print(i,end='')
            else:
                print("X",end='')
        print("\n")
        if guess in word:
            guesses+=guess
        else:
            chances-=1
            print("Chances left: ",chances)
        if guesses==word:
            pass
if  __name__ == "__main__":
    word= "touch"
    gamelogic(word)
    

#Screenshot_2024-12-02 at 12.38.39 AM (3).png