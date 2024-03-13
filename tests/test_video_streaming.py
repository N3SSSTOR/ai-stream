import sys 
sys.path.append("/Users/imac/Desktop/projects/edu/max-maxbetov/src")

import asyncio 
from utils import video_streaming


async def test() -> None:
    result = await video_streaming() 
    print(result)


def main() -> None:
    asyncio.run(test()) 


if __name__ == "__main__":
    main()