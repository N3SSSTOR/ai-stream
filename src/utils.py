import time  

from models import MaxMaxbetov, SaveliiJournalistov

from person import Person 
from speech import Speech

from config import OPENAI_API_KEY, PROXY_URL, SPEECH_TOKEN

from donation.utils import get_donations
from donation.database._requests import add_processed_donation, get_processed_donations


async def dialog_generation() -> None:
    speech = Speech(SPEECH_TOKEN)

    person_config = dict(openai_api_key=OPENAI_API_KEY, proxy_url=PROXY_URL)

    person_1 = Person(
        **person_config,
        base_prompt=MaxMaxbetov.PROMPT.value,
        words_correction=MaxMaxbetov.WORDS_CORRECTION.value 
    )
    person_2 = Person(**person_config, base_prompt=SaveliiJournalistov.PROMPT.value)

    question = await person_2.generate_answer("Можешь задать первый вопрос.", temperature=0.5)

    counter = 0 
    while True:     
        counter += 1

        # file_path = await speech.text_to_speech(
        #     text=question,
        #     voice=SaveliiJournalistov.VOICE.value,
        #     file_name=f"sav_{counter}_{int(time.time())}"
        # )
        print(f"\n\n{'='*5} САВЕЛИЙ ЖУРНАЛИСТОВ: {'='*5}\n\n{question}\nFILE PATH: {'file_path'}")

        answer = await person_1.generate_answer(question, temperature=0.5)
        # file_path = await speech.text_to_speech(
        #     text=answer,
        #     voice=MaxMaxbetov.VOICE.value,
        #     file_name=f"max_{counter}_{int(time.time())}"
        # )
        print(f"\n\n{'='*5} МАКС МАКСБЕТОВ: {'='*5}\n\n{answer}\nFILE PATH: {'file_path'}")

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