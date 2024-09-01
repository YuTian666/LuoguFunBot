import os
from openai import OpenAI
import requests
import json
import time

API_SECRET_KEY = "";
BASE_URL = "https://api.zhizengzeng.com/v1/"
init_ask = ''
with open("settings.json" ,"r", encoding="utf-8") as set:
    settings = json.load(set)
    init_ask = settings.get('__ask')

model_list = [
    "gpt-4o-mini",
    "gpt-4",
    "gpt-3.5-turbo"
]

def chat_gpt(model, messages):
    client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model=model,
        messages = messages
        # messages=[
        #     {"role": "system", "content": init_ask},
        #     {"role": "user", "content": query}
        # ]
    )
    # print(resp)
    return resp.choices[0].message.content
def if_msg(query):
    client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "user", "content": f"'{query}'是一个用户的发言，请你判断是否危害了网络发言，是只输出“true”，否则输出“false”，不用加引号"}
        ]
    )
    # print(resp)
    return resp.choices[0].message.content
def credit_grants():
    api_secret_key = API_SECRET_KEY;  # 智增增的secret_key
    url = BASE_URL+'/dashboard/billing/credit_grants'; # 余额查询url
    headers = {'Content-Type': 'application/json', 'Accept':'application/json',
               'Authorization': "Bearer "+api_secret_key}
    resp = requests.post(url, headers=headers)
    res = resp.json()
    return res['grants']['available_amount']

#     chat_completions4("'****'是一个用户的发言，请你判断是否危害了网络发言，是只输出“true”，否则输出“false”");