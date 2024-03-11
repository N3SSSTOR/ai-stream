from moviepy import editor 

BASE_DIR = "assets/"


def main():
    layout_clip = editor.ImageClip(BASE_DIR + "img/layout_2.png")
    clips = [layout_clip]

    


if __name__ == "__main__":
    main()