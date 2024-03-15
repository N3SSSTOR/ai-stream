import sys 
sys.path.append("/Users/imac/Desktop/projects/edu/max-maxbetov/src")

from donation.server import run_server


def test() -> None:
    run_server()


def main() -> None:
    test()


if __name__ == "__main__":
    main()