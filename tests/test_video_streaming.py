import sys 
sys.path.append("/Users/imac/Desktop/projects/edu/max-maxbetov/src")

import asyncio 
import moviepy.editor as mvp 

from utils import video_streaming
from donation.utils import get_donations


async def test() -> None:
    result = await video_streaming() 
    print(result)


def main() -> None:
    # asyncio.run(test()) 
    print(mvp.TextClip.list("color"))


if __name__ == "__main__":
    main()