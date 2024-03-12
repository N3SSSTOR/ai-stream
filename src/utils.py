import moviepy.editor as mvp 

from person.ai import PersonAI
from person.speech import Speech

from config import OPENAI_API_KEY, PROXY_URL, SPEECH_TOKEN
from config import PERSON_1, PERSON_2

from donation.utils import get_donations
from donation.database._requests import add_processed_donation, get_processed_donations


def create_video(file_path: str) -> None:
    scenes_dir = "assets/video/scenes/"

    scene_audio = mvp.AudioFileClip(file_path)

    scene_broke_max_talking = mvp.VideoFileClip(scenes_dir + "broke_max_talking.mp4")
    scene_journalist_talking = mvp.VideoFileClip(scenes_dir + "journalist_talking.mp4")
    scene_pause = mvp.VideoFileClip(scenes_dir + "pause.mp4")

    file_data = file_path.replace("upload/audio/", "").replace(".wav", "").split("_")

    speaker = int(file_data[0])
    counter = int(file_data[1])

    # print(speaker)
    # print(counter)

    return 


async def dialog_generation() -> None:
    speech = Speech(SPEECH_TOKEN)

    person_config = dict(openai_api_key=OPENAI_API_KEY, proxy_url=PROXY_URL)

    person_1 = PersonAI(**person_config, model=PERSON_1)
    person_2 = PersonAI(**person_config, model=PERSON_2)

    question = await person_2.generate_answer("Можешь задать первый вопрос.", temperature=0.5)

    counter = 0 
    while True:     
        counter += 1
        file_path = await speech.text_to_speech(
            text=question,
            voice=PERSON_2.voice,
            file_name=f"2_{counter}"
        )
        create_video(file_path)

        print(f"\n\n{'='*5} САВЕЛИЙ ЖУРНАЛИСТОВ: {'='*5}\n\n{question}\nFILE PATH: {file_path}")

        answer = await person_1.generate_answer(question, temperature=0.5)

        counter += 1
        file_path = await speech.text_to_speech(
            text=answer,
            voice=PERSON_1.voice,
            file_name=f"1_{counter}"
        )

        print(f"\n\n{'='*5} МАКС МАКСБЕТОВ: {'='*5}\n\n{answer}\nFILE PATH: {file_path}")

        question = ""

        all_donations = await get_donations()
        processed_donations = await get_processed_donations()

        for donation in all_donations:
            if donation.get("id") not in processed_donations:
                question = (
                    f"Макс, зритель по имени {donation.get('username')} " 
                    f"отправил вам {donation.get('amount')} рублей и задал "
                    f"вопрос: {donation.get('message')}"
                )
                await add_processed_donation(donation.get("id"))
                break 

        if not question:
            question = await person_2.generate_answer(answer, temperature=0.5) 