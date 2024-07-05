from openai import OpenAI

def get_completion(prompt: str) -> str:
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "日本語で。語尾は「なのだ」。一人称は「おいら」。20文字以内。"},
            {"role": "user", "content": prompt}
        ]
    )
    completion_content = completion.choices[0].message.content
    print(completion_content)
    return completion_content
