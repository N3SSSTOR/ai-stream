from moviepy import editor 

BASE_DIR = "assets/"

X_OFFSET = 80
X_MARGIN = 560
Y_OFFSET = 100 
IMG_SCALE = 0.35 
BASE_DURATION = 180
IMG_DURATION = BASE_DURATION
VIDEO_DURATION = 20

PERSON_1_POS = (X_OFFSET, Y_OFFSET)
PERSON_2_POS = (X_OFFSET + X_MARGIN, Y_OFFSET)


def test() -> None:
    layout = editor.ImageClip(BASE_DIR + "img/layout_3.png").set_duration(BASE_DURATION)

    img1 = editor.ImageClip(BASE_DIR + "img/broke_max.jpeg")\
        .set_duration(BASE_DURATION)\
        .resize(IMG_SCALE)

    img2 = editor.ImageClip(BASE_DIR + "img/journalist.jpeg")\
        .set_duration(BASE_DURATION)\
        .resize(IMG_SCALE)
    
    # videos = []
    # for i in range(0, BASE_DURATION, VIDEO_DURATION):
    #     videos.append(
    #         editor.VideoFileClip(BASE_DIR + "video/stock/journalist.mp4")\
    #             .set_position(PERSON_2_POS)\
    #             .set_duration(VIDEO_DURATION)\
    #             .set_start(i)\
    #             .resize(img2.size)
    #     )

    clips = editor.CompositeVideoClip([
        layout,
        img1.set_position(PERSON_1_POS),
        img2.set_position(PERSON_2_POS),
        # *videos
    ])

    clips.write_videofile("result.mp4", fps=1)


def main() -> None:
    test()


if __name__ == "__main__":
    main()