import sys 
sys.path.append("/Users/imac/Desktop/projects/edu/max-maxbetov/src")

import subprocess
import asyncio 

from utils import video_streaming
from config import STREAM_KEY, STREAM_URL


def test() -> None:
    # path = "upload/video/2.mp4"

    # server = STREAM_URL
    # key = STREAM_KEY

    # query = f"ffmpeg -re -i {path} -f flv {server}/{key}"

    # subprocess.run(query.split(" "))
    # print("\n\nTHE END")
    print(STREAM_KEY)


def async_test() -> None:
    asyncio.run(video_streaming())


def main() -> None:
    test()


if __name__ == "__main__":
    main()