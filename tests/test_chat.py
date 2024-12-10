
import cyllama.cyllama as cy


def test_chat_builtin_templates():
	assert cy.chat_builtin_templates() == [
		'chatglm3',
		'chatglm4',
		'chatml',
		'command-r',
		'deepseek',
		'deepseek2',
		'exaone3',
		'gemma',
		'granite',
		'llama2',
		'llama2-sys',
		'llama2-sys-bos',
		'llama2-sys-strip',
		'llama3',
		'minicpm',
		'mistral-v1',
		'mistral-v3',
		'mistral-v3-tekken',
		'mistral-v7',
		'monarch',
		'openchat',
		'orion',
		'phi3',
		'rwkv-world',
		'vicuna',
		'vicuna-orca',
		'zephyr',
    ]

