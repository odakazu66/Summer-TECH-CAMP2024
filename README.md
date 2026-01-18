# Summer-TECH-CAMP2024

## 目次

1. [目的](#目的)
2. [システム概要](#システム概要)
3. [インストール方法](#インストール方法)
4. [使用方法](#使用方法)

## 目的

[Summer-TECH-CAMP2024](https://www.sharen.tut.ac.jp/event/detail.php?y=2024&m=8&d=20#2065) にて使用する音声対話システムの作成。

> 手順書はこちらのファイルをご参照ください：[手順書](https://github.com/odakazu66/Summer-TECH-CAMP2024/blob/main/%E6%89%8B%E9%A0%86%E6%9B%B8.pdf)

## システム概要

このシステムは以下のコンポーネントを利用しています（デフォルト構成）：

* OpenAI API — 対話生成
* faster-whisper — 音声認識（ローカル実行の高速ASR）
* Google Translate の TTS — 音声合成

※ Google Cloud の Speech-to-Text / Text-to-Speech は**デフォルトでは使用しません**。
利用したい場合は、事前に Google Cloud の API を準備し、環境変数を設定した上で、起動時に `--use-google` フラグを指定してください（後述）。

**○環境**

* 必要な Python ライブラリは `requirements.txt` にまとめています。Pythonの仮想環境の利用を推奨します。

## インストール方法

### uv のインストール

本プロジェクトでは `uv` を使用します。以下の公式ドキュメントを参照し、事前に `uv` をインストールしてください。

* [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### 前準備

本システムは OpenAI（必須）と、デフォルトで faster-whisper / Google Translate TTS（必須）を利用します。
各 API キーや認証情報は、それぞれの公式サイトから事前に取得してください。取得手順の詳細については、以下の手順書にまとめています。

> 手順書： [手順書](https://github.com/odakazu66/Summer-TECH-CAMP2024/blob/main/%E6%89%8B%E9%A0%86%E6%9B%B8.pdf)

Google Cloud の API を使用したい場合は、その認証ファイルを配置して環境変数を設定してください（任意）。

#### 1. OpenAI の API キー

取得した OpenAI の API キーを環境変数に設定してください。

##### Windows (PowerShell)

PowerShell を開き、以下のコマンドを**実行**してください：

```powershell
setx OPENAI_API_KEY "your-api-key-here"
```

##### macOS / Linux

シェル設定ファイル（`.bashrc`, `.zshrc` 等）に追記して下さい：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

#### 2. （任意）Google Cloud の認証

Google Cloud の API（利用する場合）については、サービスアカウントの JSON をダウンロードしておき、環境変数 `GOOGLE_APPLICATION_CREDENTIALS` にフルパスをセットしてください。

##### Windows (PowerShell)

PowerShell を開き、以下のコマンドを**実行**してください：

```powershell
setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\your\credentials.json"
```

##### macOS / Linux

以下の行をシェル設定ファイル（`.bashrc`, `.zshrc` 等）に追記してください：

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```

> 補足：Google Cloud を使う場合は、起動時に `--use-google` フラグを指定します（例：`uv run main.py --use-gui --use-google`）。

### ffmpeg のインストール（pydub と faster-whisper のため）

`pydub` は内部で `ffmpeg` を利用します。また、`faster-whisper` や一部の音声処理処理も `ffmpeg` を必要とする場合があります。OS ごとのインストール方法の例を示します。

* **Windows**

  * 推奨：パッケージマネージャを利用（例: `winget`, `chocolatey`）
    * 例（このコマンドは管理者として実行した`Windows Powershell`の中で実行してください）: `winget install ffmpeg`
    * または: `choco install ffmpeg`
  * 手動ダウンロード：Windows 用ビルド（静的ビルド）は [gyan.dev のビルド配布ページ](https://www.gyan.dev/ffmpeg/builds/) からダウンロードできます。
    * この場合は、ダウンロードした bin フォルダ（`ffmpeg.exe` のある場所）を PATH に追加してください。

* **macOS**

  * Homebrew があれば：

    ```bash
    brew install ffmpeg
    ```

* **Linux (Debian/Ubuntu)**

  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

他のディストリビューションでは `yum` / `dnf` / `pacman` 等を利用してください。

* **注意**
  * インストール後、`ffmpeg` がコマンドラインから `ffmpeg -version` で確認できることを確かめてください。

## 使用方法
本プロジェクトでは `uv` コマンドを使って実行します（`uv sync` → `uv run` のワークフロー）。

1. まずリポジトリルートで同期処理を行います：
```bash
uv sync
````

2. `src/` に移動してアプリを起動します。

```bash
cd src/
uv run main.py [--use-gui] [--use-google]
```

* `--use-gui` : GUI を有効にして起動します。
* `--use-google` : Google Cloud の STT / TTS を使用する（事前に `GOOGLE_APPLICATION_CREDENTIALS` を設定しておくこと）。

### 例

* GUI を使ってデフォルト（faster-whisper + Google Translate TTS）で起動：

```bash
uv sync
cd src/
uv run main.py --use-gui
```

* GUI を使い、Google Cloud の API を利用して起動（API キー / 認証を設定済みの場合）：

```bash
uv sync
cd src/
uv run main.py --use-gui --use-google
```