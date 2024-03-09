import os 
import time 
import json 
import wave 

import aiohttp 


class Speech:

    def __init__(
        self,
        token: str
    ) -> None:
        self.token = token

    async def get_cloud_id(self, iam_token: str) -> str:
        url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds"
        headers = {
            "Authorization": f"Bearer {iam_token}"
        }

        # response = requests.get(url, headers=headers)
        # return response.json().get("clouds")[0].get("id")
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json() 
                return data.get("clouds")[0].get("id")


    async def get_iam_token(self, token: str) -> dict:
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"

        headers = {"Content-Type": "application/json"}
        data = {"yandexPassportOauthToken": token}

        # response = requests.post(url, headers=headers, data=json.dumps(data))
        # response_data = response.json()
        # return response_data.get("iamToken")
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.post(
                url, 
                headers=headers, 
                data=json.dumps(data)
            ) as response:
                data = await response.json() 
                return data.get("iamToken")


    async def get_folder_id(self, token: str) -> str:
        iam_token = await self.get_iam_token(token)

        if iam_token:
            cloud_id = await self.get_cloud_id(iam_token)

            url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders"

            params = {"cloudId": cloud_id }
            headers = {"Authorization": f"Bearer {iam_token}"}

            # response = requests.get(url, params=params, headers=headers)
            # return response.json().get("folders")[0].get("id")
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
            ) as session:
                async with session.get(
                    url,
                    params=params, 
                    headers=headers
                ) as response:
                    data = await response.json() 
                    return data.get("folders")[0].get("id")


    async def text_to_speech(
        self,
        text: str, 
        voice: str, 
        file_name: str = ""
    ) -> str:
        if not file_name:
            file_name = str(int(time.time()))

        iam_token = await self.get_iam_token(self.token)
        folder_id = await self.get_folder_id(self.token)

        url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        
        headers = {"Authorization": f"Bearer {iam_token}",}
        data = {
            "text": text,
            "lang": "ru-RU",
            "voice": voice,
            "folderId": folder_id,
            "format": "lpcm",
            "sampleRateHertz": "48000"
        }

        # response = requests.post(url, headers=headers, data=data)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.post(
                url, 
                headers=headers, 
                data=data
            ) as response:       
                content = await response.read()     
                file_path = f"upload/{file_name}"

                raw_file_path = file_path + ".raw"
                with open(raw_file_path, "wb") as f:
                    f.write(content)

                wav_file_path = file_path + ".wav"
                with open(raw_file_path, "rb") as inp_f:
                    data = inp_f.read()
                    with wave.open(wav_file_path, "wb") as out_f:
                        out_f.setnchannels(1)
                        out_f.setsampwidth(2) 
                        out_f.setframerate(44100)
                        out_f.writeframesraw(data)
                
                os.remove(raw_file_path)
                return wav_file_path