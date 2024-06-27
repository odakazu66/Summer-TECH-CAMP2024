from openai import OpenAI
#from cloudtts import CachedSpeak
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "日本語で。語尾は「なのだ」。一人称は「おいら」。20文字以内。"},
    {"role": "user", "content": "自己紹介して．"}
  ]
)
#出力結果を文章のみに変更
print(str(completion.choices[0].message)[31:-58])
