from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import requests
import aiohttp

tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")

async def get_blender_responses(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
    for ids in output:
        yield tokenizer.decode(ids, skip_special_tokens=True)

async def get_zephyr_responses(prompt):
    url = 'https://ready-liger-possible.ngrok-free.app/generate'
    data = {"inputs": prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            json_data = await response.json()
            return json_data.get('generated_text')

async def get_coder_responses(prompt):
    url = 'https://e31c-46-53-253-133.ngrok-free.app/generate'
    data = {"inputs": prompt, "parameters":{"max_new_tokens":120}}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            json_data = await response.json()
            return json_data.get('generated_text')

async def get_image_responses(prompt):
    url = 'http://172.18.0.4:7000'
    data = {"prompt": prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            image_data = await response.read()
            return image_data

async def get_text_from_image(image):
    url='http://172.18.0.5:6000/image'
    response = requests.post(url, files=image)
    return response.text
