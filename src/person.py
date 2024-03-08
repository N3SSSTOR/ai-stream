import random 

import openai 
import httpx 

from config import OPENAI_API_KEY, PROXY_URL


class Person:

    def __init__(
        self,
        base_prompt: str,
        openai_api_key: str = OPENAI_API_KEY,
        proxy_url: str = PROXY_URL,
        words_correction: dict[str, list[str]] | None = None 
    ) -> None:
        self.words_correction = words_correction
        self.messages = []
        self.messages.append({"role": "system", "content": base_prompt})

        http_client = None 
        if proxy_url:
            http_client=httpx.Client(proxies={
                "https://": proxy_url
            }) 

        self.client = openai.OpenAI(
            api_key=openai_api_key,
            http_client=http_client
        )

    def generate_answer(self, prompt: str, **kwargs) -> str:
        self.messages.append({"role": "user", "content": prompt})
        chat_completion = self.client.chat.completions.create(
            messages=[
                *self.messages,
            ],
            model="gpt-3.5-turbo",
            n=1,
            **kwargs 
        )

        answer = chat_completion.choices[0].message.content 
        self.messages.append({"role": "assistant", "content": answer})

        answer = answer.replace('"', "")

        if self.words_correction:
            for k, v in self.words_correction.items():
                answer = answer.replace(k, random.choice(v))
                answer = answer.replace(k.title(), random.choice(v).title())

        return answer