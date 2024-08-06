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
 

# 会話の履歴とパラメータをロード
def load_conversation(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    return default_conversation

# 会話の履歴とパラメータを保存
def save_conversation(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    

def reset_conversation(file_path):
    save_conversation(file_path, default_conversation)
    return default_conversation["messages"], default_conversation["temperature"]

def chat_with_gpt(messages, model="gpt-3.5-turbo", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    response_content =  response.choices[0].message.content
    print("chatGPT: ", response_content)
    return response_content

# to implement
def get_gpt_completion(transcript):
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

    messages.append({"role": "user", "content": transcript})

    try:
        response = chat_with_gpt(messages, temperature=temperature)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    messages.append({"role": "assistant", "content": response})
    
    # 会話を保存
    data["messages"] = messages
    save_conversation(file_path, data)
    return response

def main():
    file_path = "../conversation.json"
    data = load_conversation(file_path)
    messages = data["messages"]
    temperature = data["temperature"]

    # 最初の説明
    print("これはコマンドラインでchatGPTと対話するシステムです")
    print(f"中断するためには {t_color.RED}exit{t_color.RESET} と入力してください")
    print(f"会話の記録をリセットするためには {t_color.RED}reset{t_color.RESET} と入力してください")
    print(f"会話の履歴は {t_color.GREEN}conversation.json{t_color.RESET} というファイルに保存される")
    print()

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
    from terminal_colors import t_color
    main()
