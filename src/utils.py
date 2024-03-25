import contextlib
import subprocess 
import asyncio 
import json 
import time 
import os 

import moviepy.editor as mvp 

from person.ai import PersonAI
from person.speech import Speech

from config import OPENAI_API_KEY, PROXY_URL, SPEECH_TOKEN, STREAM_KEY, STREAM_URL
from config import PERSON_1, PERSON_2, FPS, TEXT_MODEL, TEMPERATURE, WIPE_PERSON_MEMORY_AFTER 
from config import AUDIO_DIR, RESULT_DIR, MAIN_DIR, IN_PROCESS_DIR, MAIN_FONT_PATH, INFO_PATH

from donation.utils import get_donations
from donation.database._requests import add_processed_donation, get_processed_donations


def clean_app() -> None:
    dirs = [MAIN_DIR, AUDIO_DIR, RESULT_DIR, IN_PROCESS_DIR]
    for dir in dirs:
        files = os.listdir(dir)
        for file in files:
            if file.lower().endswith(".mp3") or file.lower().endswith(".mp4") or file.lower().endswith(".wav"):
                os.remove(dir + file)

    with open(INFO_PATH, "r") as f:
        info = json.loads(f.read()) 

    with open(INFO_PATH, "w") as f:
        updated_info = info.copy()
        updated_info["current_video_number"] = 0

        f.write(json.dumps(updated_info, indent=4))


def video_streaming() -> None:
    counter = 1
    while True:
        try:
            time.sleep(1)

            files = os.listdir(RESULT_DIR)
            sorted_files = sorted(
                files, 
                key=lambda x: int(x.split(".")[0])
            )

            for file in sorted_files:
                if file.lower().endswith(".mp4"):
                    file_counter = int(file.split(".")[0])

                    if file_counter == counter:
                        video_path = f"{RESULT_DIR}/{file}"
                        query = (
                            f"ffmpeg -re -i {video_path} -c:v libx264 -c:a aac -f flv "
                            f"{STREAM_URL}/{STREAM_KEY}"
                        )

                        with open(INFO_PATH, "r") as f:
                            info = json.loads(f.read()) 

                        with open(INFO_PATH, "w") as f:
                            updated_info = info.copy()
                            updated_info["current_video_number"] = counter

                            f.write(json.dumps(updated_info, indent=4))

                        with contextlib.suppress(Exception):
                            subprocess.run(query.split(" "))

                        if counter > 10:
                            os.remove(f"{RESULT_DIR}{counter-10}.mp4")

                        counter += 1

        except Exception as e:
            print(e)


def create_video(file_path: str, donations: list) -> None:
    scene_audio = mvp.AudioFileClip(file_path)

    file_data = file_path.replace(AUDIO_DIR, "").replace(".wav", "").split("_")

    speaker = int(file_data[0])
    counter = int(file_data[1])

    if speaker == 1:
        current_scene = mvp.VideoFileClip(PERSON_1.talking_scene_path)
    else:
        current_scene = mvp.VideoFileClip(PERSON_2.talking_scene_path) 

    current_scene = current_scene.set_duration(scene_audio.duration)\
        .set_audio(scene_audio)
    
    result_scene_pattern = [current_scene]
    
    if donations:
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

        result_scene_pattern.append(donations_count_label)
        result_scene_pattern += donations_labels
    
    result_scene = mvp.CompositeVideoClip(result_scene_pattern) 

    process_path = IN_PROCESS_DIR + str(counter) + ".mp4"
    result_scene.write_videofile(
        process_path, 
        fps=FPS
    )

    query = f"mv {process_path} {process_path.replace(IN_PROCESS_DIR, RESULT_DIR)}"
    subprocess.run(query.split(" "))

    os.remove(file_path)


async def async_dialog_generation() -> None:
    speech = Speech(SPEECH_TOKEN)

    person_kwargs = dict(
        openai_api_key=OPENAI_API_KEY, 
        proxy_url=PROXY_URL, 
        text_model=TEXT_MODEL,
        wipe_memory_after=WIPE_PERSON_MEMORY_AFTER 
    )

    person_1 = PersonAI(**person_kwargs, model=PERSON_1)
    person_2 = PersonAI(**person_kwargs, model=PERSON_2)

    question = await person_2.generate_answer(
        "Можешь задать первый вопрос.", 
        temperature=TEMPERATURE
    )

    counter = 0 
    while True:  
        with open(INFO_PATH, "r") as f:
            info = json.loads(f.read())
            stream_counter = info.get("current_video_number")

        if stream_counter + 5 > counter:
            counter += 1

            all_donations = await get_donations()

            file_path = await speech.text_to_speech(
                text=question,
                voice=PERSON_2.voice,
                file_name=f"2_{counter}_{int(time.time())}"
            )
            create_video(file_path, all_donations)

            print(f"\n\n{'='*5} PERSON II: {'='*5}\n\n{question}\nFILE PATH: {file_path}")

            answer = await person_1.generate_answer(question, temperature=TEMPERATURE)

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

            if all_donations:
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
                question = await person_2.generate_answer(answer, temperature=TEMPERATURE) 
        
        else:
            print("Стрим не успевает за генерацией...")
            await asyncio.sleep(1)