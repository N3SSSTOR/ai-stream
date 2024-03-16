import random 

import openai 
import httpx 

from .models import PersonModel
from ._types import TextModel


class PersonAI:

    def __init__(
        self,
        openai_api_key: str,
        proxy_url: str,
        model: PersonModel,
        text_model: str = TextModel.LARGE.value,
        wipe_memory_after: int | None = None 
    ) -> None:
        self.words_correction = model.words_correction
        self.text_model = text_model
        self.wipe_memory_after = wipe_memory_after
        self.messages = []
        self.messages.append({
            "role": "system", 
            "content": model.prompt
        })

        http_client = None 
        if proxy_url:
            http_client = httpx.AsyncClient(proxies={
                "https://": proxy_url
            })
        
        self.client = openai.AsyncOpenAI(
            api_key=openai_api_key,
            http_client=http_client
        )

    async def generate_answer(self, prompt: str, **kwargs) -> str:
        self.messages.append({"role": "user", "content": prompt})
        chat_completion = await self.client.chat.completions.create(
            messages=[
                *self.messages,
            ],
            model=self.text_model,
            n=1,
            **kwargs 
        )

        answer = chat_completion.choices[0].message.content 
        self.messages.append({"role": "assistant", "content": answer})

        if self.wipe_memory_after:
            if len(self.messages) > self.wipe_memory_after:
                self.messages = [self.messages[0]]

        answer = answer.replace('"', "")

        if self.words_correction:
            for k, v in self.words_correction.items():
                answer = answer.replace(k, random.choice(v))
                answer = answer.replace(k.title(), random.choice(v).title())

        return answer