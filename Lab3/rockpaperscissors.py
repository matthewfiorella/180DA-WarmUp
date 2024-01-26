import random

if __name__ == "__main__":
    print("Welcome to Rock Paper Scissors!: ")
    win_count = 0
    loss_count = 0
    while True:
        userInput = input("Choose Rock(r), Paper(p), Scissors(s): ")
        while userInput != "r" and userInput != "p" and userInput != "s":
            print("Please Choose r for Rock, p for Paper, s for Scissors")
            userInput = input("Make your choice (r/p/s): ")
        choices = ["r", "p", "s"]
        rand_idx = random.randint(0, len(choices) - 1)
        choice = choices[rand_idx]
        print("Computer Selected: " + choice)
        if choice == userInput:
            print("Tie")
        elif userInput == "r":
            if choice == "p":
                print("Computer Won!")
            elif choice == "s":
                print("You Won!")
        elif userInput == "p":
            if choice == "s":
                print("Computer Won!")
            elif choice == "r":
                print("You Won!")
        elif userInput == "s":
            if choice == "r":
                print("Computer Won!")
            elif choice == "p":
                print("You Won!")
        