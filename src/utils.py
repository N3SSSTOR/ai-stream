import time  

from models import MaxMaxbetov, SaveliiJournalistov

from person import Person 
from speech import Speech



def dialog_generation() -> None:
    # speech = Speech()

    person_1 = Person(
        base_prompt=MaxMaxbetov.PROMPT.value,
        words_correction=MaxMaxbetov.WORDS_CORRECTION.value 
    )
    person_2 = Person(base_prompt=SaveliiJournalistov.PROMPT.value)

    question = person_2.generate_answer("Можешь задать первый вопрос.", temperature=0.5)
    counter = 0 
    while True:     
        counter += 1

        # file_path = speech.text_to_speech(
        #     text=question,
        #     voice=SaveliiJournalistov.VOICE.value,
        #     file_name=f"sav_{counter}_{int(time.time())}"
        # )
        print(f"\n\n{'='*5} САВЕЛИЙ ЖУРНАЛИСТОВ: {'='*5}\n\n{question}\nFILE PATH: {'None'}")

        answer = person_1.generate_answer(question, temperature=0.5)
        # file_path = speech.text_to_speech(
        #     text=answer,
        #     voice=MaxMaxbetov.VOICE.value,
        #     file_name=f"max_{counter}_{int(time.time())}"
        # )
        print(f"\n\n{'='*5} МАКС МАКСБЕТОВ: {'='*5}\n\n{answer}\nFILE PATH: {'None'}")

        question = person_2.generate_answer(answer, temperature=0.5) 


def answer_generation() -> None:
    person = Person(
        base_prompt=MaxMaxbetov.PROMPT.value,
        words_correction=MaxMaxbetov.WORDS_CORRECTION.value 
    )

    prompt = input(">>> ")
    while True:
        print(person.generate_answer(prompt))
        prompt = input(">>> ")