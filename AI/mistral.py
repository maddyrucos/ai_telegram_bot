from mistralai import Mistral
from openai import api_key

import config
import logging

async def get_response(prompt):
    client = Mistral(api_key=config.MISTRAL_TOKEN)

    try:
        chat_response = client.chat.complete(
            model='mistral-medium-latest',
            temperature=0,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )

        return chat_response.choices[0].message.content
    except Exception as e:
        logging.CRITICAL(e.args)
        print(e)
        return 'Произошла ошибка'