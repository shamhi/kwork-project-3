import asyncio

import aiohttp

from app.config import Config


async def gpt_response(prompt: str, history: list[dict[str, str]]) -> str:
    url = "https://api.edenai.run/v2/text/chat"

    payload = {
        "temperature": 0,
        "max_tokens": 1000,
        "providers": "openai",
        "openai": "gpt-3.5-turbo",
        "text": prompt,
        "chatbot_global_action": Config.GLOBAL_ACTION,
        "previous_history": history
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {Config.EDEN_TOKEN}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, json=payload, headers=headers)
            print(response)
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After"))
                await asyncio.sleep(retry_after)
            response_data = await response.json()
            answer = response_data.get('openai', {}).get('generated_text')
            messages = response_data.get('openai', {}).get('message')
            print(response_data)

        return answer, messages
    except Exception as er:
        print(er)
        return None, None


async def speech_to_text(file_bytes):
    try:
        url = "https://api.edenai.run/v2/audio/speech_to_text_async"
        headers = {"authorization": f"Bearer {Config.EDEN_TOKEN}"}
        data = {
            "providers": "openai",
            "language": "ru-RU",
            'file': file_bytes
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                result = await response.json()
                text = result.get('results', {}).get('openai', {}).get('text')

                return text
    except Exception as er:
        print(er)
        return None
