# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：
- 用語集の正しい意味と比べて気づいたこと：
- 表示できたトークン数（入力 / 出力）：

## 宿題

- 取り組んだレベル： 実装
- やったこと：ask.pyで会話履歴を保持して質問できるようにする
- 結果：一度だけchatを作成しask関数で質問だけ変える、というコード変更です。
def ask(chat, question: str) -> str:
    response = chat.send_message(question)
    return response.text

def main() -> None:
    # 省略
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        question = args.question
        while True:
            print(f"[質問] {question}\n")
            print(ask(chat, question))
            try:
                question = input("\n[次の質問 / 終了は exit] ").strip()
            # 以下省略
- 気づき・疑問：入力トークンは会話を重ねるごとに増え続けた。過去の入出力トークンが積みあがっているためだと思われます。また、chatを一度だけ作成し、chat.send_message(question)とするだけで、特に文字列の連結指示などせずに内部的に会話履歴が反映されているようだった。それら履歴情報が内部でどのように使われているか、知りたいと思った。
