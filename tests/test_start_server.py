import sys 
sys.path.append("/Users/imac/Desktop/projects/ai-stream/src")

from donation.server import run_server


def test() -> None:
    query1 = (
        f"ffmpeg "
        f"-reconnect 1 "
        f"-reconnect_at_eof 1 "
        f"-reconnect_streamed 1 "
        f"-reconnect_delay_max 2 "
        f"-re "
        f"-i {1} "
        f"-c:v libx264 -c:a aac "
        f"-preset ultrafast "
        f"-crf 0 "
        f"-threads 3 "
        f"-f flv {123}/{321}"
    )

    query2 = [
        "ffmpeg",
        "-reconnect", "1",
        "-reconnect_at_eof", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "2",
        "-re",
        "-i", "1",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "ultrafast",
        "-crf", "0",
        "-threads", "3",
        "-f", "flv", f"{123}/{321}"
    ]
    print(query1.split(" ") == query2)


def main() -> None:
    test()


if __name__ == "__main__":
    main()