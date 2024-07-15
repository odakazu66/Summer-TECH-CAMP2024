from openai import OpenAI
import os
import json

# グローバルでOpenAIのクライエントを定義すると、どこからでも使える
client = OpenAI()

# 会話の履歴とパラメータをロード
def load_conversation(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {
        "messages": [{"role": "system", "content": "あなたは役にたつアシスタントです。"}],
        "temperature": 0.7,
    }

# 会話の履歴とパラメータを保存
def save_conversation(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    

def chat_with_gpt(messages, model="gpt-3.5-turbo", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    response_content =  response.choices[0].message.content
    print("chatGPT: ", response_content)
    return response_content

def main():
    file_path = "../conversation.json"
    data = load_conversation(file_path)
    messages = data["messages"]
    temperature = data["temperature"]

    # 最初の説明
    print("これはコマンドラインでchatGPTと対話するシステムです")
    print("中断するためには exit と入力してください")
    print("会話の記録をリセットするためには reset と入力してください")
    print("会話の履歴は conversation.json というファイルに保存される")
    print()

    while True:
        user_input = input("あなた：")
        
        if user_input.lower() == "exit":
            print("会話を終了する")
            break

        if user_input.lower() == "reset":
            print("会話の履歴をリセットする")
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
