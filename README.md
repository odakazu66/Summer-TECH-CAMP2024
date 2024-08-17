# Summer-TECH-CAMP2024

## 前準備
本システムは以下の二つのAPIを利用しています。
- OpenAI: 対話システムの返事作成用
- Google Cloud: 音声認識および音声生成用

そこで、それぞれのAPIキーを事前に取得し、システムに登録する必要があります。登録手法は複数ありますが、以下にその一つを示しています。

> 注意：以下の両方の手順では現在開いているセッションに影響がありません、新しターミナルを開いてから、`main.py`を実行してください。

### 1. OpenAIのAPIキー
OpenAIのキーを環境変数に埋め込むために、以下のコマンドにAPIキーを代入し、実行してください。
#### Windows:
```powershell
setx OPENAI_API_KEY "your-api-key-here"
```
#### Mac OSまたはLinux環境
この環境では以下のコマンドを自分のシェルの設定ファイル(.bashrc, .zshrcなど)に以下のコマンドを張り付けてください。
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Google Cloud のAPIキー
まず、そのAPIの`.json`ファイルをダウンロードし、適当な所に入れてください。その後、そのファイルまでのパスをコピーし、以下のコマンドの引数として代入して、実行してください。
#### Windows:
```powershell
setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\your\credentials.json"
```
#### Mac OSまたはLinux環境
この環境では以下のコマンドを自分のシェルの設定ファイル(.bashrc, .zshrcなど)に以下のコマンドを張り付けてください。
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```

## 環境の準備
まずは、`requirements.txt`に記述しているライブラリーをインストールする。ここでは、仮想環境が必要であれば自分で準備してください。
```bash
pip install -r requirements.txt
```

## 実行方法
環境が準備できたら、`src/`フォルダーに入る
```bash
cd src/
```
### GUIなしで実行
```bash
python main.py
```
### GUIありで実行
```bash
python main.py --use-gui
```


## 目次
 1. [目的](#目的)
    
 2. [システム概要](#システム概要)
    - 使用技術一覧
    - 環境
 
 3. [インストール方法](#インストール方法)
    - APIKeyの取得
      - Google Cloud API
      - Open AI
     
 4. [使用方法](#使用方法)
    
 5. [注意事項](#注意事項)

### 目的
　[Summer-TECH-CAMP2024](https://www.sharen.tut.ac.jp/event/detail.php?y=2024&m=8&d=20#2065) にて使用する音声対話システムの作成

### システム概要
 **○使用技術一覧**
<div align="center">
 <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
</div>

 **○環境**
| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.11.4     |
| Django                | 4.2.1      |
| Django Rest Framework | 3.14.0     |
| MySQL                 | 8.0        |
| Node.js               | 16.17.0    |
| React                 | 18.2.0     |
| Next.js               | 13.4.6     |
| Terraform             | 1.3.6      |


### インストール方法

　

### 使用方法


### 注意事項

