
from pyllama.pyllama import ask


def test_ask(model_path):
    assert ask("When did the universe begin?", model=model_path, n_predict=32, n_ctx=512)

