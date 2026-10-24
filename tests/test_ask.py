from app import ask


class FakeChat:
    def __init__(self):
        self.questions = []

    def send_message(self, question):
        self.questions.append(question)
        return FakeResponse(question)


class FakeResponse:
    def __init__(self, text):
        self.text = text
        self.usage_metadata = None


class FakeChats:
    def __init__(self, chat):
        self.chat = chat

    def create(self, model):
        return self.chat


class FakeClient:
    def __init__(self, chat):
        self.chats = FakeChats(chat)


def test_main_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    chat = FakeChat()
    client = FakeClient(chat)
    answers = iter(["2つ目の質問", "exit"])

    monkeypatch.setattr(ask.genai, "Client", lambda api_key: client)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("sys.argv", ["app.ask", "最初の質問"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    ask.main()

    assert chat.questions == ["最初の質問", "2つ目の質問"]
    assert "最初の質問" in capsys.readouterr().out