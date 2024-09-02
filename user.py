import json
    
def change(uid, content):
    # 如果uid存在，在user列表中添加新的内容
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data[str(uid)].append({"role": "user", "content": content})
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("Sava the file of user!!!")
def change_system(uid, content):
    # GPT回答
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data[str(uid)].append({'role': 'system', 'content': content})
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("Sava the file of system!!!")

def add_new(uid, ask):
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    new_key = str(uid)
    new_value = [
        {"role": "system", "content": '你好，我是ChatGPT'},
        {"role": "user", "content": ask}
    ]
    data[new_key] = new_value  # 这将添加新的条目，如果键已存在，它将覆盖那个键的值
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def clear(uid, ask):
    with open('users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    new_key = str(uid)
    new_value = [
        {"role": "system", "content": '你好，我是ChatGPT'},
        {"role": "user", "content": ask}
    ]
    data[new_key] = new_value  # 这将添加新的条目，如果键已存在，它将覆盖那个键的值
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)