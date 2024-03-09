import random 

import openai 
import httpx 


class Person:

    def __init__(
        self,
        base_prompt: str,
        openai_api_key: str,
        proxy_url: str,
        words_correction: dict[str, list[str]] | None = None 
    ) -> None:
        self.words_correction = words_correction
        self.messages = []
        self.messages.append({"role": "system", "content": base_prompt})

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