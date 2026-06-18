PYTHON ?= .venv/bin/python
MLX_GENERATE ?= .venv/bin/mlx_lm.generate
MLX_LORA ?= .venv/bin/mlx_lm.lora
MODEL ?= Qwen/Qwen3-0.6B
ADAPTER ?= adapters/task-json-qwen3-0.6b
ITERS ?= 240

.PHONY: check-data baseline train-smoke train test generate

check-data:
	$(PYTHON) scripts/check_data.py data

baseline:
	$(MLX_GENERATE) --model $(MODEL) --prompt "$$(cat prompts/task_json_prompt.txt)" --max-tokens 320

train-smoke:
	$(MLX_LORA) --model $(MODEL) --train --data data --iters 40 --batch-size 1 --learning-rate 1e-5 --adapter-path $(ADAPTER)

train:
	$(MLX_LORA) --model $(MODEL) --train --data data --iters $(ITERS) --batch-size 1 --learning-rate 1e-5 --adapter-path $(ADAPTER)

test:
	$(MLX_LORA) --model $(MODEL) --test --data data --adapter-path $(ADAPTER)

generate:
	$(MLX_GENERATE) --model $(MODEL) --adapter-path $(ADAPTER) --prompt "$$(cat prompts/task_json_prompt.txt)" --max-tokens 320
