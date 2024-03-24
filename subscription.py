from subscriber import Subscriber

def main():
    sub = Subscriber.get()
    sub.add_subscriber()


if __name__ == "__main__":
    main()