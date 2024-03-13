import time 
import os 

import moviepy.editor as mvp 

from person.ai import PersonAI
from person.speech import Speech

from config import OPENAI_API_KEY, PROXY_URL, SPEECH_TOKEN, CHANNEL_URL
from config import PERSON_1, PERSON_2, PAUSE_SCENE_PATH, PAUSE_SCENE_DURATION

from donation.utils import get_donations
from donation.database._requests import add_processed_donation, get_processed_donations


def create_video(file_path: str, donations: list) -> None:
    scene_audio = mvp.AudioFileClip(file_path)
    scene_pause = mvp.VideoFileClip(PAUSE_SCENE_PATH).set_duration(PAUSE_SCENE_DURATION)

    file_data = file_path.replace("upload/audio/", "").replace(".wav", "").split("_")

    speaker = int(file_data[0])
    counter = int(file_data[1])

    if speaker == 1:
        current_scene = mvp.VideoFileClip(PERSON_1.talking_scene_path)
    else:
        current_scene = mvp.VideoFileClip(PERSON_2.talking_scene_path) 

    current_scene = current_scene.set_duration(scene_audio.duration)\
        .set_audio(scene_audio)
    channel_label = mvp.TextClip(txt=CHANNEL_URL, 
                                 color="white",
                                 fontsize=45)\
        .set_duration(current_scene.duration)\
        .set_position((80, 25))
    
    result_scene = mvp.CompositeVideoClip([
        current_scene,
        channel_label,
        scene_pause.set_start(current_scene.duration)
    ]) 

    result_scene.write_videofile(f"upload/video/{counter}_{int(time.time())}.mp4", fps=12)
    os.remove(file_path)


async def dialog_generation() -> None:
    speech = Speech(SPEECH_TOKEN)

    person_config = dict(openai_api_key=OPENAI_API_KEY, proxy_url=PROXY_URL)

    person_1 = PersonAI(**person_config, model=PERSON_1)
    person_2 = PersonAI(**person_config, model=PERSON_2)

    question = await person_2.generate_answer("Можешь задать первый вопрос.", temperature=0.5)

    counter = 0 
    while True:     
        try:
            counter += 1

            all_donations = await get_donations()

            file_path = await speech.text_to_speech(
                text=question,
                voice=PERSON_2.voice,
                file_name=f"2_{counter}_{int(time.time())}"
            )
            create_video(file_path, all_donations)

            print(f"\n\n{'='*5} САВЕЛИЙ ЖУРНАЛИСТОВ: {'='*5}\n\n{question}\nFILE PATH: {file_path}")

            answer = await person_1.generate_answer(question, temperature=0.5)

            counter += 1
            file_path = await speech.text_to_speech(
                text=answer,
                voice=PERSON_1.voice,
                file_name=f"1_{counter}_{int(time.time())}"
            )
            create_video(file_path, all_donations)

            print(f"\n\n{'='*5} МАКС МАКСБЕТОВ: {'='*5}\n\n{answer}\nFILE PATH: {file_path}")

            question = ""
            processed_donations = await get_processed_donations()

            for donation in all_donations:
                if donation.get("id") not in processed_donations:
                    question = (
                        f"Зритель по имени {donation.get('username')} " 
                        f"отправил вам {donation.get('amount')} рублей и задал "
                        f"вопрос: {donation.get('message')}"
                    )
                    await add_processed_donation(donation.get("id"))
                    break 

            if not question:
                question = await person_2.generate_answer(answer, temperature=0.5) 

        except Exception as e:
            print(e)


async def video_streaming() -> None:
    videos_dir = "upload/video/"
    
    counter = 1
    while True:
        try:
            files = os.listdir(videos_dir)
            for file in files:
                if file.lower().endswith(".mp4"):
                    file_counter = int(file.split("_")[0])

                    if file_counter == counter:
                        counter += 1  

        except Exception as e:
            print(e)