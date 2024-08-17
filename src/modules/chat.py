# TODO:
# [] 他の部分とのインターフェースをつくr
# [] このファイルをクラス化する 

from openai import OpenAI
import os
import json


# グローバルでOpenAIのクライエントを定義すると、どこからでも使える
client = OpenAI()
file_path = "conversation.json"


# 会話のデフォルト設定を設定する
default_conversation = {
    "messages": [{"role": "system", "content": "文字制限は20文字以内。あなたは役にたつアシスタントです。"}],
    "temperature": 0.7,
}

class t_color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RESET = '\033[0m'


# 会話ファイルの形式を確認
def check_conversation_json_validity(data):
    # Check if 'messages' is a list
    if not isinstance(data.get('messages'), list):
        return False

    for message in data['messages']:
        # Each message should be a dictionary
        if not isinstance(message, dict):
            return False

        # Each message should have 'role' and 'content'
        if 'role' not in message or 'content' not in message:
            return False

        if not isinstance(message['role'], str) or not isinstance(message['content'], str):
            return False

        # 'role' should be one of the allowed values
        if message['role'] not in {'system', 'user', 'assistant'}:
            return False

        # Optional 'sound_path' should be a string if present
        if 'sound_path' in message and message['sound_path'] is not None and not isinstance(message['sound_path'], str):
            return False

    # 'temperature' should be a float, if present
    if 'temperature' in data and not isinstance(data['temperature'], float):
        return False

    return True

# 会話の履歴とパラメータをロード
def load_conversation(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read().strip()  # Read and strip whitespace
            if content:  # Check if there's any content left after stripping
                try:
                    data = json.loads(content)
                    if check_conversation_json_validity(data):
                        return data
                except json.JSONDecodeError:
                    pass
    return default_conversation

# 会話の履歴とパラメータを保存
def save_conversation(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    

def reset_conversation(file_path):
    save_conversation(file_path, default_conversation)
    return default_conversation["messages"], default_conversation["temperature"]

def chat_with_gpt(messages, model="gpt-3.5-turbo", temperature=0.7):
    messages_to_send = prepare_for_api(messages)

    response = client.chat.completions.create(
        model=model,
        messages=messages_to_send,
        temperature=temperature
    )

    response_content =  response.choices[0].message.content
    print("chatGPT: ", response_content)
    return response_content

def prepare_for_api(messages_list_with_sound):
    cleaned_messages = []
    for message in messages_list_with_sound:
        cleaned_message = {key: value for key, value in message.items() if key != 'sound_path'}
        cleaned_messages.append(cleaned_message)
    return cleaned_messages

# to implement
def get_gpt_completion(transcript, user_sound_path=None, gpt_sound_path=None):
    """
    main()関数の代わりになる。外部と一緒に最も使われるインターフェース。
    音声認識が終わって、この関数が呼ばれると、以下の流れが行われる。
    1. 音声認識の結果をmessagesに入れる
    2. chat_with_gptを呼ぶ
    3. 返事をmessagesに入れる
    4. 会話を conversation.json 記録する
    5. responseを返す
    """
    data = load_conversation(file_path)
    messages = data["messages"]
    temperature = data["temperature"]
    response = ""

    messages.append({"role": "user", "content": transcript, "sound_path": user_sound_path})

    try:
        response = chat_with_gpt(messages, temperature=temperature)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    messages.append({"role": "assistant", "content": response, "sound_path": gpt_sound_path})
    
    # 会話を保存
    data["messages"] = messages
    save_conversation(file_path, data)
    return response

def print_full_conversation(messages_list):
    for message in messages_list:
        if message["role"] == "user":
            print(f"あなた: {message['content']}")
        elif message["role"] == "assistant":
            print(f"chatGPT: {message['content']}")
    print("---------- 以上は会話の歴史 ----------")

def main():
    data = load_conversation(file_path)
    messages = data["messages"]
    temperature = data["temperature"]

    # 最初の説明
    print("これはコマンドラインでchatGPTと対話するシステムです")
    print(f"中断するためには {t_color.RED}exit{t_color.RESET} と入力してください")
    print(f"会話の記録をリセットするためには {t_color.RED}reset{t_color.RESET} と入力してください")
    print(f"会話の履歴は {t_color.GREEN}conversation.json{t_color.RESET} というファイルに保存される")
    print()

    print_full_conversation(messages)

    while True:
        user_input = input("あなた：")
        
        if user_input.lower() == "exit":
            print("会話を終了する")
            break

        if user_input.lower() == "reset":
            print("会話の履歴をリセットする")
            res_messages, res_temp = reset_conversation(file_path)
            messages = res_messages
            temperature = res_temp
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            response = chat_with_gpt(messages, temperature=temperature)
            messages.append({"role": "assistant", "content": response})
        except Exception as e:
            print(f"Error: {e}")

    data["messages"] = messages
    save_conversation(file_path, data)

if __name__ == "__main__":
    main()
