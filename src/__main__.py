from utils import dialog_generation


def main() -> None:
    dialog_generation()
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExit") 