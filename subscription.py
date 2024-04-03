from subscriber import Subscriber
import os

def main():
    print("Press ctrl+c to stop adding/removing subscribers")   
    while True:
        try:
            sub = Subscriber.get()
            print("Press 1 to add a subscriber")
            print("Press 2 to remove a subscriber")
            operation = input("")
            if operation == "1":
                sub.add_subscriber()
            elif operation == "2":
                sub.remove_subscriber()
            else:
                clear_terminal()
                print("Invalid choice. Try again")
        except KeyboardInterrupt:
            break

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')



if __name__ == "__main__":
    main()