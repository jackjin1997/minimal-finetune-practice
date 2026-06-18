PYTHON ?= .venv/bin/python
MLX_GENERATE ?= .venv/bin/mlx_lm.generate
MLX_LORA ?= .venv/bin/mlx_lm.lora
MODEL ?= Qwen/Qwen3-0.6B
ADAPTER ?= adapters/task-json-qwen3-0.6b
ITERS ?= 100
CHAT_TEMPLATE_CONFIG ?= '{"enable_thinking": false}'
USER_PROMPT ?= prompts/user.txt
UNSEEN_PROMPT ?= prompts/user_unseen.txt

.PHONY: check-data baseline train-smoke train test generate generate-unseen

check-data:
	$(PYTHON) scripts/check_data.py data

baseline:
	$(MLX_GENERATE) --model $(MODEL) --system-prompt "$$(cat prompts/system.txt)" --prompt "$$(cat $(USER_PROMPT))" --chat-template-config $(CHAT_TEMPLATE_CONFIG) --max-tokens 320 --temp 0

train-smoke:
	$(MLX_LORA) --model $(MODEL) --train --data data --iters 40 --batch-size 1 --learning-rate 1e-5 --mask-prompt --adapter-path $(ADAPTER)

train:
	$(MLX_LORA) --model $(MODEL) --train --data data --iters $(ITERS) --batch-size 1 --learning-rate 1e-5 --mask-prompt --adapter-path $(ADAPTER)

test:
	$(MLX_LORA) --model $(MODEL) --test --data data --mask-prompt --adapter-path $(ADAPTER)

generate:
	$(MLX_GENERATE) --model $(MODEL) --adapter-path $(ADAPTER) --system-prompt "$$(cat prompts/system.txt)" --prompt "$$(cat $(USER_PROMPT))" --chat-template-config $(CHAT_TEMPLATE_CONFIG) --max-tokens 320 --temp 0

generate-unseen:
	$(MLX_GENERATE) --model $(MODEL) --adapter-path $(ADAPTER) --system-prompt "$$(cat prompts/system.txt)" --prompt "$$(cat $(UNSEEN_PROMPT))" --chat-template-config $(CHAT_TEMPLATE_CONFIG) --max-tokens 320 --temp 0
