# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要'})

- 気づき・疑問：mcpサーバを経由してツールを実行する、ということですが、いまいちピンとこないです。また、
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch==2026.11.11", "--no-readability-js"]
これで、外部のMCPサーバを自分のPCから使えるようになる感じもよくわからないので調べます。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：実装
- やったこと：以下をmcp_server.pyへ追加
# TODO(宿題・基礎): get_lecture_summary も公開しよう
server.tool()(tools.get_lecture_summary)    # added in 第6回
server.tool()(tools.make_quiz)              # added in 第6回

- 結果：uv run python -m app.mcp_agent --list-toolsにて、以下のサーバとツールを確認
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[glossary_search_glossary]
  講座の用語集から用語を検索し、定義・関連語・扱う回を返す。
  
  AIエンジニアリングやAIE2026の用語を説明するときに使う。
  比較など複数の用語を含む質問では、用語をすべて1つの query にまとめて
  一度に検索する（例: "LoRAとQLoRA"）。質問文全体ではなく、調べたい用語を指定する。
  講義の要点だけを尋ねられた場合は get_lecture_summary を使う。
  引数: {"query": {"title": "Query", "type": "string"}}

[glossary_get_lecture_summary]
  指定した回（1始まりの整数）の講義の要点を返す。
  
  「第3回では何を学ぶ？」など、特定の回の内容や要点を聞かれたときに使う。
  lecture には質問で指定された回を渡す。用語の定義や確認問題には使わない。
  引数: {"lecture": {"title": "Lecture", "type": "integer"}}

[glossary_make_quiz]
  指定した回の用語から1つ選び、確認問題と正答を返す。
  
  「第2回の確認問題を出して」など、利用者が問題やクイズを求めたときに使う。
  lecture には質問で指定された回を渡す。通常は問題文だけを利用者に提示し、
  正答は利用者が答えを求めたとき、または回答後の採点時にだけ示す。
  引数: {"lecture": {"title": "Lecture", "type": "integer"}}

[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）：５つのツールは省略。

- 気づき・疑問：
１つのサーバへ、ツールを登録することは非常に簡単でした。
実行時、fetchやawsのサーバ接続は不要な質問でしたが、タイムアウトでエラーになりました。
➡「モデルが混み合っています（503）。少し待ってから再実行してください。」
起動時はすべてのサーバにアクセスしていることがわかりました。


以下は実行確認ログです。glossary_make_quiz({'lecture': 4})が正しく呼ばれていました。

uv run python -m app.mcp_agent --trace "AIエンジニアリング講座（AIE2026）第４回の講義内容から理解を深めるためにクイ ズを作成してください。４つの選択肢として、回答を表示してはいけません。"
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
[model] gemini-3.5-flash-lite
[tools] MCP サーバー（app/mcp_servers.json）
第4回の講義内容から、理解度を確認するためのクイズです。４つの選択肢の中から正しいものを考えてみてくださいね！

---

**【第4回 確認問題】**
ルーブリックの意味として最も適切なものはどれでしょうか？

1. LLMの出力結果を自動で丸め込むためのプロンプト圧縮技術
2. 合格・不合格を判定するための基準を、項目ごとに文章で定めたもの
3. データセットの品質を自動的に検証・クレンジングするPythonライブラリ
4. 機械学習モデルのパラメータを効率よくチューニングするためのアルゴリズム

---

答えが分かったら、ぜひ教えてください！また、答えを導くためのヒントが欲しいときも遠慮なく聞いてくださいね。

--- trace ---
[tool call]   glossary_make_quiz({'lecture': 4})
[tool return] glossary_make_quiz -> {"lecture": 4, "question": "ルーブリックの意味は？", "answer": "合格・不合格を判定するための基準を、項目ごとに文章で定めたもの。人にもLLMにも同じ基準を渡して採点させる。基準に書いていないことは人…
[usage] 入力 5,983 tokens / 出力 179 tokens / モデル応答 2 回