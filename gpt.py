import openai
import config
import json
from base64 import b64decode

openai.api_key = config.OPENAI_TOKEN

def generate_response(prompt):
    response = openai.Completion.create(
        prompt = prompt,
        engine = 'text-davinci-003',
        max_tokens = 1000,
        n = 1,
        timeout= 15,
    )

    if response and response.choices:
        return response.choices[0].text
    else:
        return None

def generate_image(prompt, username):
    response = openai.Image.create(
        prompt = prompt,
        n = 1,
        size = '1024x1024',
        response_format = 'b64_json'
    )

    with open('data.json', 'w') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    image_data = b64decode(response['data'][0]['b64_json'])
    file_name = str(username)

    with open(f'{file_name}.png', 'wb') as file:
        file.write(image_data)

    file_name += '.png'
    return str(file_name)

if __name__ == '__main__':

    image_data = b64decode(response['data'][0]['b64_json'])
    file_name = '_'.join(prompt.split(' '))

    with open(f'{file_name}.png', 'wb') as file:
        file.write(image_data)