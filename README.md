# Summer-TECH-CAMP2024
## 目次
 1. [目的](#目的)
 2. [システム概要](#システム概要)
 3. [インストール方法](#インストール方法)
 4. [使用方法](#使用方法)

## 目的
　[Summer-TECH-CAMP2024](https://www.sharen.tut.ac.jp/event/detail.php?y=2024&m=8&d=20#2065) にて使用する音声対話システムの作成。

## システム概要
このシステムは以下のAPIの３つを使用している。
- OpenAI API
- Google Cloud API
   - Text to Speech
   - Speech to Text

 **○環境**
使用したライブラリーは以下、または`requirements.txt`の中に示している。

| ライブラリー  | バージョン |
| --------------------- | ---------- |
| annotated-types | 0.7.0 |
| anyio | 4.4.0 |
| cachetools | 5.3.3 |
| certifi | 2024.6.2 |
| charset-normalizer | 3.3.2 |
| colorama | 0.4.6 |
| distro | 1.9.0 |
| exceptiongroup | 1.2.1 |
| google-api-core | 2.19.1 |
| google-auth | 2.30.0 |
| google-cloud-speech | 2.26.0 |
| google-cloud-texttospeech | 2.16.3 |
| googleapis-common-protos | 1.63.2 |
| grpcio | 1.64.1 |
| grpcio-status | 1.62.2 |
| h11 | 0.14.0 |
| httpcore | 1.0.5 |
| httpx | 0.27.0 |
| idna | 3.7 |
| numpy | 2.0.0 |
| openai | 1.35.7 |
| proto-plus | 1.24.0 |
| protobuf | 4.25.3 |
| PyAudio | 0.2.14 |
| pyasn1 | 0.6.0 |
| pyasn1_modules | 0.4.0 |
| pydantic | 2.7.4 |
| pydantic_core | 2.18.4 |
| QtAwesome | 1.3.1 |
| requests | 2.32.3 |
| rsa | 4.9 |
| sniffio | 1.3.1 |
| tqdm | 4.66.4 |
| typing_extensions | 4.12.2 |
| urllib3 | 2.2.2 |
| PyQt5 | 5.15.10 |

## インストール方法
### 前準備
本システムは以下の二つのAPIを利用しています。
- OpenAI: 対話システムの返事作成用
- Google Cloud: 音声認識および音声生成用

そこで、それぞれのAPIキーを事前に取得し、システムに登録する必要があります。登録手法は複数ありますが、以下にその一つを示しています。

> 注意：以下の両方の手順では現在開いているセッションに影響がありません、新しターミナルを開いてから、`main.py`を実行してください。

#### 1. OpenAIのAPIキー
OpenAIのキーを環境変数に埋め込むために、以下のコマンドにAPIキーを代入し、実行してください。
##### Windows:
```powershell
setx OPENAI_API_KEY "your-api-key-here"
```
##### Mac OSまたはLinux環境
この環境では以下のコマンドを自分のシェルの設定ファイル(.bashrc, .zshrcなど)に以下のコマンドを張り付けてください。
```bash
export OPENAI_API_KEY="your-api-key-here"
```

#### 2. Google Cloud のAPIキー
まず、そのAPIの`.json`ファイルをダウンロードし、適当な所に入れてください。その後、そのファイルまでのパスをコピーし、以下のコマンドの引数として代入して、実行してください。
##### Windows:
```powershell
setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\your\credentials.json"
```
##### Mac OSまたはLinux環境
この環境では以下のコマンドを自分のシェルの設定ファイル(.bashrc, .zshrcなど)に以下のコマンドを張り付けてください。
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```

### 環境の準備
まずは、`requirements.txt`に記述しているライブラリーをインストールする。ここでは、仮想環境が必要であれば自分で準備してください。
```bash
pip install -r requirements.txt
```

## 使用方法
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

