from contextlib import suppress
import subprocess 
import time 
import os 

import moviepy.editor as mvp 

from person.ai import PersonAI
from person.speech import Speech

from config import (
    OPENAI_API_KEY, PROXY_URL, 
    SPEECH_TOKEN, STREAM_KEY, 
    STREAM_URL, PERSON_1, 
    PERSON_2, FPS, 
    MAIN_FONT_PATH, TEXT_MODEL
)

from donation.utils import get_donations
from donation.database._requests import add_processed_donation, get_processed_donations


def create_video(file_path: str, donations: list) -> None:
    scene_audio = mvp.AudioFileClip(file_path)

    file_data = file_path.replace("upload/audio/", "").replace(".wav", "").split("_")

    speaker = int(file_data[0])
    counter = int(file_data[1])

    if speaker == 1:
        current_scene = mvp.VideoFileClip(PERSON_1.talking_scene_path)
    else:
        current_scene = mvp.VideoFileClip(PERSON_2.talking_scene_path) 

    current_scene = current_scene.set_duration(scene_audio.duration)\
        .set_audio(scene_audio)
    
    donations_count_label = mvp.TextClip(txt=f"Всего донатов: {len(donations)}", 
                                 color="white",
                                 font=MAIN_FONT_PATH,
                                 fontsize=45)\
        .set_duration(current_scene.duration)\
        .set_position((80, 25))
    
    top_donations = sorted(donations, key=lambda x: x['amount'], reverse=True)[:5]
    donations_labels = []

    x_offset = 1225
    y_offset = 60 
    y_spacing = 125 

    for i, donation in enumerate(top_donations):
        donations_labels.append(
            mvp.TextClip(
                txt=f"{donation.get('username')} - {donation.get('amount')} RUB",
                color="gold" if i == 0 else "gray",
                font=MAIN_FONT_PATH,
                fontsize=55 
            ).set_duration(current_scene.duration)\
             .set_position((x_offset, y_offset + (y_spacing * (i + 1))))
        )
    
    result_scene = mvp.CompositeVideoClip([
        current_scene,
        donations_count_label,
        *donations_labels,
    ]) 

    file_name = f"{counter}"

    process_path = f"upload/in_process/{file_name}.mp4"
    result_scene.write_videofile(
        process_path, 
        fps=FPS
    )

    query = f"mv {process_path} {process_path.replace('in_process', 'video')}"
    subprocess.run(query.split(" "))

    os.remove(file_path)


async def dialog_generation() -> None:
    speech = Speech(SPEECH_TOKEN)

    person_config = dict(
        openai_api_key=OPENAI_API_KEY, 
        proxy_url=PROXY_URL, 
        text_model=TEXT_MODEL,
        wipe_memory_after=5 
    )

    person_1 = PersonAI(**person_config, model=PERSON_1)
    person_2 = PersonAI(**person_config, model=PERSON_2)

    question = await person_2.generate_answer("Можешь задать первый вопрос.")

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

            print(f"\n\n{'='*5} PERSON II: {'='*5}\n\n{question}\nFILE PATH: {file_path}")

            answer = await person_1.generate_answer(question)

            counter += 1
            file_path = await speech.text_to_speech(
                text=answer,
                voice=PERSON_1.voice,
                file_name=f"1_{counter}_{int(time.time())}"
            )
            create_video(file_path, all_donations)

            print(f"\n\n{'='*5} PERSON I: {'='*5}\n\n{answer}\nFILE PATH: {file_path}")

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


def video_streaming() -> None:
    videos_dir = "upload/video/"
    
    counter = 1
    while True:
        try:
            time.sleep(1)

            files = os.listdir(videos_dir)
            sorted_files = sorted(
                files, 
                key=lambda x: int(x.split(".")[0])
            )

            for file in sorted_files:
                if file.lower().endswith(".mp4"):
                    file_counter = int(file.split(".")[0])

                    if file_counter == counter:
                        video_path = f"{videos_dir}/{file}"
                        query = (
                            f"ffmpeg -re -i {video_path} -f flv {STREAM_URL}/{STREAM_KEY}"
                        )

                        with suppress(Exception):
                            subprocess.run(query.split(" "))

                        if counter > 10:
                            os.remove(f"{videos_dir}{counter-10}.mp4")

                        counter += 1  

        except Exception as e:
            print(e)